"""
Telegram bot handler for X Reply Bot.
Manages all user interactions and command processing.
"""

import logging
import os
from typing import Optional

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    User,
)
from telegram.constants import ChatAction, ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot.ai_generator import AIGenerator
from bot.ocr_processor import OCRProcessor
from bot.twex_client import TwexAPIClient
from bot.utils import (
    cleanup_file,
    cleanup_temp_dir,
    create_temp_dir,
    download_file,
    extract_url_from_text,
    format_tweet_text,
    get_user_mention,
    setup_logging,
    truncate_text,
)
from config.constants import (
    ERROR_MESSAGES,
    COMMAND_DESCRIPTIONS,
    Language,
    ReplyLength,
    ReplyStyle,
    SUCCESS_MESSAGES,
)
from config.settings import settings

logger = logging.getLogger(__name__)

# Conversation states
(
    WAITING_FOR_INPUT,
    WAITING_FOR_STYLE,
    WAITING_FOR_LENGTH,
    WAITING_FOR_LANGUAGE,
    WAITING_FOR_CUSTOM_LENGTH,
    WAITING_FOR_CONFIRMATION,
) = range(6)


class TelegramBotHandler:
    """Handle Telegram bot interactions."""

    def __init__(self):
        """Initialize bot handler with API clients."""
        self.twex_client = TwexAPIClient()
        self.ai_generator = AIGenerator()
        self.current_tweet_text: Optional[str] = None
        self.current_tweet_id: Optional[str] = None
        self.current_style: Optional[ReplyStyle] = None
        self.current_length: Optional[ReplyLength] = None
        self.current_language: Optional[Language] = None
        self.current_replies: Optional[list] = None
        self.temp_dir: Optional[str] = None

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle /start command."""
        user = get_user_mention(update)
        welcome_message = f"""👋 Welcome to X Reply Bot, {user}!

I help you generate creative replies for Twitter/X posts. Here's what I can do:

🔄 **Generate Replies** - Send me:
  • A tweet link (twitter.com/user/status/...)
  • A screenshot of a tweet
  • Plain text of a tweet

🎨 **Customize Style** - Choose from:
  • GenZ - Trendy and casual
  • Professional - Formal and business-like
  • Casual - Friendly and conversational
  • Sarcastic - Witty and ironic
  • Motivational - Inspirational and uplifting

📏 **Adjust Length** - Pick:
  • Short (10-30 words)
  • Medium (50-100 words)
  • Long (150-250 words)
  • Custom word count

🌍 **Multiple Languages** - Supported:
  • English, Urdu, Japanese, Spanish, French
  • German, Chinese, Hindi, Portuguese, Russian

Use /reply to get started!"""

        await update.message.reply_text(welcome_message)
        return WAITING_FOR_INPUT

    async def help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Handle /help command."""
        help_text = """📚 **Available Commands:**

/start - Show welcome message
/help - Show this help message
/reply - Start generating replies
/cancel - Cancel current operation

**How to use:**
1. Send /reply
2. Provide tweet (link, screenshot, or text)
3. Choose reply style
4. Select reply length
5. Pick language
6. Review and post generated replies

**Tips:**
• For best results, use clear tweet screenshots
• Custom word count must be between 10-280
• Each reply is limited to 280 characters for Twitter/X
• You can generate multiple reply options at once"""

        await update.message.reply_text(help_text)

    async def reply_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle /reply command - start reply generation workflow."""
        await update.message.reply_text(
            "📝 **Send me a tweet to reply to:**\n\n"
            "You can send:\n"
            "• A Twitter/X link\n"
            "• A screenshot of the tweet\n"
            "• The tweet text directly",
            parse_mode=ParseMode.MARKDOWN,
        )
        return WAITING_FOR_INPUT

    async def handle_input(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle tweet input (text, link, or image)."""
        try:
            # Create temp directory for file operations
            self.temp_dir = create_temp_dir()

            # Check if input is an image
            if update.message.photo:
                return await self._handle_image_input(update, context)

            # Check if input is text with URL
            elif update.message.text:
                text = update.message.text.strip()

                # Try to extract tweet URL
                url = extract_url_from_text(text)
                if url:
                    return await self._handle_url_input(update, context, url)

                # Otherwise treat as plain text
                return await self._handle_text_input(update, context, text)

            else:
                await update.message.reply_text(
                    ERROR_MESSAGES["invalid_input"],
                    parse_mode=ParseMode.MARKDOWN,
                )
                return WAITING_FOR_INPUT

        except Exception as e:
            logger.error(f"Error handling input: {str(e)}")
            await update.message.reply_text(
                ERROR_MESSAGES["api_error"], parse_mode=ParseMode.MARKDOWN
            )
            return WAITING_FOR_INPUT

    async def _handle_text_input(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str
    ) -> int:
        """Handle plain text input."""
        self.current_tweet_text = text
        self.current_tweet_id = None

        await update.message.reply_text(
            f"✅ Got your text:\n\n\"{truncate_text(text, 200)}\"\n\n"
            "Now let's choose a style for the reply.",
            parse_mode=ParseMode.MARKDOWN,
        )

        return await self._show_style_options(update, context)

    async def _handle_url_input(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, url: str
    ) -> int:
        """Handle Twitter/X URL input."""
        await update.message.reply_chat_action(ChatAction.TYPING)

        # Extract tweet ID from URL
        tweet_id = TwexAPIClient.extract_tweet_id(url)
        if not tweet_id:
            await update.message.reply_text(
                ERROR_MESSAGES["invalid_url"], parse_mode=ParseMode.MARKDOWN
            )
            return WAITING_FOR_INPUT

        # Fetch tweet from TwexAPI
        tweet = self.twex_client.get_tweet(tweet_id)
        if not tweet:
            await update.message.reply_text(
                ERROR_MESSAGES["tweet_not_found"], parse_mode=ParseMode.MARKDOWN
            )
            return WAITING_FOR_INPUT

        # Extract tweet text
        self.current_tweet_text = tweet.get("text") or tweet.get("full_text", "")
        self.current_tweet_id = tweet_id

        await update.message.reply_text(
            f"✅ {SUCCESS_MESSAGES['tweet_fetched']}\n\n"
            f"Tweet: \"{truncate_text(self.current_tweet_text, 200)}\"\n\n"
            "Now let's choose a style for the reply.",
            parse_mode=ParseMode.MARKDOWN,
        )

        return await self._show_style_options(update, context)

    async def _handle_image_input(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle image/screenshot input with OCR."""
        try:
            await update.message.reply_chat_action(ChatAction.TYPING)

            # Download image from Telegram
            photo_file = await update.message.photo[-1].get_file()
            image_path = os.path.join(self.temp_dir, "tweet_screenshot.jpg")

            await photo_file.download_to_drive(image_path)

            # Extract text using OCR
            extracted_text = OCRProcessor.extract_text(image_path)

            if not extracted_text:
                await update.message.reply_text(
                    ERROR_MESSAGES["ocr_failed"], parse_mode=ParseMode.MARKDOWN
                )
                return WAITING_FOR_INPUT

            self.current_tweet_text = extracted_text
            self.current_tweet_id = None

            await update.message.reply_text(
                f"✅ {SUCCESS_MESSAGES['text_extracted']}\n\n"
                f"Extracted: \"{truncate_text(extracted_text, 200)}\"\n\n"
                "Now let's choose a style for the reply.",
                parse_mode=ParseMode.MARKDOWN,
            )

            return await self._show_style_options(update, context)

        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            await update.message.reply_text(
                ERROR_MESSAGES["ocr_failed"], parse_mode=ParseMode.MARKDOWN
            )
            return WAITING_FOR_INPUT

    async def _show_style_options(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Show reply style selection buttons."""
        keyboard = [
            [
                InlineKeyboardButton("GenZ", callback_data="style_genz"),
                InlineKeyboardButton("Professional", callback_data="style_professional"),
            ],
            [
                InlineKeyboardButton("Casual", callback_data="style_casual"),
                InlineKeyboardButton("Sarcastic", callback_data="style_sarcastic"),
            ],
            [InlineKeyboardButton("Motivational", callback_data="style_motivational")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🎨 **Choose a reply style:**",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN,
        )

        return WAITING_FOR_STYLE

    async def style_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle style selection."""
        query = update.callback_query
        await query.answer()

        style_map = {
            "style_genz": ReplyStyle.GENZ,
            "style_professional": ReplyStyle.PROFESSIONAL,
            "style_casual": ReplyStyle.CASUAL,
            "style_sarcastic": ReplyStyle.SARCASTIC,
            "style_motivational": ReplyStyle.MOTIVATIONAL,
        }

        self.current_style = style_map.get(query.data)

        await query.edit_message_text(
            f"✅ Style: {ReplyStyle.get_description(self.current_style)}\n\n"
            "📏 **Now choose reply length:**",
            parse_mode=ParseMode.MARKDOWN,
        )

        # Show length options
        keyboard = [
            [
                InlineKeyboardButton("Short (10-30)", callback_data="length_short"),
                InlineKeyboardButton("Medium (50-100)", callback_data="length_medium"),
            ],
            [
                InlineKeyboardButton("Long (150-250)", callback_data="length_long"),
                InlineKeyboardButton("Custom", callback_data="length_custom"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "📏 **Choose reply length:**",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN,
        )

        return WAITING_FOR_LENGTH

    async def length_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle length selection."""
        query = update.callback_query
        await query.answer()

        length_map = {
            "length_short": ReplyLength.SHORT,
            "length_medium": ReplyLength.MEDIUM,
            "length_long": ReplyLength.LONG,
            "length_custom": ReplyLength.CUSTOM,
        }

        self.current_length = length_map.get(query.data)

        if self.current_length == ReplyLength.CUSTOM:
            await query.edit_message_text(
                "📝 **Enter custom word count (10-280):**"
            )
            return WAITING_FOR_CUSTOM_LENGTH

        # Show language options
        return await self._show_language_options(update, context, query)

    async def custom_length_input(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle custom word count input."""
        try:
            word_count = int(update.message.text.strip())

            if word_count < 10 or word_count > 280:
                await update.message.reply_text(
                    "❌ Word count must be between 10 and 280. Please try again."
                )
                return WAITING_FOR_CUSTOM_LENGTH

            context.user_data["custom_word_count"] = word_count
            await update.message.reply_text(
                f"✅ Custom length set to {word_count} words\n\n"
                "🌍 **Now choose a language:**"
            )

            return await self._show_language_options(update, context)

        except ValueError:
            await update.message.reply_text(
                "❌ Please enter a valid number between 10 and 280."
            )
            return WAITING_FOR_CUSTOM_LENGTH

    async def _show_language_options(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, query=None
    ) -> int:
        """Show language selection buttons."""
        keyboard = [
            [
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_english"),
                InlineKeyboardButton("🇵🇰 اردو", callback_data="lang_urdu"),
            ],
            [
                InlineKeyboardButton("🇯🇵 日本語", callback_data="lang_japanese"),
                InlineKeyboardButton("🇪🇸 Español", callback_data="lang_spanish"),
            ],
            [
                InlineKeyboardButton("🇫🇷 Français", callback_data="lang_french"),
                InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_german"),
            ],
            [
                InlineKeyboardButton("🇨🇳 中文", callback_data="lang_chinese"),
                InlineKeyboardButton("🇮🇳 हिंदी", callback_data="lang_hindi"),
            ],
            [
                InlineKeyboardButton("🇧🇷 Português", callback_data="lang_portuguese"),
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_russian"),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        if query:
            await query.edit_message_text(
                "🌍 **Choose a language:**",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await update.message.reply_text(
                "🌍 **Choose a language:**",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN,
            )

        return WAITING_FOR_LANGUAGE

    async def language_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle language selection and generate replies."""
        query = update.callback_query
        await query.answer()

        language_map = {
            "lang_english": Language.ENGLISH,
            "lang_urdu": Language.URDU,
            "lang_japanese": Language.JAPANESE,
            "lang_spanish": Language.SPANISH,
            "lang_french": Language.FRENCH,
            "lang_german": Language.GERMAN,
            "lang_chinese": Language.CHINESE,
            "lang_hindi": Language.HINDI,
            "lang_portuguese": Language.PORTUGUESE,
            "lang_russian": Language.RUSSIAN,
        }

        self.current_language = language_map.get(query.data)

        await query.edit_message_text("⏳ Generating replies... Please wait.")
        await query.message.chat.send_action(ChatAction.TYPING)

        # Generate replies
        custom_word_count = context.user_data.get("custom_word_count")
        replies = self.ai_generator.generate_replies(
            tweet_text=self.current_tweet_text,
            style=self.current_style,
            length=self.current_length,
            language=self.current_language,
            num_replies=3,
            custom_word_count=custom_word_count,
        )

        if not replies:
            await query.edit_message_text(
                ERROR_MESSAGES["generation_failed"], parse_mode=ParseMode.MARKDOWN
            )
            return WAITING_FOR_INPUT

        self.current_replies = replies

        # Display replies with selection buttons
        reply_text = f"✅ {SUCCESS_MESSAGES['replies_generated']}\n\n"

        for i, reply in enumerate(replies, 1):
            reply_text += f"**Option {i}:**\n{format_tweet_text(reply)}\n\n"

        keyboard = [
            [
                InlineKeyboardButton(f"✓ Post Reply {i+1}", callback_data=f"post_{i}")
                for i in range(len(replies))
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(reply_text, parse_mode=ParseMode.MARKDOWN)
        await query.message.reply_text(
            "Select a reply to post to X:", reply_markup=reply_markup
        )

        return WAITING_FOR_CONFIRMATION

    async def post_reply_callback(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Handle reply posting to X."""
        query = update.callback_query
        await query.answer()

        # Extract reply index
        reply_index = int(query.data.split("_")[1])

        if reply_index >= len(self.current_replies):
            await query.edit_message_text("❌ Invalid reply selection.")
            return WAITING_FOR_INPUT

        selected_reply = self.current_replies[reply_index]

        try:
            await query.edit_message_text("⏳ Posting reply to X... Please wait.")

            if self.current_tweet_id:
                # Post as reply to tweet
                posted_id = self.twex_client.post_reply(
                    self.current_tweet_id, selected_reply
                )
            else:
                # Post as standalone tweet
                posted_id = self.twex_client.post_tweet(selected_reply)

            if posted_id:
                await query.edit_message_text(
                    f"✅ {SUCCESS_MESSAGES['reply_posted']}\n\n"
                    f"Tweet ID: `{posted_id}`\n\n"
                    "Use /reply to generate more replies!",
                    parse_mode=ParseMode.MARKDOWN,
                )
            else:
                await query.edit_message_text(
                    ERROR_MESSAGES["api_error"], parse_mode=ParseMode.MARKDOWN
                )

        except Exception as e:
            logger.error(f"Error posting reply: {str(e)}")
            await query.edit_message_text(
                ERROR_MESSAGES["api_error"], parse_mode=ParseMode.MARKDOWN
            )

        finally:
            # Cleanup
            if self.temp_dir:
                cleanup_temp_dir(self.temp_dir)

        return WAITING_FOR_INPUT

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Handle /cancel command."""
        # Cleanup
        if self.temp_dir:
            cleanup_temp_dir(self.temp_dir)

        await update.message.reply_text(
            "❌ Operation cancelled. Use /reply to start again."
        )
        return WAITING_FOR_INPUT

    def build_application(self) -> Application:
        """Build and configure Telegram application."""
        app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

        # Conversation handler for reply workflow
        reply_handler = ConversationHandler(
            entry_points=[CommandHandler("reply", self.reply_command)],
            states={
                WAITING_FOR_INPUT: [
                    MessageHandler(filters.TEXT | filters.PHOTO, self.handle_input),
                ],
                WAITING_FOR_STYLE: [
                    CallbackQueryHandler(self.style_callback, pattern="^style_"),
                ],
                WAITING_FOR_LENGTH: [
                    CallbackQueryHandler(self.length_callback, pattern="^length_"),
                ],
                WAITING_FOR_CUSTOM_LENGTH: [
                    MessageHandler(filters.TEXT, self.custom_length_input),
                ],
                WAITING_FOR_LANGUAGE: [
                    CallbackQueryHandler(self.language_callback, pattern="^lang_"),
                ],
                WAITING_FOR_CONFIRMATION: [
                    CallbackQueryHandler(self.post_reply_callback, pattern="^post_"),
                ],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )

        # Add handlers
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(reply_handler)

        return app


async def run_bot() -> None:
    """Run the Telegram bot."""
    # Setup logging
    setup_logging(settings.LOG_LEVEL)

    # Validate API keys
    logger.info("Validating API keys...")
    handler = TelegramBotHandler()

    if not handler.twex_client.validate_api_key():
        logger.error("Invalid TwexAPI key. Please check your configuration.")
        return

    if not handler.ai_generator.validate_api_key():
        logger.error("Invalid OpenAI API key. Please check your configuration.")
        return

    logger.info("All API keys validated successfully!")

    # Build and start application
    app = handler.build_application()

    logger.info("Starting X Reply Bot...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_bot())
