#!/usr/bin/env python3
"""
X Reply Bot - Main entry point.
Telegram bot for generating customizable replies to X (Twitter) posts.
"""

import asyncio
import logging
import sys

from config.settings import settings
from telegram_handler import run_bot

logger = logging.getLogger(__name__)


def main() -> None:
    """Main entry point for the bot."""
    try:
        # Validate settings
        settings.validate()

        # Run bot
        asyncio.run(run_bot())

    except ValueError as e:
        print(f"Configuration Error: {str(e)}", file=sys.stderr)
        print("Please set all required environment variables and try again.", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nBot stopped by user.", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Fatal Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
