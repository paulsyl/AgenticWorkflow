#!/bin/bash
# deploy.sh
# Cross-platform single source of truth deployment wrapper.
# Runs python3 scripts/compile_and_deploy.py

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    python3 "$SCRIPT_DIR/compile_and_deploy.py" "$@"
elif command -v python >/dev/null 2>&1; then
    python "$SCRIPT_DIR/compile_and_deploy.py" "$@"
else
    echo "Error: python3 or python command is required to run deploy script."
    exit 1
fi
