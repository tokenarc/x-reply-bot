# X Reply Bot - Research & Architecture

## TwexAPI Overview

**TwexAPI** is a cost-effective Twitter/X API wrapper that provides:
- **Pricing**: $0.01 per API call (90% cheaper than official API)
- **Rate Limits**: 20+ requests/second (vs 300/15min for official API)
- **Endpoints**:
  - `POST /twitter/tweets/lookup` - Fetch tweet details by ID
  - `POST /twitter/tweets/create` - Post tweets and replies
  - `GET /twitter/tweets/lookup` - Batch get tweets by ID

**Key Features**:
- Simple Bearer token authentication
- No complex OAuth flows
- Support for media, scheduling, and replies
- Real-time data access

## Architecture Plan

### Project Structure
```
x-reply-bot/
├── bot/                          # Core bot logic
│   ├── main.py                   # Entry point
│   ├── telegram_handler.py        # Telegram Bot API integration
│   ├── twex_client.py             # TwexAPI wrapper
│   ├── ai_generator.py            # ChatGPT-4o integration
│   ├── ocr_processor.py           # Tesseract OCR
│   ├── reply_styles.py            # Reply style templates
│   └── utils.py                   # Helper functions
├── config/
│   ├── settings.py                # Configuration management
│   └── constants.py               # Constants and enums
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── README.md                      # Documentation
└── LICENSE                        # MIT License
```

### Technology Stack
- **Telegram**: python-telegram-bot library
- **X API**: TwexAPI (REST API via requests)
- **AI**: OpenAI ChatGPT-4o API
- **OCR**: Tesseract OCR via pytesseract
- **Language**: Python 3.9+

### Workflow
1. User sends `/reply` command with text, link, or image
2. Bot processes input:
   - Text: Use directly
   - Link: Extract tweet ID and fetch via TwexAPI
   - Image: Run Tesseract OCR to extract text
3. Bot prompts user for:
   - Reply style (GenZ, professional, casual, sarcastic, motivational)
   - Length (short, medium, long, custom word count)
   - Language (English, Urdu, Japanese, etc.)
4. Send to ChatGPT-4o with all parameters
5. Generate multiple reply options
6. Display options in Telegram
7. User selects one to post back to X via TwexAPI

### Key Components

#### Telegram Handler
- `/start` - Initialize bot
- `/reply` - Main command to generate replies
- Button callbacks for style/length selection
- Reply option selection and posting

#### TwexAPI Client
- Fetch tweet by URL or ID
- Post reply to tweet
- Handle authentication and errors

#### AI Generator
- System prompt with style and language context
- Generate multiple reply variations
- Validate response format

#### OCR Processor
- Download image from Telegram
- Run Tesseract OCR
- Clean and validate extracted text

#### Reply Styles
- GenZ: Casual, trendy, emoji-heavy
- Professional: Formal, business-appropriate
- Casual: Friendly, conversational
- Sarcastic: Witty, ironic tone
- Motivational: Inspirational, uplifting

## Dependencies
- `python-telegram-bot` - Telegram Bot API
- `requests` - HTTP client for TwexAPI
- `openai` - ChatGPT-4o integration
- `pytesseract` - OCR wrapper
- `Pillow` - Image processing
- `python-dotenv` - Environment variables
- `pydantic` - Data validation

## Environment Variables
- `TELEGRAM_BOT_TOKEN` - Telegram Bot API token
- `TWEXAPI_KEY` - TwexAPI bearer token
- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_MODEL` - Model name (gpt-4o)
- `TESSERACT_PATH` - Path to Tesseract binary (optional)

## Next Steps
1. Set up project structure
2. Implement core modules
3. Test each component
4. Create comprehensive documentation
5. Push to GitHub
