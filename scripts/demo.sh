#!/usr/bin/env sh
set -eu
BASE_URL="${BASE_URL:-http://localhost:8080}"
echo "== Health =="
curl -fsS "$BASE_URL/health"; echo
echo "== Create message =="
curl -fsS -X POST "$BASE_URL/api/messages" -H 'Content-Type: application/json' -d '{"content":"Hello from Docker portfolio"}'; echo
echo "== List messages =="
curl -fsS "$BASE_URL/api/messages"; echo
echo "== Generate 404 and 500 for log analysis =="
curl -s -o /dev/null -w '404 -> %{http_code}\n' "$BASE_URL/not-found"
curl -s -o /dev/null -w '500 -> %{http_code}\n' "$BASE_URL/demo-500"
