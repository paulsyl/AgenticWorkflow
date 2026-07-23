#!/bin/bash
# undeploy-agents.sh
# Removes workflow agents from user profile.
# Run from the repository root: ./scripts/undeploy-agents.sh

set -e

USER_PROMPTS="$HOME/Library/Application Support/Code/User/prompts"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "Removing agents from user profile..."
echo ""

# Remove agents
if [ -d "$USER_PROMPTS/agents" ]; then
    for agent in "$USER_PROMPTS/agents/"*.agent.md; do
        if [ -f "$agent" ]; then
            filename=$(basename "$agent")
            rm "$agent"
            echo -e "  ${RED}✗${NC} $filename"
        fi
    done
fi

# Remove instructions
if [ -f "$USER_PROMPTS/copilot-instructions.md" ]; then
    rm "$USER_PROMPTS/copilot-instructions.md"
    echo -e "  ${RED}✗${NC} copilot-instructions.md"
fi

echo ""
echo -e "${GREEN}Uninstall complete.${NC}"
echo ""
echo "Restart VS Code to apply changes."
