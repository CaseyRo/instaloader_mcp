FROM python:3.11-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml README.md ./

# Install dependencies using UV
RUN uv pip install --system --prerelease=allow -e .

# Copy application code
COPY src/ ./src/
COPY .env.example ./.env.example

# Expose port (default 3336, configurable via MCP_PORT)
EXPOSE 3336

# Set environment variable for port (can be overridden)
ENV MCP_PORT=3336

# Run the server as a module so relative imports work
CMD ["python", "-m", "src.server"]
