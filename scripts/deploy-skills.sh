#!/bin/bash
# deploy-skills.sh
# Deploys Antigravity skills to user profile for global availability.
# Run from the repository root: ./scripts/deploy-skills.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Antigravity Config Target Directory
ANTIGRAVITY_SKILLS_HOME="$HOME/.gemini/config/skills"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Deploying Antigravity skills to user profile..."
echo ""

mkdir -p "$ANTIGRAVITY_SKILLS_HOME"

if [ -d "$REPO_ROOT/skills" ]; then
    SKILL_DIRS=("$REPO_ROOT/skills/"*/)
    if [ -e "${SKILL_DIRS[0]}" ]; then
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
                echo -e "  ${GREEN}✓${NC} [Antigravity Skill] @$skill_name"
            fi
        done
        echo ""
    fi
fi

echo -e "${GREEN}Deployment complete!${NC}"
echo ""
echo "Deployed Antigravity skills to:"
echo "  $ANTIGRAVITY_SKILLS_HOME"
echo ""
echo "Available Antigravity skills:"
ls -1d "$REPO_ROOT/skills/"*/ 2>/dev/null | while read d; do
    name=$(basename "$d")
    echo "  @$name"
done
