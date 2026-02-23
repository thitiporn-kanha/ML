#!/usr/bin/env bash
set -euo pipefail
# Simple runner for the ML workspace
# Usage: ./run.sh [logistic|linear|all]

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv"

echo "Using workspace: $ROOT"

if [ ! -d "$VENV" ]; then
  echo "Creating virtualenv at $VENV"
  python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"
echo "Installing dependencies..."
pip install --upgrade pip >/dev/null
if [ -f "$ROOT/requirements.txt" ]; then
  pip install -r "$ROOT/requirements.txt"
else
  echo "No requirements.txt found at $ROOT/requirements.txt"
fi

CMD=${1:-}
case "$CMD" in
  logistic)
    echo "Running logistic..."
    cd "$ROOT/logistic"
    python main.py
    ;;
  linear)
    echo "Running linear..."
    cd "$ROOT/linear"
    python main.py
    ;;
  all)
    echo "Running logistic then linear..."
    cd "$ROOT/logistic" && python main.py
    cd "$ROOT/linear" && python main.py
    ;;
  *)
    echo "Usage: $0 [logistic|linear|all]"
    exit 1
    ;;
esac
