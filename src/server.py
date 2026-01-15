"""FastMCP server for Instagram content fetching."""

import os
from typing import Optional
from dotenv import load_dotenv
from fastmcp import FastMCP

from .instaloader_client import InstaloaderClient
from .url_parser import extract_shortcode, is_valid_instagram_url
from .update_checker import check_for_updates
from instaloader.exceptions import (
    LoginRequiredException,
    InstaloaderException,
)

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Instaloader MCP Server")

# Get configuration from environment
MCP_PORT = int(os.getenv("MCP_PORT", "3336"))
COOKIE_FILE = os.getenv("COOKIE_FILE")

# Initialize instaloader client
instaloader_client = InstaloaderClient(cookie_file=COOKIE_FILE)


@mcp.tool()
async def fetch_instagram_post(url: str) -> dict:
    """
    Fetch an Instagram post by URL or shortcode and return its text content as JSON.
    
    Args:
        url: Instagram post URL (e.g., "https://www.instagram.com/p/DRr-n4XER3x/") 
             or shortcode (e.g., "DRr-n4XER3x")
    
    Returns:
        Dictionary containing:
        - text: Post caption/text content
        - shortcode: Post shortcode
        - author: Author username
        - timestamp: Post timestamp (ISO format)
        - likes: Number of likes
        - comments: Number of comments
        - is_video: Whether post is a video
        - update_info: Instaloader version update information
    """
    try:
        # Validate URL format
        if not is_valid_instagram_url(url):
            return {
                "error": "Invalid Instagram URL format",
                "url": url,
            }
        
        # Fetch post data
        post_data = await instaloader_client.fetch_post(url)
        
        # Get update information
        update_info = await check_for_updates()
        
        # Combine post data with update info
        return {
            **post_data,
            "update_info": update_info,
        }
    except LoginRequiredException as e:
        return {
            "error": "Authentication required",
            "message": str(e),
            "url": url,
        }
    except ValueError as e:
        return {
            "error": "Invalid URL or post not found",
            "message": str(e),
            "url": url,
        }
    except InstaloaderException as e:
        return {
            "error": "Error fetching post",
            "message": str(e),
            "url": url,
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "message": str(e),
            "url": url,
        }


@mcp.tool()
async def fetch_instagram_reel(url: str) -> dict:
    """
    Fetch an Instagram reel by URL or shortcode and return its text content as JSON.
    
    Args:
        url: Instagram reel URL (e.g., "https://www.instagram.com/reel/ABC123/") 
             or shortcode (e.g., "ABC123")
    
    Returns:
        Dictionary containing:
        - text: Reel caption/text content
        - shortcode: Reel shortcode
        - author: Author username
        - timestamp: Reel timestamp (ISO format)
        - likes: Number of likes
        - comments: Number of comments
        - is_video: Always True for reels
        - update_info: Instaloader version update information
    """
    try:
        # Validate URL format
        if not is_valid_instagram_url(url):
            return {
                "error": "Invalid Instagram URL format",
                "url": url,
            }
        
        # Fetch reel data (reels are posts with video content)
        reel_data = await instaloader_client.fetch_reel(url)
        
        # Get update information
        update_info = await check_for_updates()
        
        # Combine reel data with update info
        return {
            **reel_data,
            "update_info": update_info,
        }
    except LoginRequiredException as e:
        return {
            "error": "Authentication required",
            "message": str(e),
            "url": url,
        }
    except ValueError as e:
        return {
            "error": "Invalid URL or reel not found",
            "message": str(e),
            "url": url,
        }
    except InstaloaderException as e:
        return {
            "error": "Error fetching reel",
            "message": str(e),
            "url": url,
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "message": str(e),
            "url": url,
        }


if __name__ == "__main__":
    # Run the server with HTTP transport
    mcp.run(transport="http", host="0.0.0.0", port=MCP_PORT)
