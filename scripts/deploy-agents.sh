#!/bin/bash
# deploy-agents.sh
# Deploys workflow agents and Antigravity skills to user profile for global availability.
# Run from the repository root: ./scripts/deploy-agents.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VS_CODE_USER="$HOME/Library/Application Support/Code/User"
USER_PROMPTS="$HOME/Library/Application Support/Code/User/prompts"
COPILOT_AGENTS="$HOME/.copilot/agents"
PROFILE_AGENTS="$HOME/Library/Application Support/Code/User/profiles/builtin/agents"
SETTINGS_FILE="$VS_CODE_USER/settings.json"

# Antigravity Config Target Directories
ANTIGRAVITY_SKILLS_HOME="$HOME/.gemini/config/skills"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Deploying agents and Antigravity skills to user profile..."
echo ""

# Create directories
mkdir -p "$USER_PROMPTS/agents" "$COPILOT_AGENTS" "$PROFILE_AGENTS" "$ANTIGRAVITY_SKILLS_HOME"

# Deploy Antigravity Skills if present
if [ -d "$REPO_ROOT/skills" ]; then
    SKILL_DIRS=("$REPO_ROOT/skills/"*/)
    if [ -e "${SKILL_DIRS[0]}" ]; then
        echo "Deploying Antigravity skills..."
        for skill_dir in "${SKILL_DIRS[@]}"; do
            if [ -d "$skill_dir" ]; then
                skill_name=$(basename "$skill_dir")
                mkdir -p "$ANTIGRAVITY_SKILLS_HOME/$skill_name"
                cp -r "$skill_dir"* "$ANTIGRAVITY_SKILLS_HOME/$skill_name/" 2>/dev/null || true
                
                # If running in WSL and Windows profile exists, sync to Windows path as well
                if [ -d "/mnt/c/Users" ]; then
                    for win_user in /mnt/c/Users/*; do
                        if [ -d "$win_user/.gemini/config" ]; then
                            mkdir -p "$win_user/.gemini/config/skills/$skill_name"
                            cp -r "$skill_dir"* "$win_user/.gemini/config/skills/$skill_name/" 2>/dev/null || true
                        fi
                    done
                fi
                echo -e "  ${GREEN}✓${NC} [Antigravity Skill] $skill_name"
            fi
        done
        echo ""
    fi
fi

# Count Copilot agent files
AGENT_COUNT=$(ls -1 "$REPO_ROOT/.github/agents/"*.agent.md 2>/dev/null | wc -l | tr -d ' ')

if [ "$AGENT_COUNT" -gt 0 ]; then
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
        echo -e "  ${GREEN}✓${NC} [Copilot Agent] $filename"
    done

    # Register custom agent locations with VS Code.
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
fi

# Deploy instructions if present
if [ -f "$REPO_ROOT/.github/copilot-instructions.md" ]; then
    cp "$REPO_ROOT/.github/copilot-instructions.md" "$USER_PROMPTS/"
    echo -e "  ${GREEN}✓${NC} copilot-instructions.md"
fi

echo ""
echo -e "${GREEN}Deployment complete!${NC}"
echo ""
echo "Deployed Antigravity skills to:"
echo "  $ANTIGRAVITY_SKILLS_HOME"
echo ""
echo "Deployed Copilot agents to:"
echo "  $COPILOT_AGENTS"
echo "  $USER_PROMPTS/agents"
echo "  $PROFILE_AGENTS"
echo ""
echo "Available Antigravity skills:"
ls -1d "$REPO_ROOT/skills/"*/ 2>/dev/null | while read d; do
    name=$(basename "$d")
    echo "  @$name"
done
