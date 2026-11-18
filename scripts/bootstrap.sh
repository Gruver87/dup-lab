#!/usr/bin/env bash
# One-shot Unix entry: clone siblings, install skills, wire Cursor MCP, run demos
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 -m pip install -U pip -q
python3 scripts/bootstrap.py "$@"
