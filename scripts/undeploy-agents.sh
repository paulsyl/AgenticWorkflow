#!/bin/bash
# undeploy-agents.sh
# Removes workflow agents from user profile.
# Run from the repository root: ./scripts/undeploy-agents.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
USER_PROMPTS="$HOME/Library/Application Support/Code/User/prompts"
COPILOT_AGENTS="$HOME/.copilot/agents"
PROFILE_AGENTS="$HOME/Library/Application Support/Code/User/profiles/builtin/agents"
SETTINGS_FILE="$HOME/Library/Application Support/Code/User/settings.json"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "Removing agents from user profile..."
echo ""

# Remove only this workflow's agents
for source_agent in "$REPO_ROOT/.github/agents/"*.agent.md; do
    if [ -f "$source_agent" ]; then
        filename=$(basename "$source_agent")
        for target_dir in "$USER_PROMPTS/agents" "$COPILOT_AGENTS" "$PROFILE_AGENTS"; do
            if [ -f "$target_dir/$filename" ]; then
                rm "$target_dir/$filename"
                echo -e "  ${RED}✗${NC} $target_dir/$filename"
            fi
        done
    fi
done

# Unregister custom agent locations when they are empty.
python3 - "$SETTINGS_FILE" "$COPILOT_AGENTS" "$USER_PROMPTS/agents" "$PROFILE_AGENTS" <<'PY'
import json
import sys
from pathlib import Path

settings_path = Path(sys.argv[1])
agent_locations = sys.argv[2:]

if not settings_path.exists():
    raise SystemExit

with settings_path.open() as settings_file:
    settings = json.load(settings_file)

locations = settings.get("chat.agentFilesLocations")
if isinstance(locations, dict):
    for location in agent_locations:
        path = Path(location).expanduser()
        if not any(path.glob("*.agent.md")):
            locations.pop(location, None)
    if not locations:
        settings.pop("chat.agentFilesLocations", None)

with settings_path.open("w") as settings_file:
    json.dump(settings, settings_file, indent=4)
    settings_file.write("\n")
PY

# Remove instructions
if [ -f "$USER_PROMPTS/copilot-instructions.md" ]; then
    rm "$USER_PROMPTS/copilot-instructions.md"
    echo -e "  ${RED}✗${NC} copilot-instructions.md"
fi

echo ""
echo -e "${GREEN}Uninstall complete.${NC}"
echo ""
echo "Restart VS Code or reload window to apply changes."
