"""
Utility functions for X Reply Bot.
"""

import logging
import os
import re
from pathlib import Path
from typing import Optional

import requests
from telegram import Update

logger = logging.getLogger(__name__)


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("bot.log"),
            logging.StreamHandler(),
        ],
    )


def download_file(url: str, file_path: str, timeout: int = 30) -> bool:
    """
    Download file from URL.

    Args:
        url: URL to download from
        file_path: Path to save file
        timeout: Request timeout in seconds

    Returns:
        True if download successful, False otherwise
    """
    try:
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        logger.info(f"Successfully downloaded file to {file_path}")
        return True

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download file: {str(e)}")
        return False


def cleanup_file(file_path: str) -> None:
    """
    Delete a file if it exists.

    Args:
        file_path: Path to file to delete
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.debug(f"Cleaned up file: {file_path}")
    except Exception as e:
        logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")


def extract_url_from_text(text: str) -> Optional[str]:
    """
    Extract first URL from text.

    Args:
        text: Text containing URL

    Returns:
        URL if found, None otherwise
    """
    url_pattern = r"https?://(?:www\.)?(?:twitter|x)\.com/\S+"
    match = re.search(url_pattern, text)
    return match.group(0) if match else None


def format_tweet_text(text: str, max_length: int = 280) -> str:
    """
    Format tweet text to fit within character limit.

    Args:
        text: Tweet text
        max_length: Maximum character length (default: 280)

    Returns:
        Formatted text
    """
    if len(text) <= max_length:
        return text

    # Truncate and add ellipsis
    return text[: max_length - 3] + "..."


def validate_tweet_text(text: str) -> bool:
    """
    Validate tweet text.

    Args:
        text: Tweet text to validate

    Returns:
        True if valid, False otherwise
    """
    if not text or not isinstance(text, str):
        return False

    text = text.strip()
    if len(text) == 0 or len(text) > 280:
        return False

    return True


def get_user_mention(update: Update) -> str:
    """
    Get user mention from Telegram update.

    Args:
        update: Telegram update object

    Returns:
        User mention string (name or ID)
    """
    user = update.effective_user
    if user.first_name:
        return user.first_name
    return f"User {user.id}"


def create_temp_dir(base_path: str = "/tmp") -> str:
    """
    Create a temporary directory for bot operations.

    Args:
        base_path: Base path for temp directory

    Returns:
        Path to created temp directory
    """
    import tempfile

    temp_dir = tempfile.mkdtemp(prefix="x_reply_bot_", dir=base_path)
    logger.debug(f"Created temp directory: {temp_dir}")
    return temp_dir


def cleanup_temp_dir(temp_dir: str) -> None:
    """
    Recursively delete a temporary directory.

    Args:
        temp_dir: Path to temp directory
    """
    try:
        import shutil

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            logger.debug(f"Cleaned up temp directory: {temp_dir}")
    except Exception as e:
        logger.warning(f"Failed to cleanup temp directory {temp_dir}: {str(e)}")


def truncate_text(text: str, max_length: int = 1000, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
