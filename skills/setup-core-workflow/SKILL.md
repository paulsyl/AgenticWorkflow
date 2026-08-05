---
name: setup-core-workflow
description: >
  Per-repo setup skill that configures the core-workflow for a specific project.
  Creates the workflow directory structure and writes a project-specific config file.
  Run this once per repo before using the other core-workflow skills.
  Summon via @setup-core-workflow or /setup-core-workflow.
---

# Setup Core Workflow

Run this once per repo to configure the core-workflow skills for your project.

## Process

### 1. Ask Configuration Questions

Ask the user (accept defaults if they press enter):

1. **Workflow directory:** Where should workflow artifacts live?
   - Default: `./AgentWorkflow/`

2. **Test runner:** What command runs your tests?
   - Auto-detect: look for `pytest`, `npm test`, `go test`, `cargo test` based on project files
   - Default: auto-detected value, or ask if ambiguous

3. **Launch command:** How do you start the application locally?
   - Auto-detect: `docker-compose.yml` → `docker compose up`, `manage.py` → `python manage.py runserver`, `package.json` → `npm start`
   - Default: auto-detected value, or ask if ambiguous

### 2. Create Directory Structure

```bash
mkdir -p <workflow_dir>/01_requirements
mkdir -p <workflow_dir>/02_architecture/iterations
mkdir -p <workflow_dir>/03_reviews
mkdir -p <workflow_dir>/04_execution
```

### 3. Sync Harness Ignore Files

Execute the python ignore sync utility to ensure master `.agentignore` exists and non-destructively syncs to target agent harnesses (`.antigravityignore`, `.copilotignore`, `.github/copilot-ignore`, `.claudeignore`, `.ignore`):

```bash
python3 scripts/sync_agent_ignores.py
```

### 4. Ensure Repository Ignore Files

Create or update `.gitignore` at the repo root. Preserve existing entries and append the workflow directory if it is missing:

```gitignore
# Agent workflow artifacts
<workflow_dir>/
```

Create or update `.antigravityignore` at the repo root. Preserve existing entries and append defaults if missing. Do not add the workflow directory to ignore files; workflow markdown outputs must remain visible to LLMs.

### 5. Write Config

Write `.agents/core-workflow-config.md` at the repo root:

```markdown
# Core Workflow Configuration

- **Workflow directory:** <workflow_dir>
- **Test runner:** <test_command>
- **Launch command:** <launch_command>
- **Date configured:** <today>
```

### 6. Confirm

```
✅ Core workflow configured for this repository.

Workflow artifacts: <workflow_dir>/
Config saved: .agents/core-workflow-config.md

Available skills:
  @specifier-grill     — alignment, grilling & PRD generation
  @specifier-adversary — adversarial challenge of alignment
  @architect          — technical blueprints (vertical slices)
  @review-council     — plan validation (4 core reviewers)
  @executor           — phase-by-phase implementation
  @orchestrator       — build loop (optional)
  @prototype          — throwaway exploration
```
