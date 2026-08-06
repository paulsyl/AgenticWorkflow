---
name: setup-workflow
description: Per-repo setup that configures the core-workflow for a specific project. Creates the workflow directory structure and writes a project-specific config file. Run this once per repo before using the other workflow agents.
model: ['GPT-5.4 mini (copilot)', 'MAI-Code-1-Flash (copilot)', 'GPT-5.3-Codex (copilot)']
---

# Setup Core Workflow

Run this once per repo to configure the core-workflow agents for your project.

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

### 3. Ensure Repository Ignore Files

Create or update `.gitignore` at the repo root. Preserve existing entries and append the workflow directory if it is missing:

```gitignore
# Agent workflow artifacts
<workflow_dir>/
```

Create or update `{{IGNORE_FILE}}` at the repo root. Preserve existing entries and append these defaults if they are missing. Do not add the workflow directory to `{{IGNORE_FILE}}`; workflow markdown outputs must remain visible to LLMs.

```gitignore
# Dependencies and generated output
node_modules/
dist/
build/
coverage/
.next/
.nuxt/
.svelte-kit/
.vite/
.venv/
venv/
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
target/
bin/
obj/
vendor/

# Binary and archive files
*.7z
*.a
*.bin
*.class
*.dll
*.dmg
*.dylib
*.exe
*.gz
*.iso
*.jar
*.lib
*.o
*.pdf
*.png
*.jpg
*.jpeg
*.gif
*.webp
*.pyc
*.so
*.tar
*.tgz
*.zip

# Logs, caches, and local data
*.log
*.sqlite
*.sqlite3
*.db
.cache/
.DS_Store
```

If the selected workflow directory includes a leading `./`, normalize it to a repo-root relative ignore pattern with one trailing slash for `.gitignore` only, e.g. `AgentWorkflow/`.

### 4. Ensure Project README

If `README.md` does not exist at the repo root, create a comprehensive starter that follows the Documentation Requirements in `{{INSTRUCTIONS_FILE}}`. If it already exists, leave it untouched.

```markdown
# <Project Name>

[One-paragraph description of what this project does and the problem it solves.]

## Features

- [Key capability]

## Prerequisites

- [Required runtimes, tools, and versions]

## Installation

[Step-by-step, isolated setup — containers/virtual envs/`node_modules`; no global installs on the host.]

## Configuration

[Required environment variables and config files, using placeholders like `YOUR_SECRET_HERE`. Never commit real secrets.]

## Usage

[Copy-pasteable commands and examples showing how to run the app and exercise its main features.]

## Testing

\`\`\`bash
<test_command>
\`\`\`

## Project Structure

[Short map of the key directories and their purpose.]

## License

[License, where applicable.]
```

### 5. Write Config

Write `{{CONFIG_PATH}}` at the repo root:

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
Config saved: {{CONFIG_PATH}}
Git ignore updated: .gitignore
Agent ignore updated: {{IGNORE_FILE}}
Project README: README.md

Available agents:
  {{@specifier-grill}}   — alignment, grilling & PRD generation
  {{@specifier-adversary}} — adversarial challenge of alignment
  {{@architect}}          — technical blueprints (vertical slices)
  {{@review-council}}     — plan validation (4 core reviewers)
  {{@executor}}           — phase-by-phase implementation
  {{@orchestrator}}       — build loop (optional)
  {{@prototype}}          — throwaway exploration
  {{@ponytail}}           — lazy senior dev mode

QA agents:
  {{@qa-orchestrator}}  — full QA pipeline
  {{@qa-architect}}     — test plan design
  {{@qa-execution}}     — test execution
  {{@qa-analyzer}}      — results audit
```
