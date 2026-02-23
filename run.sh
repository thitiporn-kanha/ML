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
  random_forest)
    echo "Running random_forest..."
    cd "$ROOT/random_forest"
    python main.py
    ;;
  svm)
    echo "Running svm..."
    cd "$ROOT/svm"
    python main.py
    ;;
  knn)
    echo "Running knn..."
    cd "$ROOT/knn"
    python main.py
    ;;
  nn)
    echo "Running nn..."
    cd "$ROOT/nn"
    python main.py
    ;;
  kmeans)
    echo "Running kmeans..."
    cd "$ROOT/kmeans"
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
