"""
OCR processor for extracting text from images.

NOTE: OCR functionality has been disabled for Cloudflare Workers compatibility.
Pillow and pytesseract are not compatible with Cloudflare Workers environment.

For image processing, consider these alternatives:
1. Use client-side OCR with tesseract.js in the web client
2. Send images to external OCR API (Google Vision, AWS Textract, etc.)
3. Ask users to provide tweet text directly instead of screenshots
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class OCRProcessor:
    """
    OCR processor stub - OCR functionality disabled.
    
    This class provides the same interface as the original OCR processor
    but returns None to indicate OCR is not available.
    """

    # Supported image formats
    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

    # Maximum image size (10MB)
    MAX_IMAGE_SIZE = 10 * 1024 * 1024

    @staticmethod
    def is_supported_format(file_path: str) -> bool:
        """
        Check if file format is supported for OCR.

        Args:
            file_path: Path to image file

        Returns:
            True if format is supported, False otherwise
        """
        suffix = Path(file_path).suffix.lower()
        return suffix in OCRProcessor.SUPPORTED_FORMATS

    @staticmethod
    def validate_image_file(file_path: str) -> bool:
        """
        Validate image file before processing.

        Args:
            file_path: Path to image file

        Returns:
            True if file is valid, False otherwise
        """
        logger.warning(
            "OCR functionality is disabled. Image validation skipped."
        )
        return False

    @staticmethod
    def extract_text(image_path: str, language: str = "eng") -> Optional[str]:
        """
        Extract text from image using OCR.

        NOTE: This method is disabled and always returns None.
        
        OCR functionality requires Pillow and pytesseract, which are not
        compatible with Cloudflare Workers. To process images:

        1. Use client-side OCR with tesseract.js in your web application
        2. Send images to an external OCR API service
        3. Ask users to provide tweet text directly instead of screenshots

        Args:
            image_path: Path to image file
            language: Language code (default: 'eng' for English)

        Returns:
            None - OCR is disabled
        """
        logger.warning(
            "OCR extraction requested but OCR is disabled for Cloudflare Workers compatibility. "
            "Please use alternative methods to extract text from images."
        )
        return None

    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean extracted text by removing extra whitespace and normalizing.

        Args:
            text: Raw extracted text

        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        lines = [line.strip() for line in text.split("\n")]
        lines = [line for line in lines if line]  # Remove empty lines
        text = " ".join(lines)

        # Remove multiple spaces
        while "  " in text:
            text = text.replace("  ", " ")

        return text.strip()

    @staticmethod
    def get_language_code(language_name: str) -> str:
        """
        Get language code from language name.

        Args:
            language_name: Language name (e.g., 'english', 'urdu', 'japanese')

        Returns:
            Language code
        """
        language_map = {
            "english": "eng",
            "urdu": "urd",
            "japanese": "jpn",
            "spanish": "spa",
            "french": "fra",
            "german": "deu",
            "chinese": "chi_sim",
            "hindi": "hin",
            "portuguese": "por",
            "russian": "rus",
        }
        return language_map.get(language_name.lower(), "eng")
