# Instaloader MCP Server

A Model Context Protocol (MCP) server that fetches Instagram posts and reels, extracting their text content as JSON. Built with [FastMCP](https://github.com/jlowin/fastmcp) and the [instaloader](https://github.com/instaloader/instaloader) library, containerized with Docker.

## Features

- 🔗 Fetch Instagram posts and reels by URL or shortcode
- 📝 Extract text content (captions) from posts/reels
- 🔐 Optional session cookie support for private content
- 🔄 Automatic update checking for `instaloader` (cached, refreshed daily)
- 🐳 Docker containerization with docker-compose support
- 🧪 Test suite with example URLs

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository and navigate to the project directory.

2. Create a `.env` file (or copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` if needed (port defaults to 3336):
   ```env
   MCP_PORT=3336
   # COOKIE_FILE=/path/to/cookies.txt  # Optional, for private content
   ```

4. Build and run with docker-compose:
   ```bash
   docker-compose up --build
   ```

The server will be available at `http://localhost:3336` (or your configured port).

### Local Development

1. Install UV (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install dependencies:
   ```bash
   uv pip install -e .
   ```

3. Create and configure `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env as needed
   ```

4. Run the server:
   ```bash
   python src/server.py
   ```

## Configuration

### Environment Variables

- `MCP_PORT`: HTTP server port (default: `3336`)
- `COOKIE_FILE`: Path to Instagram session cookie file (optional, for private content access)

### Session Cookie Setup (Optional)

To access private Instagram posts/reels, you'll need to provide a session cookie file:

1. Use `instaloader` CLI to login and save session:
   ```bash
   instaloader --login your_username
   ```
   This creates a session file that `instaloader` can use.

2. Set the `COOKIE_FILE` environment variable or in `.env` to point to your session file.

#### Logging in via Docker

You can create a session inside the container and persist it locally:

```bash
docker compose run --rm instaloader-mcp instaloader --login your_username
```

This stores the session under `/root/.config/instaloader/session-your_username` in the container. The `docker-compose.yml` file mounts `./instaloader_sessions` to persist these sessions, so you can set:

```env
COOKIE_FILE=/root/.config/instaloader/session-your_username
```

Note: The exact cookie file format depends on how you export your Instagram session. See `instaloader` documentation for details.

## API Usage

The server exposes two MCP tools:

### `fetch_instagram_post`

Fetch an Instagram post by URL or shortcode.

**Parameters:**
- `url` (string, required): Instagram post URL (e.g., `"https://www.instagram.com/p/DRr-n4XER3x/"`) or shortcode (e.g., `"DRr-n4XER3x"`)

**Returns:**
```json
{
  "text": "Post caption text",
  "shortcode": "DRr-n4XER3x",
  "author": "username",
  "timestamp": "2024-01-01T12:00:00",
  "likes": 100,
  "comments": 10,
  "is_video": false,
  "update_info": {
    "installed_version": "4.10.0",
    "latest_version": "4.11.0",
    "update_available": true
  }
}
```

### `fetch_instagram_reel`

Fetch an Instagram reel by URL or shortcode.

**Parameters:**
- `url` (string, required): Instagram reel URL (e.g., `"https://www.instagram.com/reel/ABC123/"`) or shortcode

**Returns:**
Same format as `fetch_instagram_post`.

## Example Requests

### Using curl

```bash
curl -X POST http://localhost:3336/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "fetch_instagram_post",
      "arguments": {
        "url": "https://www.instagram.com/p/DRr-n4XER3x/"
      }
    }
  }'
```

Note: The MCP tools only accept the `url` argument. Extra fields will be rejected.

## Testing

Run tests with pytest:

```bash
uv pip install -e ".[dev]"
pytest
```

### Test File

Example URLs for testing are in `tests/example_urls.txt`. You can add more URLs to this file for testing.

Required test URLs:
- `https://www.instagram.com/p/DRr-n4XER3x/`
- `https://www.instagram.com/p/DTDy4fMDCc4/`
- `https://www.instagram.com/p/DQUVv9kANPh/`
- `https://www.instagram.com/p/DSNKaEZjIR9/`

## Docker

### Build Image

```bash
docker build -t instaloader-mcp .
```

### Run Container

```bash
docker run -p 3336:3336 \
  -e MCP_PORT=3336 \
  instaloader-mcp
```

### Docker Compose

See "Quick Start" section above for docker-compose usage.

## Update Checking

The server automatically checks for `instaloader` updates and includes this information in responses. Update checks are:
- Cached for performance
- Refreshed once per day
- Include current and latest version information

## Error Handling

The server handles various error conditions:

- **Invalid URL format**: Returns error message with invalid URL
- **Post/Reel not found**: Returns error with details
- **Authentication required**: Returns error if private content accessed without cookies
- **Network errors**: Returns appropriate error messages

## Development

### Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── server.py           # FastMCP server implementation
│   ├── instaloader_client.py  # Instaloader wrapper
│   ├── url_parser.py       # URL parsing utilities
│   └── update_checker.py   # Update checking mechanism
├── tests/
│   ├── example_urls.txt    # Test URLs
│   ├── test_url_parser.py  # URL parser tests
│   └── test_integration.py # Integration tests
├── docker/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

### Running Tests

```bash
pytest tests/
```

## Credits

This project uses and extends functionality from the following open-source libraries:

- **[instaloader](https://github.com/instaloader/instaloader)**: Python library for downloading Instagram content. This MCP server wraps instaloader to provide Instagram content access via the Model Context Protocol.
  - Copyright (c) 2016-2024 Alexander Graf, André Koch-Kramer, Federico Zivolo, and contributors
  - Licensed under the MIT License
  - GitHub: https://github.com/instaloader/instaloader

- **[FastMCP](https://github.com/jlowin/fastmcp)**: Fast Python framework for building MCP servers with HTTP transport support.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
