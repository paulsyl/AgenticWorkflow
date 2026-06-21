#!/usr/bin/env bash
# Helper script to set common environment variables for Antigravity core-workflow skills

export PROJECT_ROOT="$(pwd)"
export PLAN_FILE="$PROJECT_ROOT/implementation_plan.md"

# Uncomment and set if you need a custom launch command that cannot be auto-detected
# export LAUNCH_CMD="npm run dev"

echo "✅ Environment configured for Antigravity"
echo "PROJECT_ROOT: $PROJECT_ROOT"
echo "PLAN_FILE: $PLAN_FILE"
echo "LAUNCH_CMD: ${LAUNCH_CMD:-<auto-detect>}"
