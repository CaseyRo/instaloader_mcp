#!/usr/bin/env bash
set -euo pipefail

HOST="${1:-192.168.1.5}"
PORT="${2:-3336}"
URLS_FILE="${3:-tests/example_urls.txt}"

if [[ "${HOST}" == http*://* ]]; then
  MCP_URL="${HOST}"
elif [[ "${HOST}" == *:* ]]; then
  MCP_URL="http://${HOST}/mcp"
else
  MCP_URL="http://${HOST}:${PORT}/mcp"
fi

if [[ ! -f "${URLS_FILE}" ]]; then
  echo "URL file not found: ${URLS_FILE}" >&2
  exit 1
fi

init_payload='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"mcp-url-tester","version":"0.1"}}}'
init_response="$(curl -s -i -X POST "${MCP_URL}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d "${init_payload}")"

session_id="$(printf "%s" "${init_response}" | grep -i "^mcp-session-id:" | head -n 1 | cut -d ":" -f 2- | tr -d "[:space:]")"
if [[ -z "${session_id}" ]]; then
  echo "Failed to initialize MCP session." >&2
  echo "${init_response}" >&2
  exit 1
fi

id=2
while IFS= read -r url; do
  [[ -z "${url}" ]] && continue
  [[ "${url}" =~ ^# ]] && continue

  payload="$(printf '{"jsonrpc":"2.0","id":%s,"method":"tools/call","params":{"name":"fetch_instagram_post","arguments":{"url":"%s"}}}' "${id}" "${url}")"
  echo "== ${url} =="
  echo "POST ${MCP_URL}"
  response="$(curl -s -X POST "${MCP_URL}" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -H "Mcp-Session-Id: ${session_id}" \
    -d "${payload}")"

  json_line="$(printf "%s" "${response}" | sed -n 's/^data: //p' | tail -n 1)"
  if [[ -n "${json_line}" ]]; then
    if command -v python3 >/dev/null 2>&1; then
      printf "%s" "${json_line}" | python3 -m json.tool
    elif command -v python >/dev/null 2>&1; then
      printf "%s" "${json_line}" | python -m json.tool
    elif command -v jq >/dev/null 2>&1; then
      printf "%s" "${json_line}" | jq .
    else
      printf "%s\n" "${json_line}"
    fi
  else
    printf "%s\n" "${response}"
  fi
  echo
  id=$((id + 1))
done < "${URLS_FILE}"
