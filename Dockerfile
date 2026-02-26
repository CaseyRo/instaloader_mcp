FROM python:3.13-slim

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files + lockfile for reproducible builds
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using UV with locked versions
RUN uv pip install --system -e .

# Copy application code
COPY src/ ./src/
COPY .env.example ./.env.example

# Create non-root user and set up instaloader config directory
RUN useradd --create-home appuser \
    && mkdir -p /home/appuser/.config/instaloader \
    && chown -R appuser:appuser /home/appuser/.config/instaloader
USER appuser

# Expose port (default 3336, configurable via MCP_PORT)
EXPOSE 3336

# Set environment variable for port (can be overridden)
ENV MCP_PORT=3336

# Run with uvicorn for production (ASGI app exposed in server.py)
# Uses shell form so $MCP_PORT is expanded at runtime
CMD uvicorn src.server:app --host 0.0.0.0 --port $MCP_PORT
