#!/bin/bash
# deploy-agents.sh
# Deploys workflow agents and instructions to user profile for global availability.
# Run from the repository root: ./scripts/deploy-agents.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
USER_PROMPTS="$HOME/Library/Application Support/Code/User/prompts"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Deploying agents to user profile..."
echo ""

# Create directories
mkdir -p "$USER_PROMPTS/agents"

# Count files
AGENT_COUNT=$(ls -1 "$REPO_ROOT/.github/agents/"*.agent.md 2>/dev/null | wc -l | tr -d ' ')

if [ "$AGENT_COUNT" -eq 0 ]; then
    echo "No agent files found in .github/agents/"
    exit 1
fi

# Deploy agents
echo "Deploying $AGENT_COUNT agents..."
for agent in "$REPO_ROOT/.github/agents/"*.agent.md; do
    filename=$(basename "$agent")
    cp "$agent" "$USER_PROMPTS/agents/$filename"
    echo -e "  ${GREEN}✓${NC} $filename"
done

# Deploy instructions if present
if [ -f "$REPO_ROOT/.github/copilot-instructions.md" ]; then
    cp "$REPO_ROOT/.github/copilot-instructions.md" "$USER_PROMPTS/"
    echo -e "  ${GREEN}✓${NC} copilot-instructions.md"
fi

echo ""
echo -e "${GREEN}Deployment complete!${NC}"
echo ""
echo "Deployed to: $USER_PROMPTS"
echo ""
echo "Available agents:"
ls -1 "$USER_PROMPTS/agents/"*.agent.md 2>/dev/null | while read f; do
    name=$(basename "$f" .agent.md)
    echo "  @$name"
done

echo ""
echo -e "${YELLOW}Note:${NC} Restart VS Code or reload window to pick up changes."
