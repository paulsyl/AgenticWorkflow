# Customization Guide: Extending AgenticWorkflow

This document explains how to create, modify, and extend agents, instructions, and skills in AgenticWorkflow.

---

## Table of Contents

1. [Understanding Customization Files](#understanding-customization-files)
2. [Creating Custom Agents](#creating-custom-agents)
3. [Creating Custom Instructions](#creating-custom-instructions)
4. [Creating Custom Skills](#creating-custom-skills)
5. [Workspace vs. Global Scope](#workspace-vs-global-scope)
6. [YAML Frontmatter Reference](#yaml-frontmatter-reference)
7. [Troubleshooting](#troubleshooting)

---

## Understanding Customization Files

GitHub Copilot customization uses several file types:

### Agent Files (`.agent.md`)

Specialized AI personas with specific capabilities and tool restrictions.

**Use when**: You need a distinct workflow or tool restrictions (e.g., read-only mode, full execution mode).

**File location**: `.github/agents/` (workspace) or user-level prompts (global)

**Example**:
```markdown
---
name: my-agent
description: Does X by doing Y. Use when Z.
applyTo: "**"
---

# My Agent

[instructions in markdown]
```

### Instruction Files (`.instructions.md`)

Always-on rules that apply to agent behavior or file-specific guidance.

**Use when**: You want to establish coding standards, project conventions, or guidelines that should apply broadly.

**File location**: `.github/instructions/` (workspace) or user-level prompts (global)

**Example**:
```markdown
---
name: my-rules
description: Rules for X. Applies to files matching Y. Use when Z.
applyTo: "src/services/**"
---

# My Coding Rules

[instructions in markdown]
```

### Skill Files (`SKILL.md`)

On-demand workflows with bundled assets (scripts, templates, etc.). Appear as slash commands (`/skill-name`).

**Use when**: You want a reusable, parameterized workflow that users can invoke on-demand.

**File location**: `.agents/skills/my-skill/SKILL.md` (or `.github/skills/`)

**Example**:
```markdown
---
name: my-skill
description: Does X. Use when Y.
---

# My Skill

[instructions]
```

---

## Creating Custom Agents

### Step 1: Decide on Scope

- **Global**: Agent used across all projects → user-level prompts
- **Workspace-local**: Agent specific to this project → `.github/agents/`

For this guide, we'll create workspace-local agents (easier to version control).

### Step 2: Create the Agent File

Create `.github/agents/my-agent.agent.md`:

```markdown
---
name: my-agent
description: >
  Brief description of what this agent does. Use when requesting [specific task].
  This description is the discovery surface—include keywords so Copilot finds this agent.
applyTo: "**"
---

# My Agent: [Title]

You are [persona description].

## Primary Directive

[What the agent should do]

## Workflow

[Step-by-step instructions]

## Tool Restrictions

### Allowed
✅ [Tools/capabilities allowed]

### Forbidden
❌ [Tools/capabilities forbidden]

## Halt Behavior

After [completion condition], halt with: "[Explicit message to user]"

## Example

[Example session]
```

### Step 3: Define Tool Restrictions (Critical)

Specify exactly what the agent can and cannot do:

```markdown
## Tool Restrictions

### Allowed
✅ Read files (code search, file exploration)
✅ Semantic analysis
✅ Plan file writing

### Forbidden
❌ Code execution (no pytest, npm test, etc.)
❌ Terminal commands
❌ File modifications outside the plan
```

### Step 4: Define Halt Behavior

Specify when the agent should stop and what message to show:

```markdown
## Halt Behavior

After creating the plan:
- DO NOT proceed to review or execution
- Explicitly tell the user: "Plan saved to {path}. Summon @review to begin critique."
```

### Step 5: Test

1. Restart VS Code to load the new agent
2. Type `@my-agent` in chat and select it
3. Test the agent with a sample request
4. Verify tool restrictions are working (agent doesn't execute code, modify files beyond scope, etc.)

### Step 6: Iterate

If the agent behavior is wrong:
1. Edit `.github/agents/my-agent.agent.md`
2. Restart Copilot/VS Code
3. Test again

---

## Creating Custom Instructions

### Step 1: Identify Scope

- **Files it applies to**: Use `applyTo` glob pattern
  - `"**"` = all files (applies globally)
  - `"src/services/**"` = only services
  - `"**/*.py"` = only Python files

- **When it applies**: Trigger keywords in description

### Step 2: Create the Instruction File

Create `.github/instructions/my-rules.instructions.md`:

```markdown
---
name: my-rules
description: >
  Rules for [domain]. Applies when working with [files]. Use when: [keyword phrases].
applyTo: "src/**"
---

# My Coding Rules

These rules apply to all code in `src/`.

## Rule 1: [Name]

[Explanation]

```python
# ✅ CORRECT
[example]

# ❌ WRONG
[counterexample]
```

## Rule 2: [Name]

[Explanation]
```

### Step 3: Set `applyTo` Correctly

**CRITICAL**: `applyTo` is a glob pattern that determines when the instruction loads.

```yaml
applyTo: "**"                    # Always-on (global)
applyTo: "src/**"                # Only src/ files
applyTo: "**/*.py"               # Only Python files
applyTo: "tests/**/*.test.ts"    # Test files only
applyTo: "**/services/**"        # Services modules
```

**Warning**: `applyTo: "**"` loads the instruction for EVERY file interaction. Use sparingly; include only truly global rules (security, core principles).

### Step 4: Make Description Discoverable

The description field is the discovery surface. Include trigger keywords:

```yaml
# ✅ GOOD - Keywords help Copilot find this
description: "Python service layer patterns. Use when: writing services, business logic, building APIs."

# ❌ WRONG - Too vague
description: "Python rules"
```

### Step 5: Test

1. Restart VS Code
2. Open a matching file (e.g., `src/services/user_service.py`)
3. Start editing code and confirm instruction appears in suggestions
4. Verify the rules are being applied

---

## Creating Custom Skills

Skills are on-demand workflows with bundled assets (scripts, templates, configurations).

### Step 1: Create Skill Directory

```bash
mkdir -p .agents/skills/my-skill
touch .agents/skills/my-skill/SKILL.md
```

### Step 2: Create `SKILL.md`

```markdown
---
name: my-skill
description: >
  What this skill does. Use when: requesting [specific task].
  Briefly explain inputs, outputs, and use cases.
---

# My Skill

## Overview

[What does this skill do?]

## Use Cases

- When you need to [X]
- When you want to [Y]

## Workflow

1. Step 1: [User input]
2. Step 2: [Agent action]
3. Step 3: [Output]

## Example

```
/my-skill with these parameters...
```

## Configuration

[Environment variables, settings, etc.]

## Bundled Assets

- `script.py` — Does X
- `template.md` — Template for Y
```

### Step 3: Create Bundled Scripts

Add any supporting scripts to the same directory:

```bash
.agents/skills/my-skill/
├── SKILL.md              # Skill documentation
├── script.py             # Automation script
├── template.md           # Template file
└── config.json           # Configuration
```

### Step 4: Document Asset Usage

In `SKILL.md`, document how each asset is used:

```markdown
## Assets

### `script.py`

Processes input and generates output.

```bash
python script.py <input>
```

Returns JSON with results.

### `template.md`

Starter template for [purpose]. Customize as needed.
```

### Step 5: Test

1. Restart VS Code
2. Type `/my-skill` in chat
3. Verify the skill appears and executes correctly

---

## Workspace vs. Global Scope

### Workspace-Local (Recommended for Teams)

Files in `.github/` are version-controlled and team-shared.

**Location**: `.github/agents/`, `.github/instructions/`, `.github/skills/`

**Pros**:
- ✅ Version controlled
- ✅ Team-shared customizations
- ✅ Project-specific overrides
- ✅ Easy to sync with `./scripts/sync-workspace.sh`

**Cons**:
- Duplicated files if used across many projects

**Setup**:
```bash
# Sync from repository
/path/to/AgenticWorkflow/scripts/sync-workspace.sh

# Now customize in .github/
# Commit to version control
git add .github/
git commit -m "Add custom agents for project"
```

### Global (User-Level)

Files in user's Copilot prompts directory are available everywhere.

**Location**: `~/Library/Application Support/Code/User/prompts/copilot/`

**Pros**:
- ✅ Available in all projects (no duplication)
- ✅ Automatic symlink updates

**Cons**:
- Not version-controlled
- Requires initial setup

**Setup**:
```bash
cd /path/to/AgenticWorkflow
./scripts/install-global.sh
```

### Precedence

If both exist, **workspace-local takes precedence** over global.

Example:
- Global: `@architect` agent (available everywhere)
- Workspace: `.github/agents/architect.agent.md` (overrides global)

Result: The workspace version is used for this project.

---

## YAML Frontmatter Reference

All customization files start with YAML frontmatter (between `---` markers).

### Required Fields

```yaml
---
name: my-name
description: Brief description. Include trigger keywords.
---
```

### Optional Fields

```yaml
---
name: my-name
description: >
  Multi-line description using > folding syntax.
  Keywords for discovery.

# For instructions and custom agents
applyTo: "**"

# For custom agents with tool restrictions
hooks:
  - event: "PreToolUse"
    action: "block"
    tools: ["execute", "terminal"]

# For agents with specific models
models:
  - "claude-opus"
  - "claude-sonnet"

# For skills
version: "1.0.0"
---
```

### Common Patterns

**Multi-line description**:
```yaml
description: >
  First line of description. Use when: requesting X.
  Second line with more details. Includes keywords for discovery.
applyTo: "**"
```

**Escaping special characters**:
```yaml
# If description contains colons, quote it
description: "Use when: doing X. Pattern: Y to Z."

# Arrays use `-` prefix
applyTo:
  - "src/**"
  - "tests/**"
```

**Forbidden characters**:
```yaml
# ❌ DON'T use unquoted colons
description: Use when: doing X

# ✅ Quote descriptions with colons
description: "Use when: doing X"
```

---

## Troubleshooting

### Agent/Instruction Not Appearing

**Symptom**: You created a file but `@my-agent` doesn't appear in the suggestion list.

**Solutions**:
1. Restart VS Code (Copilot needs to reload)
2. Check YAML frontmatter syntax (use validator if unsure)
3. Verify file is in correct location (`.github/agents/`, `.github/instructions/`, etc.)
4. Check file name matches `name` field: `my-agent.agent.md` → `name: my-agent`
5. Ensure `description` includes discovery keywords

### YAML Frontmatter Error

**Symptom**: Agent/instruction loads but seems ignored; no error message.

**Common causes**:
- Unquoted colons in description: `Use when: X` should be `"Use when: X"`
- Tabs instead of spaces (YAML requires spaces)
- `name` doesn't match filename
- Missing `---` marker

**Fix**:
1. Use YAML linter: `yamllint my-file.md`
2. Validate frontmatter manually
3. Compare with working examples in this repo

### Instruction Not Applying to Files

**Symptom**: You created an instruction with `applyTo: "src/**"` but it's not appearing.

**Solutions**:
1. Verify `applyTo` glob is correct
2. Check file you're editing matches the pattern
3. If using multi-line glob, ensure each line is quoted
4. Try simpler pattern first: `applyTo: "**"` (global)
5. Restart VS Code

### Skills Not Appearing as Slash Command

**Symptom**: You created `SKILL.md` but `/my-skill` doesn't work.

**Solutions**:
1. Verify `SKILL.md` is in `.agents/skills/my-skill/` directory
2. Check `name` field in frontmatter matches folder name
3. Restart VS Code
4. Try typing `/` to see list of available skills

### Circular or Conflicting Instructions

**Symptom**: Instructions conflict or override each other unexpectedly.

**Solutions**:
1. Check `applyTo` patterns don't overlap unnecessarily
2. Document intended precedence
3. Use descriptive names to clarify purpose
4. Consider if instruction should be split into separate files

### Performance Issues After Adding Instructions

**Symptom**: Copilot responds slowly after adding new instructions.

**Likely cause**: `applyTo: "**"` with very long instructions loads on every file.

**Solution**:
1. Use specific `applyTo` patterns instead of `"**"`
2. Move verbose documentation to external files
3. Keep always-on instructions brief and essential

---

## Best Practices

### File Organization

```
.github/
├── agents/
│   ├── architect.agent.md          # Core agents
│   ├── review.agent.md
│   ├── executor.agent.md
│   └── my-custom-agent.agent.md    # Your custom agents
├── instructions/
│   ├── core-workflow-base.instructions.md     # Core instructions
│   ├── security-coding-standards.instructions.md
│   └── my-project-rules.instructions.md       # Your custom rules
└── CUSTOMIZATION.md                # This file
```

### Naming Conventions

- **Agents**: `noun.agent.md` (e.g., `architect.agent.md`, `reviewer.agent.md`)
- **Instructions**: `adjective-noun.instructions.md` (e.g., `security-coding.instructions.md`)
- **Skills**: `my-skill/SKILL.md` (kebab-case folder name)

### Documentation

Always include:
1. **Purpose** — What does this agent/instruction do?
2. **Use case** — When should users invoke this?
3. **Example** — Show a typical session
4. **Halt behavior** — When does it stop and what does it say?

### Versioning

For significant changes:
- Update the `version` field in frontmatter
- Document changes in a CHANGELOG
- Consider backwards compatibility

---

## Advanced Topics

### Creating Multi-Stage Workflows

Combine multiple agents for complex workflows:

```markdown
---
name: complex-workflow
description: Complex task requiring multiple stages.
---

# Complex Workflow

This workflow uses multiple agents:

1. First, use @architect to plan
2. Then, summon @review to critique
3. Finally, use @executor to build

[Detailed instructions]
```

### Integrating External Tools

Use skills to wrap external tools:

```markdown
---
name: linter-checker
description: Run linter and format code. Use when: checking code quality.
---

# Linter Checker Skill

[Script that runs linter]
```

### Custom Hooks (Advanced)

Hooks run shell commands at specific lifecycle events:

```yaml
---
name: my-agent
hooks:
  - event: "PreToolUse"
    command: "validate-environment.sh"
    action: "block-on-failure"
---
```

(Consult VS Code extension docs for full hook API)

---

## Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code Settings](https://code.visualstudio.com/docs/getstarted/settings)
- [YAML Specification](https://yaml.org/)

---

See also:
- `.github/agents/` — Example agent implementations
- `.github/instructions/` — Example instruction implementations
- `.agents/skills/` — Example skill implementations
