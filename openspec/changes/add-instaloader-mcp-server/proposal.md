# Change: Add Instaloader MCP Server

## Why
There is a need for a Model Context Protocol (MCP) server that can fetch Instagram posts and reels and extract their text content as JSON. This will enable AI assistants and other MCP clients to access Instagram content programmatically. The server should support both public and private content (with optional session cookies) and be containerized for easy deployment and version management.

## What Changes
- **NEW**: HTTP-based MCP server implementation using Python and FastMCP framework
- **NEW**: Integration with the `instaloader` Python module to fetch posts and reels
- **NEW**: URL parsing to extract shortcodes from full Instagram URLs
- **NEW**: Tool endpoint to extract text content from Instagram posts/reels and return as JSON
- **NEW**: Optional session/cookie support for accessing private content
- **NEW**: Update checking mechanism to detect available updates for the `instaloader` module (cached, refreshed once per day)
- **NEW**: Docker containerization with on-the-spot builds (no registry dependency)
- **NEW**: docker-compose.yml for easy setup and execution
- **NEW**: Test suite with example URL file (including "https://www.instagram.com/p/DRr-n4XER3x/", "https://www.instagram.com/p/DTDy4fMDCc4/", "https://www.instagram.com/p/DQUVv9kANPh/", and "https://www.instagram.com/p/DSNKaEZjIR9/")
- **NEW**: Comprehensive documentation for setup, usage, and API reference
- **NEW**: OpenSpec documentation updates for project conventions

## Impact
- Affected specs: All new capabilities (no existing specs to modify)
- Affected code: New codebase (no existing code to modify)
- Dependencies: Python 3.5+, UV package manager, `instaloader` module, FastMCP framework, Docker, docker-compose
- Deployment: New Docker container that can be built and run locally
