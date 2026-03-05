# Contributing to X Reply Bot 🤝

Thank you for your interest in contributing to X Reply Bot! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Report issues responsibly

## Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub
git clone https://github.com/your-username/x-reply-bot.git
cd x-reply-bot
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or for bug fixes:
git checkout -b fix/bug-description
```

### 3. Set Up Development Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Development Guidelines

### Code Style
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

### Commit Messages
```
[Type] Brief description

Detailed explanation of changes (if needed)

- Bullet point for specific changes
- Another bullet point
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
[feat] Add support for custom reply templates
[fix] Handle OCR errors for low-quality images
[docs] Update installation instructions
```

### Pull Request Process

1. **Update your fork**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Make your changes**
   - Keep changes focused and related
   - Write clear commit messages
   - Add comments for complex logic

3. **Test your changes**
   ```bash
   # Run tests (when available)
   python -m pytest
   
   # Check code style
   pylint bot/ config/
   black --check bot/ config/
   ```

4. **Create Pull Request**
   - Provide clear title and description
   - Reference related issues
   - Include before/after examples if applicable
   - Ensure all tests pass

## Areas for Contribution

### Bug Fixes
- Report bugs with detailed reproduction steps
- Include error messages and logs
- Suggest fixes if possible

### Features
- Suggest new features in issues first
- Discuss implementation approach
- Follow existing code patterns

### Documentation
- Improve README and guides
- Add code examples
- Fix typos and clarifications
- Add API documentation

### Tests
- Write unit tests for new features
- Improve test coverage
- Test edge cases

## Project Structure

```
bot/
├── main.py                 # Entry point
├── telegram_handler.py      # Telegram integration
├── twex_client.py           # X API wrapper
├── ai_generator.py          # ChatGPT-4o integration
├── ocr_processor.py         # Tesseract OCR
└── utils.py                 # Utilities

config/
├── settings.py              # Configuration
└── constants.py             # Constants and enums
```

## Key Components

### TwexAPI Client (`bot/twex_client.py`)
- Handles X API communication
- Methods: `get_tweet()`, `post_reply()`, `post_tweet()`
- Uses Bearer token authentication

### AI Generator (`bot/ai_generator.py`)
- Generates replies using ChatGPT-4o
- Supports multiple styles and languages
- Returns list of reply options

### OCR Processor (`bot/ocr_processor.py`)
- Extracts text from images
- Validates image files
- Supports 100+ languages

### Telegram Handler (`bot/telegram_handler.py`)
- Manages bot interactions
- Implements conversation flow
- Handles user commands

## Testing

When adding new features:
1. Test with real API calls (use test accounts)
2. Test error handling
3. Test edge cases
4. Verify logging output

Example test approach:
```python
# Test with different input types
test_inputs = [
    "https://twitter.com/user/status/123456",  # URL
    "Plain tweet text",                          # Text
    # Image file (screenshot)
]

for test_input in test_inputs:
    result = handler.handle_input(test_input)
    assert result is not None
```

## Documentation

When adding features, update:
1. **README.md** - Add feature description
2. **Code comments** - Explain complex logic
3. **Docstrings** - Document functions and classes
4. **RESEARCH.md** - Update architecture notes

Example docstring:
```python
def generate_replies(
    self,
    tweet_text: str,
    style: ReplyStyle,
    language: Language,
) -> Optional[List[str]]:
    """
    Generate multiple reply options for a tweet.
    
    Args:
        tweet_text: Original tweet text
        style: Reply style (GenZ, professional, etc.)
        language: Target language for reply
    
    Returns:
        List of generated replies or None if failed
    """
```

## Common Issues & Solutions

### Import Errors
```python
# Ensure config is in Python path
import sys
sys.path.insert(0, '/path/to/x-reply-bot')
from config import settings
```

### API Key Issues
- Check `.env` file exists
- Verify no extra whitespace in keys
- Ensure keys are current and valid

### Tesseract Not Found
```bash
# Install and set path
export TESSERACT_PATH=/usr/bin/tesseract
# Or add to .env file
```

## Release Process

1. Update version in `bot/__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release with notes

## Questions?

- Check existing issues and discussions
- Create a new issue with `[Question]` prefix
- Join our community discussions
- Contact maintainers

## Recognition 🏆

Contributors will be:
- Listed in README.md
- Credited in release notes
- Acknowledged in commit history

Thank you for making X Reply Bot better! 🙏
