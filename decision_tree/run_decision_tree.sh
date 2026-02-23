#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)/.."
source "$ROOT/.venv/bin/activate" || true
cd "$(dirname "$0")"
python main.py 2>&1 | tee run.log
