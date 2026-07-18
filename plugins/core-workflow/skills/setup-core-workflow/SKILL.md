---
name: setup-core-workflow
description: >
  Per-repo setup skill that configures the core-workflow for a specific project.
  Creates the workflow directory structure, CONTEXT.md template, and writes
  a project-specific config file. Run this once per repo before using the other
  core-workflow skills. Summon via @setup-core-workflow or /setup-core-workflow.
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
mkdir -p <workflow_dir>/00_scope
mkdir -p <workflow_dir>/01_requirements
mkdir -p <workflow_dir>/02_architecture/iterations
mkdir -p <workflow_dir>/03_reviews
mkdir -p <workflow_dir>/04_execution
```

### 3. Create CONTEXT.md Template

Write `<workflow_dir>/00_scope/CONTEXT.md`:

```markdown
# Project Context

## Language

<!-- Add domain-specific terms here during /specifier-grill sessions -->
<!-- Format:
**[Term]**:
[Definition in one or two lines.]
_Avoid_: [synonyms that cause confusion]
-->
```

### 4. Create Project Scope Template (if missing)

If `<workflow_dir>/00_scope/Project-scope.md` doesn't exist, create a template:

```markdown
# Project Scope

## What are we building?
[Describe the feature or project]

## Who is it for?
[Target users]

## What does success look like?
[Measurable outcomes]

## Known constraints
[Budget, timeline, tech stack, team size]
```

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
  @specifier-grill  — alignment & grilling
  @specifier-prd    — PRD generation
  @architect         — technical blueprints (vertical slices)
  @review-council    — plan validation (4 core reviewers)
  @executor          — phase-by-phase implementation
  @orchestrator      — full pipeline (optional)
  @prototype         — throwaway exploration
```
