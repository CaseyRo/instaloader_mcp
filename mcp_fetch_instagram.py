#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.request
from typing import Any, Dict, Optional


def _read_stdin_json() -> Optional[Dict[str, Any]]:
    if sys.stdin.isatty():
        return None
    raw = sys.stdin.read().strip()
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _find_url(value: Any) -> Optional[str]:
    if isinstance(value, str):
        if "instagram.com/" in value:
            return value
        return None
    if isinstance(value, dict):
        for key in ("url",):
            found = value.get(key)
            if isinstance(found, str) and "instagram.com/" in found:
                return found
        for child in value.values():
            found = _find_url(child)
            if found:
                return found
    if isinstance(value, list):
        for item in value:
            found = _find_url(item)
            if found:
                return found
    return None


def _extract_url(payload: Optional[Dict[str, Any]]) -> Optional[str]:
    if not payload:
        return None
    paths = [
        ("url",),
        ("arguments", "url"),
        ("params", "arguments", "url"),
        ("body", "recipe", "url"),
        ("recipe", "url"),
    ]
    for path in paths:
        current: Any = payload
        for key in path:
            if not isinstance(current, dict) or key not in current:
                current = None
                break
            current = current[key]
        if isinstance(current, str) and "instagram.com/" in current:
            return current
    return _find_url(payload)


def _build_mcp_url(host: str, port: str, mcp_url: Optional[str]) -> str:
    if mcp_url:
        return mcp_url
    if host.startswith(("http://", "https://")):
        return host
    if ":" in host:
        return f"http://{host}/mcp"
    return f"http://{host}:{port}/mcp"


def _post_json(url: str, payload: Dict[str, Any], headers: Dict[str, str]) -> tuple[Dict[str, str], str]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8", errors="replace")
        response_headers = {k.lower(): v for k, v in response.headers.items()}
    return response_headers, body


def _parse_sse_data(body: str) -> str:
    data_lines = []
    for line in body.splitlines():
        if line.startswith("data: "):
            data_lines.append(line[len("data: ") :])
    if data_lines:
        return data_lines[-1]
    return body.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Call Instaloader MCP tools with a URL only.")
    parser.add_argument("host", nargs="?", default="192.168.1.5", help="Host or host:port")
    parser.add_argument("port", nargs="?", default="3336", help="Port if host has no port")
    parser.add_argument("--mcp-url", dest="mcp_url", help="Full MCP URL (overrides host/port)")
    parser.add_argument("--tool", default="fetch_instagram_reel", help="Tool name to call")
    parser.add_argument("--url", help="Instagram URL to fetch")
    args = parser.parse_args()

    input_payload = _read_stdin_json()
    url = args.url or _extract_url(input_payload)
    if not url:
        print("Error: no Instagram URL found. Provide --url or JSON on stdin.", file=sys.stderr)
        return 2

    mcp_url = _build_mcp_url(args.host, args.port, args.mcp_url)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mcp_fetch_instagram", "version": "0.1"},
        },
    }
    init_headers, init_body = _post_json(mcp_url, init_payload, headers)
    session_id = init_headers.get("mcp-session-id")
    if not session_id:
        print("Error: failed to initialize MCP session.", file=sys.stderr)
        print(init_body, file=sys.stderr)
        return 3

    call_payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": args.tool, "arguments": {"url": url}},
    }
    call_headers = dict(headers)
    call_headers["Mcp-Session-Id"] = session_id
    _, call_body = _post_json(mcp_url, call_payload, call_headers)
    data = _parse_sse_data(call_body)

    try:
        parsed = json.loads(data)
    except json.JSONDecodeError:
        print(data)
        return 0

    print(json.dumps(parsed, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
