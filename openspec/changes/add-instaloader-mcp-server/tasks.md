## 1. Project Setup
- [x] 1.1 Initialize Python project structure with UV (pyproject.toml)
- [x] 1.2 Set up FastMCP framework dependencies using UV
- [x] 1.3 Set up testing framework dependencies (pytest or similar) using UV
- [x] 1.4 Create project directory structure (src/, tests/, docs/, docker/)

## 2. MCP Server Implementation
- [x] 2.1 Implement HTTP transport MCP server using FastMCP (not just streamable)
- [x] 2.2 Set up JSON-RPC 2.0 message handling via FastMCP
- [x] 2.3 Implement MCP protocol initialization and capability negotiation
- [x] 2.4 Add error handling and proper JSON-RPC error responses
- [x] 2.5 Implement .env file support for configuration
- [x] 2.6 Configure HTTP port (default 3336, configurable via MCP_PORT in .env)

## 3. Instaloader Integration
- [x] 3.1 Implement URL parsing to extract shortcode from full Instagram URLs
- [x] 3.2 Support both full URLs and direct shortcode input
- [x] 3.3 Implement tool to fetch Instagram post by URL/shortcode
- [x] 3.4 Implement tool to fetch Instagram reel by URL/shortcode
- [x] 3.5 Extract text content (caption) from post/reel objects
- [x] 3.6 Format response as JSON with post metadata and text
- [x] 3.7 Add optional session/cookie support for private content
- [x] 3.8 Implement cookie file path configuration via COOKIE_FILE in .env
- [x] 3.9 Handle errors (private posts without auth, invalid URLs, network errors, invalid URL formats)

## 4. Update Checking Mechanism
- [x] 4.1 Implement function to check latest version of `instaloader` on PyPI
- [x] 4.2 Compare installed version with latest available version
- [x] 4.3 Implement caching mechanism that refreshes once per day
- [x] 4.4 Include update information in JSON responses (version status, latest version if available)

## 5. Docker Containerization
- [x] 5.1 Create Dockerfile with Python base image
- [x] 5.2 Install UV package manager in container
- [x] 5.3 Install dependencies including `instaloader` and FastMCP using UV
- [x] 5.4 Configure container to run MCP server on HTTP port
- [x] 5.5 Set up build process that doesn't require external registry
- [x] 5.6 Create docker-compose.yml file with proper configuration
- [x] 5.7 Configure docker-compose to use .env file for environment variables
- [x] 5.8 Set up volume mounts for cookie file (if needed)

## 6. Documentation
- [x] 6.1 Write README.md with project overview and quick start
- [x] 6.2 Document API endpoints and tool definitions
- [x] 6.3 Document session/cookie setup for private content
- [x] 6.4 Document .env configuration (MCP_PORT, COOKIE_FILE)
- [x] 6.5 Document Docker build and run instructions
- [x] 6.6 Document docker-compose setup and usage
- [x] 6.7 Add example requests and responses
- [x] 6.8 Document update checking mechanism (daily cache refresh)

## 7. OpenSpec Documentation
- [x] 7.1 Update openspec/project.md with project context, tech stack, and conventions
- [x] 7.2 Document Python code style preferences
- [x] 7.3 Document testing strategy
- [x] 7.4 Document deployment and Docker conventions

## 8. Testing & Validation
- [x] 8.1 Create example test file (tests/example_urls.txt) with at least:
  - "https://www.instagram.com/p/DRr-n4XER3x/"
  - "https://www.instagram.com/p/DTDy4fMDCc4/"
  - "https://www.instagram.com/p/DQUVv9kANPh/"
  - "https://www.instagram.com/p/DSNKaEZjIR9/"
- [x] 8.2 Implement test runner that reads URLs from example file
- [x] 8.3 Implement test cases that fetch posts/reels and verify text extraction
- [x] 8.4 Test fetching public posts without authentication
- [x] 8.5 Test fetching public reels without authentication
- [x] 8.6 Test fetching private posts with session cookies
- [x] 8.7 Test error handling (invalid URLs, network failures)
- [x] 8.8 Test update checking mechanism
- [x] 8.9 Test Docker build and container execution
- [x] 8.10 Validate MCP protocol compliance
- [x] 8.11 Ensure tests can run both locally and in Docker container
