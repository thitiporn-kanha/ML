#!/usr/bin/env bash
set -euo pipefail
# pack.sh - create a portable zip of the project for moving to another machine
# Usage: ./pack.sh [-o output.zip] [--include-results] [--include-venv] [--include-git]

OUT=../ML-project.zip
INCLUDE_RESULTS=0
INCLUDE_VENV=0
INCLUDE_GIT=0

usage(){
  cat <<EOF
Usage: $0 [-o output.zip] [--include-results] [--include-venv] [--include-git]

By default this creates a zip at ../ML-project.zip excluding:
 - .venv, results/, .git

Options:
  -o FILE            write output zip to FILE
  --include-results  include results/ folder in the zip
  --include-venv     include .venv (not recommended)
  --include-git      include .git directory (keeps history)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o)
      OUT="$2"; shift 2;;
    --include-results)
      INCLUDE_RESULTS=1; shift;;
    --include-venv)
      INCLUDE_VENV=1; shift;;
    --include-git)
      INCLUDE_GIT=1; shift;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "Packing project from: $ROOT_DIR"

# If a .venv exists, update requirements.txt from it (optional)
if [[ -d "$ROOT_DIR/.venv" ]]; then
  if command -v "$ROOT_DIR/.venv/bin/pip" >/dev/null 2>&1; then
    echo "Detected .venv — updating requirements.txt from the environment's pip freeze"
    "$ROOT_DIR/.venv/bin/pip" freeze > "$ROOT_DIR/requirements.txt.tmp" || true
    mv "$ROOT_DIR/requirements.txt.tmp" "$ROOT_DIR/requirements.txt"
    echo "Updated requirements.txt"
  fi
fi

EXCLUDE_ARGS=("-x" "*.pyc" "-x" "__pycache__/*" "-x" ".DS_Store")

if [[ $INCLUDE_VENV -eq 0 ]]; then
  EXCLUDE_ARGS+=("-x" ".venv/*")
fi
if [[ $INCLUDE_RESULTS -eq 0 ]]; then
  EXCLUDE_ARGS+=("-x" "results/*")
fi
if [[ $INCLUDE_GIT -eq 0 ]]; then
  EXCLUDE_ARGS+=("-x" ".git/*")
fi

echo "Creating zip: $OUT"
cd "$ROOT_DIR"
rm -f "$OUT"
zip -r "$OUT" . "${EXCLUDE_ARGS[@]}"

echo "Created $OUT"
