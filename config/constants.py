"""
Constants and enums for X Reply Bot.
"""

from enum import Enum
from typing import Dict, List


class ReplyStyle(str, Enum):
    """Available reply styles for generated responses."""

    GENZ = "genz"
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    SARCASTIC = "sarcastic"
    MOTIVATIONAL = "motivational"

    @classmethod
    def get_description(cls, style: "ReplyStyle") -> str:
        """Get human-readable description for a style."""
        descriptions = {
            cls.GENZ: "GenZ - Trendy, casual, emoji-heavy",
            cls.PROFESSIONAL: "Professional - Formal, business-appropriate",
            cls.CASUAL: "Casual - Friendly, conversational",
            cls.SARCASTIC: "Sarcastic - Witty, ironic tone",
            cls.MOTIVATIONAL: "Motivational - Inspirational, uplifting",
        }
        return descriptions.get(style, str(style))


class ReplyLength(str, Enum):
    """Available reply length options."""

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"
    CUSTOM = "custom"

    @classmethod
    def get_word_range(cls, length: "ReplyLength") -> tuple[int, int]:
        """Get word count range for a length option."""
        ranges = {
            cls.SHORT: (10, 30),
            cls.MEDIUM: (50, 100),
            cls.LONG: (150, 250),
        }
        return ranges.get(length, (50, 100))


class Language(str, Enum):
    """Supported languages for reply generation."""

    ENGLISH = "english"
    URDU = "urdu"
    JAPANESE = "japanese"
    SPANISH = "spanish"
    FRENCH = "french"
    GERMAN = "german"
    CHINESE = "chinese"
    HINDI = "hindi"
    PORTUGUESE = "portuguese"
    RUSSIAN = "russian"

    @classmethod
    def get_display_name(cls, lang: "Language") -> str:
        """Get display name for a language."""
        display_names = {
            cls.ENGLISH: "🇬🇧 English",
            cls.URDU: "🇵🇰 اردو",
            cls.JAPANESE: "🇯🇵 日本語",
            cls.SPANISH: "🇪🇸 Español",
            cls.FRENCH: "🇫🇷 Français",
            cls.GERMAN: "🇩🇪 Deutsch",
            cls.CHINESE: "🇨🇳 中文",
            cls.HINDI: "🇮🇳 हिंदी",
            cls.PORTUGUESE: "🇧🇷 Português",
            cls.RUSSIAN: "🇷🇺 Русский",
        }
        return display_names.get(lang, lang.value)


# Style prompts for AI generation
STYLE_PROMPTS: Dict[ReplyStyle, str] = {
    ReplyStyle.GENZ: "Write in GenZ style: use trendy slang, emojis, casual language, and internet culture references. Keep it fun and relatable.",
    ReplyStyle.PROFESSIONAL: "Write in a professional tone: use formal language, business-appropriate vocabulary, and maintain a respectful demeanor.",
    ReplyStyle.CASUAL: "Write in a casual, friendly tone: be conversational, warm, and approachable while maintaining clarity.",
    ReplyStyle.SARCASTIC: "Write with sarcasm and wit: use irony and clever humor while keeping the message understandable.",
    ReplyStyle.MOTIVATIONAL: "Write in an inspirational and motivational tone: encourage, uplift, and provide positive energy.",
}

# Language instructions for AI
LANGUAGE_INSTRUCTIONS: Dict[Language, str] = {
    Language.ENGLISH: "Respond in English.",
    Language.URDU: "جواب اردو میں دیں۔",
    Language.JAPANESE: "日本語で応答してください。",
    Language.SPANISH: "Responda en español.",
    Language.FRENCH: "Répondez en français.",
    Language.GERMAN: "Antworten Sie auf Deutsch.",
    Language.CHINESE: "用中文回应。",
    Language.HINDI: "हिंदी में जवाब दें।",
    Language.PORTUGUESE: "Responda em português.",
    Language.RUSSIAN: "Ответьте на русском языке.",
}

# Twitter/X URL patterns
TWITTER_URL_PATTERNS = [
    "twitter.com",
    "x.com",
    "t.co",
]

# Telegram command descriptions
COMMAND_DESCRIPTIONS = {
    "start": "Start the bot and see available commands",
    "reply": "Generate replies for a tweet (text, link, or image)",
    "help": "Show help information",
    "settings": "Configure bot preferences",
}

# Error messages
ERROR_MESSAGES = {
    "invalid_url": "❌ Invalid Twitter/X URL. Please provide a valid tweet link.",
    "tweet_not_found": "❌ Tweet not found. Please check the URL and try again.",
    "ocr_failed": "❌ Failed to extract text from image. Please try a clearer image.",
    "api_error": "❌ API error occurred. Please try again later.",
    "invalid_input": "❌ Invalid input. Please provide text, a tweet link, or an image.",
    "generation_failed": "❌ Failed to generate replies. Please try again.",
}

# Success messages
SUCCESS_MESSAGES = {
    "tweet_fetched": "✅ Tweet fetched successfully!",
    "text_extracted": "✅ Text extracted from image!",
    "replies_generated": "✅ Replies generated! Select one to post:",
    "reply_posted": "✅ Reply posted successfully!",
}
