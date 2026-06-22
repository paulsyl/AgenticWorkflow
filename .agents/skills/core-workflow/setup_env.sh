#!/bin/bash
# setup_env.sh
# Helper script to set common environment variables for Antigravity core-workflow skills
# Source this script before running skills manually or testing

export PROJECT_ROOT="${PROJECT_ROOT:-.}"
export PLAN_FILE="${PLAN_FILE:-$PROJECT_ROOT/implementation_plan.md}"
export PROGRESS_FILE="${PROGRESS_FILE:-$PROJECT_ROOT/PROGRESS.md}"

# Auto-detect launch command if not provided
if [ -z "$LAUNCH_CMD" ]; then
    if [ -f "$PROJECT_ROOT/docker-compose.yml" ]; then
        export LAUNCH_CMD="docker-compose up"
    elif [ -f "$PROJECT_ROOT/manage.py" ]; then
        export LAUNCH_CMD="python manage.py runserver"
    elif [ -f "$PROJECT_ROOT/package.json" ]; then
        export LAUNCH_CMD="npm start"
    elif [ -f "$PROJECT_ROOT/go.mod" ]; then
        export LAUNCH_CMD="go run ."
    fi
fi

echo "✅ Environment configured for Antigravity"
echo "PROJECT_ROOT: $PROJECT_ROOT"
echo "PLAN_FILE: $PLAN_FILE"
echo "PROGRESS_FILE: $PROGRESS_FILE"
echo "LAUNCH_CMD: ${LAUNCH_CMD:-<auto-detect>}"
