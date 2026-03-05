# X Reply Bot 🤖

A powerful Telegram bot that generates customizable, AI-powered replies for X (Twitter) posts. Supports multiple reply styles, languages, and input methods (text, links, or screenshots).

## Features ✨

### Input Methods
- **Tweet Links**: Automatically fetch tweet content via TwexAPI
- **Screenshots**: Extract text from tweet screenshots using Tesseract OCR
- **Plain Text**: Directly provide tweet text for reply generation

### Reply Customization
- **5 Reply Styles**:
  - 🎨 **GenZ**: Trendy, casual, emoji-heavy responses
  - 💼 **Professional**: Formal, business-appropriate tone
  - 😊 **Casual**: Friendly, conversational style
  - 😏 **Sarcastic**: Witty, ironic humor
  - 🌟 **Motivational**: Inspirational, uplifting messages

- **4 Length Options**:
  - Short: 10-30 words
  - Medium: 50-100 words
  - Long: 150-250 words
  - Custom: Specify exact word count

- **10 Languages**:
  - English, Urdu, Japanese, Spanish, French
  - German, Chinese, Hindi, Portuguese, Russian

### AI-Powered Generation
- Uses **OpenAI ChatGPT-4o** for intelligent reply generation
- Generates multiple reply options (default: 3 variations)
- Ensures replies fit Twitter's 280-character limit
- Context-aware responses based on original tweet

### Direct Posting
- Post generated replies directly to X via TwexAPI
- Support for both replies to existing tweets and standalone posts
- Instant confirmation with tweet IDs

## Architecture 🏗️

```
x-reply-bot/
├── bot/                          # Core bot logic
│   ├── main.py                   # Entry point
│   ├── telegram_handler.py        # Telegram Bot API integration
│   ├── twex_client.py             # TwexAPI wrapper
│   ├── ai_generator.py            # ChatGPT-4o integration
│   ├── ocr_processor.py           # Tesseract OCR
│   └── utils.py                   # Helper functions
├── config/
│   ├── settings.py                # Configuration management
│   └── constants.py               # Constants and enums
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md                      # This file
```

## Technology Stack 🛠️

| Component | Technology |
|-----------|-----------|
| **Bot Framework** | python-telegram-bot 21.0.1 |
| **X API** | TwexAPI (REST API wrapper) |
| **AI Model** | OpenAI ChatGPT-4o |
| **OCR Engine** | Tesseract OCR via pytesseract |
| **Image Processing** | Pillow (PIL) |
| **HTTP Client** | requests |
| **Configuration** | python-dotenv, pydantic |

## Installation 📦

### Prerequisites
- Python 3.9 or higher
- Tesseract OCR engine
- API keys for: Telegram Bot API, TwexAPI, OpenAI

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/x-reply-bot.git
cd x-reply-bot
```

### Step 2: Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr libtesseract-dev
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download installer from [GitHub Tesseract releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# TwexAPI Configuration
TWEXAPI_KEY=your_twexapi_bearer_token_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o

# Optional: Tesseract path (if not in system PATH)
TESSERACT_PATH=/usr/bin/tesseract

# Bot Configuration
BOT_ADMIN_ID=your_telegram_user_id_here
LOG_LEVEL=INFO
```

## Getting API Keys 🔑

### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions
3. Copy the provided bot token

### TwexAPI Key
1. Visit [TwexAPI Dashboard](https://dashboard.twexapi.com)
2. Sign up for a free account
3. Generate API key from dashboard
4. Copy the Bearer token

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in
3. Go to API keys section
4. Create new secret key
5. Copy the key

## Usage 🚀

### Start the Bot
```bash
python bot/main.py
```

The bot will validate all API keys and start listening for commands.

### Telegram Commands

| Command | Description |
|---------|-------------|
| `/start` | Show welcome message and available features |
| `/reply` | Start the reply generation workflow |
| `/help` | Display help information |
| `/cancel` | Cancel current operation |

### Workflow Example

1. **Send `/reply`** - Start the workflow
2. **Provide Input** - Send tweet link, screenshot, or text
3. **Choose Style** - Select from 5 reply styles
4. **Select Length** - Pick reply length (short/medium/long/custom)
5. **Pick Language** - Choose from 10 supported languages
6. **Review Replies** - See 3 AI-generated options
7. **Post Reply** - Select one to post to X

## Configuration Details ⚙️

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | Telegram Bot API token |
| `TWEXAPI_KEY` | ✅ | TwexAPI Bearer token |
| `OPENAI_API_KEY` | ✅ | OpenAI API key |
| `OPENAI_MODEL` | ❌ | Model name (default: gpt-4o) |
| `TESSERACT_PATH` | ❌ | Path to Tesseract binary |
| `BOT_ADMIN_ID` | ❌ | Admin user ID for special features |
| `LOG_LEVEL` | ❌ | Logging level (default: INFO) |

### Reply Styles Details

**GenZ Style**: Uses trendy slang, emojis, and internet culture references. Perfect for casual, relatable responses.

**Professional Style**: Maintains formal language and business etiquette. Ideal for corporate or serious contexts.

**Casual Style**: Friendly and conversational tone. Great for everyday interactions.

**Sarcastic Style**: Employs wit and irony while keeping messages understandable. Best for clever, humorous replies.

**Motivational Style**: Inspirational and uplifting. Perfect for encouraging and positive responses.

## API Integration Details 🔌

### TwexAPI Integration
- **Endpoint**: `https://api.twexapi.io`
- **Authentication**: Bearer token in Authorization header
- **Key Operations**:
  - `POST /twitter/tweets/lookup` - Fetch tweet details
  - `POST /twitter/tweets/create` - Post tweets and replies
- **Cost**: $0.01 per API call
- **Rate Limit**: 20+ requests/second

### OpenAI Integration
- **Model**: GPT-4o (latest multimodal model)
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 2000 per request
- **Context**: System prompts include style, language, and length constraints

### Tesseract OCR
- **Supported Formats**: JPG, PNG, GIF, BMP, WebP
- **Max File Size**: 10MB
- **Language Support**: 100+ languages via language codes
- **Processing**: Image preprocessing for optimal text extraction

## Troubleshooting 🔧

### "Tesseract not installed" Error
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Then set TESSERACT_PATH in .env if needed
```

### "Invalid API Key" Error
- Verify API keys in `.env` file
- Ensure no extra whitespace in keys
- Check that API keys haven't expired
- Confirm API keys have necessary permissions

### OCR Not Extracting Text
- Ensure image is clear and readable
- Try higher resolution screenshots
- Check supported image format
- Verify Tesseract installation

### Bot Not Responding
- Check bot token is correct
- Verify internet connection
- Check logs for error messages
- Ensure all required environment variables are set

## Logging 📝

Logs are written to `bot.log` and console output. Configure log level via `LOG_LEVEL` environment variable:

```bash
# Available levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=DEBUG
```

## Performance Considerations ⚡

- **Reply Generation**: ~5-10 seconds (depends on OpenAI API)
- **OCR Processing**: ~2-5 seconds (depends on image size)
- **Tweet Fetching**: ~1-2 seconds (TwexAPI)
- **Total Workflow**: ~10-20 seconds from input to posting

## Limitations ⚠️

- Twitter/X API access requires valid TwexAPI key
- OpenAI API has usage limits based on subscription
- Tesseract OCR works best with clear, readable text
- Replies are limited to 280 characters (Twitter/X limit)
- Language support depends on Tesseract language packs

## Contributing 🤝

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (when available)
python -m pytest

# Format code
black bot/ config/

# Lint code
pylint bot/ config/
```

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer ⚖️

This bot is for educational and personal use. Users are responsible for:
- Complying with X (Twitter) Terms of Service
- Respecting API rate limits and usage policies
- Using generated content responsibly
- Obtaining necessary permissions before posting

## Support 💬

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include relevant logs and error messages
4. Provide steps to reproduce the issue

## Roadmap 🗺️

Planned features for future releases:
- [ ] Web dashboard for bot management
- [ ] Database for storing generated replies
- [ ] Advanced analytics and statistics
- [ ] Batch reply generation
- [ ] Custom style templates
- [ ] Multi-language support expansion
- [ ] Reply scheduling
- [ ] Integration with other social platforms

## Credits 👏

Built with:
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [OpenAI Python Library](https://github.com/openai/openai-python)
- [TwexAPI](https://twexapi.io)
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract)

---

**Made with ❤️ for Twitter/X enthusiasts**
