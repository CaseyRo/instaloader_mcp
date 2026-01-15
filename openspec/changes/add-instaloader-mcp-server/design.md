## Context
This change introduces a new MCP server that wraps the `instaloader` Python module to provide Instagram content access via the Model Context Protocol. The server must support HTTP transport (not just stdio), handle both public and private content, and be containerized for easy deployment.

## Goals / Non-Goals

### Goals
- Provide HTTP-based MCP server (not just streamable)
- Fetch Instagram posts and reels and extract text content
- Support optional session cookies for private content
- Containerize the entire solution in Docker
- Enable on-the-spot Docker builds without registry dependency
- Include update checking for the `instaloader` module
- Create comprehensive documentation

### Non-Goals
- Downloading media files (images/videos) - only text extraction
- Supporting other Instagram content types (stories, highlights) in initial version
- Providing authentication/login functionality (only session cookie support)
- Supporting stdio transport (HTTP only)
- Building a web UI or dashboard
- Batch operations (multiple posts/reels in one request)
- Response caching (limited use case for current requirements)

## Decisions

### Decision: HTTP Transport Only
**What**: Implement MCP server using HTTP transport only, not stdio.
**Why**: User explicitly requested HTTP transport. HTTP allows for better scalability and can be accessed from multiple clients.
**Alternatives considered**: 
- stdio transport: Rejected - user requirement specifies HTTP
- Both transports: Rejected - adds complexity, HTTP-only is sufficient for initial version

### Decision: JSON Response Format
**What**: Return post/reel text content as JSON with metadata.
**Why**: MCP protocol uses JSON-RPC 2.0, and JSON format is standard for API responses. Including metadata provides additional context.
**Alternatives considered**:
- Plain text only: Rejected - loses valuable metadata (post ID, author, timestamp)
- XML: Rejected - JSON is standard for modern APIs

### Decision: Optional Session Support
**What**: Make session/cookie authentication optional, only required for private posts.
**Why**: Public posts don't require authentication, reducing friction for common use cases. Private content access is still supported when needed.
**Alternatives considered**:
- Always require authentication: Rejected - unnecessary for public content
- No authentication support: Rejected - needed for private posts

### Decision: Docker Build On-The-Spot
**What**: Build Docker images locally without requiring external registry.
**Why**: User requirement specifies building on the spot for easy rebuilds on updated versions. This simplifies development and deployment workflow.
**Alternatives considered**:
- Use pre-built images from registry: Rejected - user requirement
- Multi-stage builds with caching: Accepted - improves build performance while maintaining on-the-spot capability

### Decision: Update Checking via PyPI API
**What**: Check for `instaloader` updates by querying PyPI API and comparing with installed version. Cache results and refresh once per day.
**Why**: PyPI provides a standard API for version checking. Including update info in responses helps users stay current. UV installs packages from PyPI, so PyPI remains the canonical source for version information. Caching with daily refresh reduces API calls while keeping information reasonably current.
**Alternatives considered**:
- Manual version checking: Rejected - not automated
- GitHub releases API: Rejected - PyPI is the canonical source for Python packages (used by both pip and UV)
- Hourly cache refresh: Rejected - once per day is sufficient and reduces API load

### Decision: FastMCP Framework
**What**: Use FastMCP as the Python MCP server framework for protocol handling.
**Why**: FastMCP provides a fast, modern framework for building MCP servers with HTTP transport support. It reduces boilerplate and ensures MCP protocol compliance. Python is required for `instaloader` integration.
**Alternatives considered**:
- Generic `mcp` package: Rejected - FastMCP is specifically designed for fast HTTP-based MCP servers
- Manual JSON-RPC implementation: Rejected - error-prone, reinvents the wheel
- Other languages: Rejected - `instaloader` is Python-only

### Decision: HTTP Port Configuration
**What**: Default HTTP server port to 3336, configurable via environment variable in `.env` file.
**Why**: Provides a sensible default while allowing flexibility for different deployment environments. Using `.env` file is a standard practice for configuration management.
**Alternatives considered**:
- Hard-coded port: Rejected - lacks flexibility
- Command-line argument only: Rejected - `.env` is more convenient for Docker deployments

### Decision: Environment Variable Configuration
**What**: Support configuration via `.env` file, including HTTP port and cookie file path.
**Why**: Environment variables provide a clean way to configure the server without code changes. Cookie file path configuration allows users to specify where their Instagram session cookies are stored.
**Configuration options**:
- `MCP_PORT`: HTTP server port (default: 3336)
- `COOKIE_FILE`: Path to Instagram session cookie file (optional)
**Alternatives considered**:
- Configuration file (YAML/JSON): Rejected - `.env` is simpler and more standard for Docker
- Command-line arguments only: Rejected - less convenient for containerized deployments

### Decision: UV Package Manager
**What**: Use UV as the Python package manager instead of pip.
**Why**: UV is significantly faster than pip for dependency resolution and installation, written in Rust. This speeds up Docker builds and local development. UV provides a modern, fast alternative to pip while maintaining compatibility with PyPI packages.
**Alternatives considered**:
- pip: Rejected - slower than UV, user preference for speed
- poetry: Rejected - UV is faster and simpler for this use case
- pip-tools: Rejected - UV provides better performance and modern tooling

### Decision: URL Parsing and Shortcode Extraction
**What**: Parse full Instagram URLs to extract shortcodes/post IDs before passing to `instaloader`.
**Why**: Users will provide full Instagram URLs (e.g., "https://www.instagram.com/p/DRr-n4XER3x/"), but `instaloader` requires shortcodes (e.g., "DRr-n4XER3x"). The system must handle both full URLs and shortcodes directly, extracting the shortcode from URLs when needed.
**URL patterns to support**:
- `https://www.instagram.com/p/{shortcode}/`
- `https://instagram.com/p/{shortcode}/` (without www)
- `https://www.instagram.com/reel/{shortcode}/` (for reels)
- Direct shortcode input (e.g., "DRr-n4XER3x")
**Alternatives considered**:
- Require only shortcodes: Rejected - full URLs are more user-friendly and what users naturally provide
- Require only full URLs: Rejected - shortcodes should also be supported for flexibility

### Decision: Test Suite with Example URLs
**What**: Provide a test suite that reads URLs from an example text file and runs tests against the MCP server.
**Why**: Enables automated testing of the server functionality with real Instagram URLs. Using a text file makes it easy to add/remove test cases. The example file must include at least the following URLs: "https://www.instagram.com/p/DRr-n4XER3x/", "https://www.instagram.com/p/DTDy4fMDCc4/", "https://www.instagram.com/p/DQUVv9kANPh/", and "https://www.instagram.com/p/DSNKaEZjIR9/".
**Test file format**:
- One URL per line
- Empty lines ignored
- Lines starting with `#` treated as comments
- Located in `tests/example_urls.txt` or similar
**Required test URLs**:
- "https://www.instagram.com/p/DRr-n4XER3x/"
- "https://www.instagram.com/p/DTDy4fMDCc4/"
- "https://www.instagram.com/p/DQUVv9kANPh/"
- "https://www.instagram.com/p/DSNKaEZjIR9/"
**Alternatives considered**:
- Hard-coded test URLs in code: Rejected - less flexible, harder to update
- JSON/YAML test files: Rejected - plain text is simpler for URL lists
- No example test file: Rejected - user requirement specifies example file with specific URLs

## Risks / Trade-offs

### Risk: Instagram Rate Limiting
**Mitigation**: Implement rate limiting and error handling. Document rate limit considerations in documentation. Consider adding retry logic with exponential backoff.

### Risk: Instagram API Changes Breaking `instaloader`
**Mitigation**: Update checking mechanism helps identify when `instaloader` updates are available. Document dependency on `instaloader` stability.

### Risk: Session Cookie Format/Validity
**Mitigation**: Document expected cookie format. Provide clear error messages when session is invalid or expired.

### Risk: Docker Image Size
**Trade-off**: Python base images can be large. Consider using Alpine-based images or multi-stage builds to reduce size if needed.

## Migration Plan
N/A - This is a new project with no existing implementation to migrate.

## Open Questions
None - all design questions have been resolved.
