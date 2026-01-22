"""Client wrapper for instaloader to fetch Instagram posts and reels."""

import asyncio
import os
from typing import Any

import instaloader
from instaloader import Post
from instaloader.exceptions import (
    ConnectionException,
    InstaloaderException,
    LoginRequiredException,
    ProfileNotExistsException,
)

from .url_parser import extract_shortcode


class InstaloaderClient:
    """Wrapper around instaloader for fetching Instagram content."""

    def __init__(self, cookie_file: str | None = None):
        """
        Initialize the Instaloader client.

        Args:
            cookie_file: Optional path to cookie file for authenticated sessions
        """
        self.loader = instaloader.Instaloader()
        self.cookie_file = cookie_file
        self._session_loaded = False

        # Load session from cookie file if provided
        if cookie_file and os.path.exists(cookie_file):
            try:
                # Try to load session from file
                # instaloader expects session files in a specific format
                # For now, we'll handle this in a basic way
                # In practice, users would need to export cookies in instaloader format
                self._load_session(cookie_file)
            except Exception:
                # If loading fails, continue without authentication
                pass

    def _load_session(self, cookie_file: str) -> None:
        """
        Load session from cookie file.

        Note: Instaloader expects session files in its own format, typically
        created by running `instaloader --login username`. The cookie_file
        path should point to a directory containing session files, or we
        can use instaloader's context.load_session_from_file() method.

        For now, this is a placeholder. Full implementation would:
        1. Parse the cookie file path to extract username
        2. Use instaloader's session loading mechanism
        3. Handle errors gracefully
        """
        # TODO: Implement proper session loading using instaloader's API
        # For now, session loading is handled by instaloader's context
        # when needed. The cookie_file should point to instaloader session directory.
        try:
            # If cookie_file is a directory, instaloader can load sessions from there
            # For now, we mark session as available if file/directory exists
            if os.path.exists(cookie_file):
                self._session_loaded = True
        except Exception:
            # If loading fails, continue without authentication
            self._session_loaded = False

    async def fetch_post(self, url_or_shortcode: str) -> dict[str, Any]:
        """
        Fetch an Instagram post by URL or shortcode.

        Args:
            url_or_shortcode: Instagram post URL or shortcode

        Returns:
            Dictionary with post data including text and metadata

        Raises:
            ValueError: If URL is invalid
            InstaloaderException: If post cannot be fetched
            LoginRequiredException: If authentication is required for private content
        """
        shortcode = extract_shortcode(url_or_shortcode)
        if not shortcode:
            raise ValueError(f"Invalid Instagram URL or shortcode: {url_or_shortcode}")

        # Run blocking instaloader operations in a thread pool
        def _fetch_post_sync():
            try:
                post = Post.from_shortcode(self.loader.context, shortcode)

                # Extract text content
                caption = post.caption if post.caption else ""

                return {
                    "shortcode": post.shortcode,
                    "text": caption,
                    "author": post.owner_username,
                    "timestamp": post.date_utc.isoformat() if post.date_utc else None,
                    "likes": post.likes,
                    "comments": post.comments,
                    "is_video": post.is_video,
                    "typename": post.typename,
                }
            except LoginRequiredException:
                raise LoginRequiredException(
                    "This post is private and requires authentication. "
                    "Please provide a valid session cookie file via COOKIE_FILE environment variable."
                ) from None
            except ProfileNotExistsException:
                raise ValueError(f"Post not found: {shortcode}") from None
            except ConnectionException as e:
                raise ConnectionException(
                    f"Network error while fetching post: {e!s}"
                ) from e
            except InstaloaderException as e:
                raise InstaloaderException(f"Error fetching post: {e!s}") from e

        # Run in executor to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch_post_sync)

    async def fetch_reel(self, url_or_shortcode: str) -> dict[str, Any]:
        """
        Fetch an Instagram reel by URL or shortcode.

        Note: Instagram reels are essentially posts with typename "GraphVideo".
        This method uses the same underlying logic as fetch_post.

        Args:
            url_or_shortcode: Instagram reel URL or shortcode

        Returns:
            Dictionary with reel data including text and metadata

        Raises:
            ValueError: If URL is invalid
            InstaloaderException: If reel cannot be fetched
            LoginRequiredException: If authentication is required for private content
        """
        # Reels are posts with video content, so we can use the same logic
        return await self.fetch_post(url_or_shortcode)
