"""
AI reply generator using OpenAI ChatGPT-4o.
"""

import json
import logging
from typing import List, Optional

from openai import OpenAI

from config.constants import (
    LANGUAGE_INSTRUCTIONS,
    STYLE_PROMPTS,
    Language,
    ReplyLength,
    ReplyStyle,
)
from config.settings import settings

logger = logging.getLogger(__name__)


class AIGenerator:
    """Generate replies using OpenAI ChatGPT-4o."""

    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def generate_replies(
        self,
        tweet_text: str,
        style: ReplyStyle,
        length: ReplyLength,
        language: Language,
        num_replies: int = 3,
        custom_word_count: Optional[int] = None,
    ) -> Optional[List[str]]:
        """
        Generate multiple reply options for a tweet.

        Args:
            tweet_text: Original tweet text
            style: Reply style (GenZ, professional, casual, sarcastic, motivational)
            length: Reply length (short, medium, long, custom)
            language: Language for reply
            num_replies: Number of reply options to generate (default: 3)
            custom_word_count: Custom word count if length is 'custom'

        Returns:
            List of generated replies or None if generation failed
        """
        try:
            # Determine word count range
            if length == ReplyLength.CUSTOM and custom_word_count:
                word_range = (custom_word_count - 5, custom_word_count + 5)
            else:
                word_range = ReplyLength.get_word_range(length)

            # Build system prompt
            system_prompt = self._build_system_prompt(
                style, language, word_range, num_replies
            )

            # Build user message
            user_message = f"Generate {num_replies} different reply options for this tweet:\n\n\"{tweet_text}\"\n\nRespond with a JSON array of strings, each being a complete reply."

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                max_tokens=2000,
            )

            # Parse response
            response_text = response.choices[0].message.content
            replies = self._parse_replies(response_text)

            if replies:
                logger.info(f"Generated {len(replies)} replies successfully")
                return replies
            else:
                logger.warning("Failed to parse generated replies")
                return None

        except Exception as e:
            logger.error(f"Error generating replies: {str(e)}")
            return None

    def _build_system_prompt(
        self,
        style: ReplyStyle,
        language: Language,
        word_range: tuple,
        num_replies: int,
    ) -> str:
        """
        Build system prompt for reply generation.

        Args:
            style: Reply style
            language: Target language
            word_range: (min_words, max_words) tuple
            num_replies: Number of replies to generate

        Returns:
            System prompt string
        """
        style_instruction = STYLE_PROMPTS.get(
            style, "Write a helpful and engaging reply."
        )
        language_instruction = LANGUAGE_INSTRUCTIONS.get(
            language, "Respond in English."
        )

        prompt = f"""You are an expert social media reply writer. Your task is to generate engaging and authentic replies to tweets.

{style_instruction}

{language_instruction}

Requirements:
- Generate exactly {num_replies} different reply options
- Each reply should be between {word_range[0]} and {word_range[1]} words
- Replies should be authentic and conversational
- Avoid generic or repetitive responses
- Each reply should have a unique perspective or angle
- Keep replies within Twitter/X character limits (280 characters max)
- Return ONLY a valid JSON array of strings, nothing else

Example format:
["reply 1", "reply 2", "reply 3"]"""

        return prompt

    @staticmethod
    def _parse_replies(response_text: str) -> Optional[List[str]]:
        """
        Parse JSON array of replies from response.

        Args:
            response_text: Raw response text from API

        Returns:
            List of replies or None if parsing failed
        """
        try:
            # Try to extract JSON array from response
            # Sometimes the model might include extra text
            start_idx = response_text.find("[")
            end_idx = response_text.rfind("]") + 1

            if start_idx == -1 or end_idx == 0:
                logger.warning("No JSON array found in response")
                return None

            json_str = response_text[start_idx:end_idx]
            replies = json.loads(json_str)

            # Validate that we got a list of strings
            if isinstance(replies, list) and all(isinstance(r, str) for r in replies):
                # Filter out empty replies
                replies = [r.strip() for r in replies if r.strip()]
                return replies if replies else None

            logger.warning("Invalid reply format in response")
            return None

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error parsing replies: {str(e)}")
            return None

    def validate_api_key(self) -> bool:
        """
        Validate that the OpenAI API key is working.

        Returns:
            True if API key is valid, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
            )
            return response.choices[0].message.content is not None
        except Exception as e:
            logger.error(f"OpenAI API validation failed: {str(e)}")
            return False
