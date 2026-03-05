"""
TwexAPI client for fetching tweets and posting replies.
Wrapper around TwexAPI REST endpoints.
"""

import logging
import re
from typing import Optional

import requests

from config.settings import settings

logger = logging.getLogger(__name__)


class TwexAPIClient:
    """Client for interacting with TwexAPI."""

    def __init__(self):
        """Initialize TwexAPI client with authentication."""
        self.base_url = settings.TWEXAPI_BASE_URL
        self.api_key = settings.TWEXAPI_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.timeout = settings.REQUEST_TIMEOUT

    @staticmethod
    def extract_tweet_id(url: str) -> Optional[str]:
        """
        Extract tweet ID from Twitter/X URL.

        Args:
            url: Twitter/X URL (e.g., https://twitter.com/user/status/1234567890)

        Returns:
            Tweet ID if found, None otherwise
        """
        # Pattern for standard tweet URLs
        patterns = [
            r"(?:twitter|x)\.com/\w+/status/(\d+)",  # Standard URL
            r"t\.co/\w+",  # Shortened URL (would need to follow redirect)
            r"^(\d+)$",  # Direct ID
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    def get_tweet(self, tweet_id: str) -> Optional[dict]:
        """
        Fetch tweet details by ID.

        Args:
            tweet_id: Twitter tweet ID

        Returns:
            Tweet data dictionary or None if failed
        """
        try:
            url = f"{self.base_url}/twitter/tweets/lookup"
            payload = [tweet_id]

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            if data.get("code") == 200 and data.get("data"):
                return data["data"][0]

            logger.warning(f"Failed to fetch tweet {tweet_id}: {data.get('msg')}")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching tweet {tweet_id}: {str(e)}")
            return None

    def post_reply(
        self, tweet_id: str, reply_text: str, media_url: Optional[str] = None
    ) -> Optional[str]:
        """
        Post a reply to a tweet.

        Args:
            tweet_id: ID of tweet to reply to
            reply_text: Text content of the reply
            media_url: Optional URL of image to attach

        Returns:
            Posted tweet ID if successful, None otherwise
        """
        try:
            url = f"{self.base_url}/twitter/tweets/create"
            payload = {
                "tweet_content": reply_text,
                "reply_tweet_id": tweet_id,
            }

            if media_url:
                payload["media_url"] = media_url

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            if data.get("code") == 200 and data.get("data"):
                posted_id = data["data"].get("tweet_id")
                logger.info(f"Successfully posted reply: {posted_id}")
                return posted_id

            logger.warning(f"Failed to post reply: {data.get('msg')}")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting reply: {str(e)}")
            return None

    def post_tweet(
        self, tweet_text: str, media_url: Optional[str] = None
    ) -> Optional[str]:
        """
        Post a standalone tweet.

        Args:
            tweet_text: Text content of the tweet
            media_url: Optional URL of image to attach

        Returns:
            Posted tweet ID if successful, None otherwise
        """
        try:
            url = f"{self.base_url}/twitter/tweets/create"
            payload = {"tweet_content": tweet_text}

            if media_url:
                payload["media_url"] = media_url

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            if data.get("code") == 200 and data.get("data"):
                posted_id = data["data"].get("tweet_id")
                logger.info(f"Successfully posted tweet: {posted_id}")
                return posted_id

            logger.warning(f"Failed to post tweet: {data.get('msg')}")
            return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting tweet: {str(e)}")
            return None

    def validate_api_key(self) -> bool:
        """
        Validate that the API key is working.

        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Try a simple request to validate the key
            url = f"{self.base_url}/twitter/tweets/lookup"
            response = requests.post(
                url,
                headers=self.headers,
                json=["1"],  # Dummy tweet ID
                timeout=self.timeout,
            )
            # Even if tweet doesn't exist, if we get a proper response, key is valid
            return response.status_code in [200, 422]

        except requests.exceptions.RequestException:
            return False
