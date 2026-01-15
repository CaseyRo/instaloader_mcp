# Project Context

## Purpose
This project provides a Model Context Protocol (MCP) server that enables AI assistants and other MCP clients to fetch Instagram posts and reels programmatically, extracting their text content as JSON. The server supports both public and private content (with optional session cookies) and is fully containerized for easy deployment.

## Tech Stack
- **Python 3.10+**: Core language
- **FastMCP**: MCP server framework with HTTP transport support
- **instaloader**: Python module for fetching Instagram content
- **UV**: Fast Python package manager (replaces pip)
- **Docker & docker-compose**: Containerization and orchestration
- **pytest**: Testing framework
- **python-dotenv**: Environment variable management

## Project Conventions

### Code Style
- Follow PEP 8 Python style guidelines
- Use type hints for function parameters and return types
- Maximum line length: 100 characters (where practical)
- Use descriptive variable and function names
- Docstrings for all public functions and classes (Google style)

### Architecture Patterns
- Modular design: Separate concerns (URL parsing, instaloader client, update checking, server)
- Async/await for I/O operations (HTTP requests, file operations)
- Dependency injection: Pass dependencies as constructor parameters where appropriate
- Error handling: Use specific exceptions and return structured error responses

### Testing Strategy
- Unit tests for utility functions (URL parser, update checker)
- Integration tests for main functionality (fetching posts/reels)
- Test file (`tests/example_urls.txt`) contains example URLs for testing
- Tests should handle network failures gracefully (skip if network unavailable)
- Run tests with: `pytest tests/`

### Git Workflow
- Main branch: `main`
- Feature branches: `feature/description`
- Commit messages: Use conventional commits format
- PR required for main branch merges

## Domain Context
- **Instagram Content**: Posts (images/videos) and Reels (short videos)
- **Shortcodes**: Unique identifiers for Instagram posts/reels (e.g., "DRr-n4XER3x")
- **MCP Protocol**: Model Context Protocol for connecting LLMs with external tools/resources
- **FastMCP**: Modern Python framework for building MCP servers with HTTP transport
- **Session Cookies**: Required for accessing private Instagram accounts/posts

## Important Constraints
- **Rate Limiting**: Instagram may rate limit requests - implement appropriate error handling
- **Private Content**: Requires valid session cookies from authenticated Instagram session
- **Network Dependency**: Requires internet connection to fetch Instagram content
- **Python Version**: Requires Python 3.10+ (for FastMCP and modern async features)
- **UV Package Manager**: Project uses UV instead of pip for faster dependency management

## External Dependencies
- **FastMCP**: MCP server framework (PyPI)
- **instaloader**: Instagram content fetching library (PyPI)
- **PyPI API**: For checking `instaloader` version updates
- **Instagram**: External service (rate limits may apply)
- **Docker**: For containerization (optional, for local development)
