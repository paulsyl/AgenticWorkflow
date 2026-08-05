#!/bin/bash
# deploy-agents.sh
# Deploys GitHub Copilot agents and instructions to user profile for global availability.
# Run from the repository root: ./scripts/deploy-agents.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VS_CODE_USER="$HOME/Library/Application Support/Code/User"
USER_PROMPTS="$HOME/Library/Application Support/Code/User/prompts"
COPILOT_AGENTS="$HOME/.copilot/agents"
PROFILE_AGENTS="$HOME/Library/Application Support/Code/User/profiles/builtin/agents"
SETTINGS_FILE="$VS_CODE_USER/settings.json"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Deploying GitHub Copilot agents to user profile..."
echo ""

mkdir -p "$USER_PROMPTS/agents" "$COPILOT_AGENTS" "$PROFILE_AGENTS"

AGENT_COUNT=$(ls -1 "$REPO_ROOT/.github/agents/"*.agent.md 2>/dev/null | wc -l | tr -d ' ')

if [ "$AGENT_COUNT" -eq 0 ]; then
    echo "No agent files found in .github/agents/"
    exit 1
fi

echo "Deploying $AGENT_COUNT Copilot agents..."
for agent in "$REPO_ROOT/.github/agents/"*.agent.md; do
    filename=$(basename "$agent")
    cp "$agent" "$USER_PROMPTS/agents/$filename"
    cp "$agent" "$PROFILE_AGENTS/$filename"
    python3 - "$agent" "$COPILOT_AGENTS/$filename" <<'PY'
import re
import sys
from pathlib import Path

source = Path(sys.argv[1])
target = Path(sys.argv[2])
text = source.read_text()

model_slugs = {
    "Claude Sonnet 4.6 (copilot)": "claude-sonnet-4.6",
    "GPT-5.4 (copilot)": "gpt-5.4",
    "GPT-5.3-Codex (copilot)": "gpt-5.3-codex",
    "GPT-5.4 mini (copilot)": "gpt-5.4-mini",
    "MAI-Code-1-Flash (copilot)": "mai-code-1-flash",
}

def cli_model(match):
    models = [item.strip().strip("'\"") for item in match.group(1).split(",")]
    for model in models:
        if model in model_slugs:
            return f"model: {model_slugs[model]}"
    raise SystemExit(f"No CLI model slug mapping for {source}: {models}")

text = re.sub(r"^model:\s*\[([^\n]+)\]$", cli_model, text, count=1, flags=re.MULTILINE)
target.write_text(text)
PY
    echo -e "  ${GREEN}✓${NC} $filename"
done

python3 - "$SETTINGS_FILE" "$COPILOT_AGENTS" "$USER_PROMPTS/agents" "$PROFILE_AGENTS" <<'PY'
import json
import sys
from pathlib import Path

settings_path = Path(sys.argv[1])
cli_agent_location = sys.argv[2]
agent_locations = sys.argv[3:]

if settings_path.exists():
    with settings_path.open() as settings_file:
        settings = json.load(settings_file)
else:
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings = {}

locations = settings.setdefault("chat.agentFilesLocations", {})
locations.pop(cli_agent_location, None)
for location in agent_locations:
    locations[location] = True

with settings_path.open("w") as settings_file:
    json.dump(settings, settings_file, indent=4)
    settings_file.write("\n")
PY

echo -e "  ${GREEN}✓${NC} chat.agentFilesLocations"

if [ -f "$REPO_ROOT/.github/copilot-instructions.md" ]; then
    cp "$REPO_ROOT/.github/copilot-instructions.md" "$USER_PROMPTS/"
    echo -e "  ${GREEN}✓${NC} copilot-instructions.md"
fi

echo ""
echo -e "${GREEN}Deployment complete!${NC}"
echo ""
echo "Deployed Copilot agents to:"
echo "  $COPILOT_AGENTS"
echo "  $USER_PROMPTS/agents"
echo "  $PROFILE_AGENTS"
echo ""
echo "Available Copilot agents:"
ls -1 "$COPILOT_AGENTS/"*.agent.md 2>/dev/null | while read f; do
    name=$(basename "$f" .agent.md)
    echo "  $name"
done

echo ""
echo -e "${YELLOW}Note:${NC} Restart VS Code or reload window to pick up changes."
