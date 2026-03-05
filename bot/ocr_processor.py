"""
OCR processor for extracting text from images using Tesseract.
"""

import logging
import os
from pathlib import Path
from typing import Optional

from PIL import Image

from config.settings import settings

# Configure pytesseract path if specified
if settings.TESSERACT_PATH:
    import pytesseract

    pytesseract.pytesseract.pytesseract_cmd = settings.TESSERACT_PATH
else:
    import pytesseract

logger = logging.getLogger(__name__)


class OCRProcessor:
    """Process images and extract text using Tesseract OCR."""

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
        try:
            # Check file exists
            if not os.path.exists(file_path):
                logger.error(f"Image file not found: {file_path}")
                return False

            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > OCRProcessor.MAX_IMAGE_SIZE:
                logger.error(f"Image file too large: {file_size} bytes")
                return False

            # Check format
            if not OCRProcessor.is_supported_format(file_path):
                logger.error(f"Unsupported image format: {file_path}")
                return False

            # Try to open and verify it's a valid image
            with Image.open(file_path) as img:
                img.verify()

            return True

        except Exception as e:
            logger.error(f"Image validation failed: {str(e)}")
            return False

    @staticmethod
    def extract_text(image_path: str, language: str = "eng") -> Optional[str]:
        """
        Extract text from image using Tesseract OCR.

        Args:
            image_path: Path to image file
            language: Tesseract language code (default: 'eng' for English)

        Returns:
            Extracted text or None if extraction failed
        """
        try:
            # Validate image file
            if not OCRProcessor.validate_image_file(image_path):
                return None

            # Open and preprocess image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Extract text using Tesseract
                text = pytesseract.image_to_string(img, lang=language)

                # Clean up extracted text
                text = OCRProcessor._clean_text(text)

                if text:
                    logger.info(f"Successfully extracted {len(text)} characters from image")
                    return text
                else:
                    logger.warning("No text found in image")
                    return None

        except pytesseract.TesseractNotFoundError:
            logger.error(
                "Tesseract not installed. Install with: sudo apt-get install tesseract-ocr"
            )
            return None
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
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
        Get Tesseract language code from language name.

        Args:
            language_name: Language name (e.g., 'english', 'urdu', 'japanese')

        Returns:
            Tesseract language code
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
