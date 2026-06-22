#!/bin/bash
# install-global.sh
# Install AgenticWorkflow agents globally to user-level customization directory
# This makes agents available across all projects

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VSCODE_USER_PROMPTS="${HOME}/Library/Application Support/Code/User/prompts"
COPILOT_ANTIGRAVITY="${VSCODE_USER_PROMPTS}/copilot-antigravity"

echo "🚀 Installing AgenticWorkflow globally..."
echo ""
echo "From: $REPO_ROOT"
echo "To:   $COPILOT_ANTIGRAVITY"
echo ""

# Create user prompts directory if it doesn't exist
mkdir -p "$VSCODE_USER_PROMPTS"
mkdir -p "$COPILOT_ANTIGRAVITY"

# Function to safely link or copy a file
safe_link_or_copy() {
    local src="$1"
    local dst="$2"
    local name="$3"
    
    if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
        echo "  ✅ $name already linked"
        return
    fi
    
    if [ -L "$dst" ]; then
        rm "$dst"
        echo "  🔄 Updated symlink: $name"
    elif [ -e "$dst" ]; then
        echo "  ⚠️  File exists, skipping: $name"
        return
    fi
    
    ln -s "$src" "$dst"
    echo "  ✅ Linked: $name"
}

# Link agents (can be symlinks)
echo "📌 Linking agents..."
mkdir -p "$COPILOT_ANTIGRAVITY/agents"
safe_link_or_copy "$REPO_ROOT/.github/agents/architect.agent.md" "$COPILOT_ANTIGRAVITY/agents/architect.agent.md" "architect.agent.md"
safe_link_or_copy "$REPO_ROOT/.github/agents/review.agent.md" "$COPILOT_ANTIGRAVITY/agents/review.agent.md" "review.agent.md"
safe_link_or_copy "$REPO_ROOT/.github/agents/executor.agent.md" "$COPILOT_ANTIGRAVITY/agents/executor.agent.md" "executor.agent.md"
safe_link_or_copy "$REPO_ROOT/.github/agents/ponytail.agent.md" "$COPILOT_ANTIGRAVITY/agents/ponytail.agent.md" "ponytail.agent.md"

# Link instructions (can be symlinks)
echo "📌 Linking instructions..."
mkdir -p "$COPILOT_ANTIGRAVITY/instructions"
safe_link_or_copy "$REPO_ROOT/.github/instructions/core-workflow-base.instructions.md" "$COPILOT_ANTIGRAVITY/instructions/core-workflow-base.instructions.md" "core-workflow-base.instructions.md"
safe_link_or_copy "$REPO_ROOT/.github/instructions/ponytail-rules.instructions.md" "$COPILOT_ANTIGRAVITY/instructions/ponytail-rules.instructions.md" "ponytail-rules.instructions.md"
safe_link_or_copy "$REPO_ROOT/.github/instructions/security-coding-standards.instructions.md" "$COPILOT_ANTIGRAVITY/instructions/security-coding-standards.instructions.md" "security-coding-standards.instructions.md"
safe_link_or_copy "$REPO_ROOT/.github/instructions/development-instructions.instructions.md" "$COPILOT_ANTIGRAVITY/instructions/development-instructions.instructions.md" "development-instructions.instructions.md"

# Link or copy workspace-level config (for reference)
echo "📌 Linking workspace configs..."
safe_link_or_copy "$REPO_ROOT/copilot-instructions.md" "$COPILOT_ANTIGRAVITY/copilot-instructions.md" "copilot-instructions.md"
safe_link_or_copy "$REPO_ROOT/AGENTS.md" "$COPILOT_ANTIGRAVITY/AGENTS.md" "AGENTS.md"

# Link skills (should be symlinks so they stay in sync)
echo "📌 Linking skills..."
mkdir -p "$COPILOT_ANTIGRAVITY/skills"
safe_link_or_copy "$REPO_ROOT/.agents/skills/core-workflow" "$COPILOT_ANTIGRAVITY/skills/core-workflow" "skills/core-workflow"

# Create a README for the installed location
cat > "$COPILOT_ANTIGRAVITY/README.md" <<'EOF'
# AgenticWorkflow Global Installation

This directory contains the globally-installed AgenticWorkflow agents, instructions, and skills.

These are symlinked from the repository and will automatically stay in sync when the repo is updated.

## Usage

These agents are now available globally in any VS Code workspace that uses GitHub Copilot:

1. **@architect** — Create implementation plans
2. **@review** — Review plans with 9-phase adversarial critique
3. **@executor** — Implement approved plans with validation gates
4. **@ponytail** — Simplify code (YAGNI, stdlib, deletion)

## Instructions

Automatically applied to all code:

- `core-workflow-base` — Planning → Review → Execute flow
- `ponytail-rules` — Lazy senior developer philosophy
- `security-coding-standards` — Security requirements
- `development-instructions` — Development standards

## Workspace Overrides

To override global settings for a specific project, create a `.github/` directory in your project root and add workspace-specific `.agent.md` or `.instructions.md` files.

Workspace files take precedence over global files.

## Updating

To update the global installation from the repository:

```bash
cd /path/to/AgenticWorkflow
./scripts/install-global.sh
```

The symlinks will automatically reflect the latest changes.

---

See the repository root for complete documentation:
- `README.md` — Project overview
- `.github/CUSTOMIZATION.md` — Extending agents and instructions
- `AGENTS.md` — Agent descriptions
EOF

echo ""
echo "✅ Global installation complete!"
echo ""
echo "📍 Location: $COPILOT_ANTIGRAVITY"
echo ""
echo "🎯 Available agents:"
echo "   - @architect — Create implementation plans"
echo "   - @review — Review plans with adversarial critique"
echo "   - @executor — Execute approved plans"
echo "   - @ponytail — Simplify code"
echo ""
echo "💡 Tip: Use @architect in any workspace to start an agentic workflow"
echo ""
echo "📚 Documentation: Open README.md in the installation directory"
echo ""
