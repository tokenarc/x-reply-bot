# Deployment Guide 🚀

This guide covers deploying X Reply Bot to various platforms.

## Local Deployment

### Prerequisites
- Python 3.9+
- Tesseract OCR installed
- All API keys configured

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/x-reply-bot.git
cd x-reply-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run bot
python bot/main.py
```

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

# Install Tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run bot
CMD ["python", "bot/main.py"]
```

### Build and Run
```bash
# Build image
docker build -t x-reply-bot .

# Run container
docker run -d \
  -e TELEGRAM_BOT_TOKEN=your_token \
  -e TWEXAPI_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  --name x-reply-bot \
  x-reply-bot
```

## Cloud Deployment

### Heroku

1. **Create Procfile**
```
worker: python bot/main.py
```

2. **Deploy**
```bash
heroku create x-reply-bot
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set TWEXAPI_KEY=your_key
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

### Railway.app

1. **Connect GitHub repository**
2. **Add environment variables** in Railway dashboard
3. **Set start command**: `python bot/main.py`
4. **Deploy**

### PythonAnywhere

1. **Upload files** to PythonAnywhere
2. **Create virtual environment**
3. **Install dependencies**
4. **Create scheduled task** to run `python bot/main.py`

### AWS Lambda

Note: Lambda has limitations for long-running bots. Use EC2 or ECS instead.

### Google Cloud Run

1. **Create Dockerfile** (see above)
2. **Deploy**
```bash
gcloud run deploy x-reply-bot \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars TELEGRAM_BOT_TOKEN=your_token
```

## Environment Variables

Set these in your deployment platform:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TWEXAPI_KEY=your_twexapi_bearer_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o
LOG_LEVEL=INFO
```

## Monitoring

### Health Checks
```python
# Add periodic health check
async def health_check():
    # Verify API connections
    if not twex_client.validate_api_key():
        logger.error("TwexAPI key invalid")
    if not ai_generator.validate_api_key():
        logger.error("OpenAI key invalid")
```

### Logging
- Logs written to `bot.log`
- Set `LOG_LEVEL=DEBUG` for detailed logs
- Monitor logs for errors and warnings

### Uptime Monitoring
- Use services like UptimeRobot
- Monitor bot responsiveness
- Set up alerts for failures

## Scaling Considerations

### Single Instance
- Suitable for small to medium usage
- Simple deployment
- No load balancing needed

### Multiple Instances
- Use message queue (RabbitMQ, Redis)
- Distribute requests across instances
- Requires state management

### Database
- Store conversation history
- Track user preferences
- Cache generated replies

## Troubleshooting

### Bot Not Starting
```bash
# Check logs
tail -f bot.log

# Verify Python version
python --version

# Test imports
python -c "from bot.telegram_handler import TelegramBotHandler"
```

### API Connection Issues
```bash
# Test API connectivity
python -c "from bot.twex_client import TwexAPIClient; print(TwexAPIClient().validate_api_key())"
```

### Memory Issues
- Monitor memory usage
- Implement cleanup routines
- Use streaming for large responses

### Rate Limiting
- Implement request queuing
- Add delays between API calls
- Monitor API usage

## Security Best Practices

1. **Never commit secrets**
   - Use `.env` files
   - Add to `.gitignore`
   - Use environment variables in production

2. **API Key Rotation**
   - Rotate keys regularly
   - Use key versioning
   - Monitor key usage

3. **Input Validation**
   - Validate all user inputs
   - Sanitize text before processing
   - Check file sizes and formats

4. **Rate Limiting**
   - Implement per-user limits
   - Prevent abuse
   - Monitor suspicious activity

5. **Logging**
   - Log important events
   - Don't log sensitive data
   - Rotate log files

## Backup and Recovery

### Database Backup
```bash
# Backup SQLite database (if using)
cp bot.db bot.db.backup
```

### Configuration Backup
```bash
# Backup .env file (store securely)
cp .env .env.backup
```

### Code Backup
- Use Git for version control
- Tag releases
- Maintain backup branches

## Performance Optimization

### API Caching
```python
# Cache frequently accessed data
from functools import lru_cache

@lru_cache(maxsize=128)
def get_tweet(tweet_id):
    return twex_client.get_tweet(tweet_id)
```

### Batch Processing
- Process multiple requests together
- Reduce API calls
- Improve efficiency

### Async Operations
- Use async/await for I/O operations
- Improve responsiveness
- Handle more concurrent users

## Maintenance

### Regular Updates
```bash
# Check for dependency updates
pip list --outdated

# Update dependencies
pip install --upgrade -r requirements.txt
```

### Testing
```bash
# Run tests before deployment
python -m pytest

# Check code quality
pylint bot/ config/
```

### Monitoring
- Check bot responsiveness
- Monitor API usage
- Review error logs
- Track user metrics

## Support and Troubleshooting

For deployment issues:
1. Check logs for error messages
2. Verify all environment variables are set
3. Test API connectivity
4. Check firewall/network settings
5. Review platform-specific documentation

---

**Happy deploying! 🚀**
