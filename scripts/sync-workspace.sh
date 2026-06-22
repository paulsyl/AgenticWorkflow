#!/bin/bash
# sync-workspace.sh
# Sync workspace-local .github/ configuration from repository
# Updates agents, instructions, and skills in the current project

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-.}"

echo "🔄 Syncing workspace configuration..."
echo ""
echo "From: $REPO_ROOT/.github/"
echo "To:   $PROJECT_ROOT/.github/"
echo ""

# Create .github directories if they don't exist
mkdir -p "$PROJECT_ROOT/.github/agents"
mkdir -p "$PROJECT_ROOT/.github/instructions"
mkdir -p "$PROJECT_ROOT/.github/skills"

# Copy agents (overwrite only if source has changed)
echo "📋 Syncing agents..."
for file in "$REPO_ROOT/.github/agents"/*.agent.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        dst="$PROJECT_ROOT/.github/agents/$filename"
        if [ ! -e "$dst" ] || ! diff -q "$file" "$dst" > /dev/null 2>&1; then
            cp "$file" "$dst"
            echo "  ✅ Updated: $filename"
        else
            echo "  ℹ️  Up to date: $filename"
        fi
    fi
done

# Copy instructions (overwrite only if source has changed)
echo "📋 Syncing instructions..."
for file in "$REPO_ROOT/.github/instructions"/*.instructions.md; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        dst="$PROJECT_ROOT/.github/instructions/$filename"
        if [ ! -e "$dst" ] || ! diff -q "$file" "$dst" > /dev/null 2>&1; then
            cp "$file" "$dst"
            echo "  ✅ Updated: $filename"
        else
            echo "  ℹ️  Up to date: $filename"
        fi
    fi
done

# Copy root-level configs
echo "📋 Syncing root configs..."
for file in "$REPO_ROOT/copilot-instructions.md" "$REPO_ROOT/AGENTS.md"; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        dst="$PROJECT_ROOT/$filename"
        if [ ! -e "$dst" ] || ! diff -q "$file" "$dst" > /dev/null 2>&1; then
            cp "$file" "$dst"
            echo "  ✅ Updated: $filename"
        else
            echo "  ℹ️  Up to date: $filename"
        fi
    fi
done

# Copy .copilotignore if not customized
if [ ! -f "$PROJECT_ROOT/.copilotignore" ] || grep -q "Global ignore patterns" "$PROJECT_ROOT/.copilotignore"; then
    cp "$REPO_ROOT/.copilotignore" "$PROJECT_ROOT/.copilotignore"
    echo "  ✅ Updated: .copilotignore"
else
    echo "  ⏭️  Skipped: .copilotignore (customized locally)"
fi

echo ""
echo "✅ Workspace sync complete!"
echo ""
echo "📝 Note: You can customize workspace-local agents/instructions by editing files in $PROJECT_ROOT/.github/"
echo ""
