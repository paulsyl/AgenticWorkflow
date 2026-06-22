# AgenticWorkflow Skills & Automation

This directory contains portable Python and shell scripts used by the Executor agent to parse implementation plans, run validation gates, rollback workspaces, and track progress.

## Core-Workflow Skills

### `parse_plan.py`

Extract structured data from an implementation plan markdown file.

**Purpose**: Parse the implementation plan and extract sections (execution steps, code snippets, validation gates, rollback plans) for the executor to use.

**Usage**:
```bash
# Extract full plan as JSON
python parse_plan.py auth_caching_plan.md

# Extract just execution steps
python parse_plan.py auth_caching_plan.md step

# Extract just code snippets
python parse_plan.py auth_caching_plan.md snip

# Extract just validation gate
python parse_plan.py auth_caching_plan.md val

# Extract just rollback plan
python parse_plan.py auth_caching_plan.md roll
```

**Output** (full JSON mode):
```json
{
  "title": "User Authentication Implementation Plan",
  "filename": "auth_plan.md",
  "status": "pending",
  "validation_gate": "pytest tests/auth/...",
  "rollback_plan": "git reset --hard HEAD",
  "building_blocks": [
    {
      "name": "JWT Token Service",
      "execution_steps": "1. Create src/auth/jwt_service.py\n2. ...",
      "snippets": [
        {
          "label": "JWT Service Interface",
          "language": "python",
          "code": "class JWTService:\n  def generate_token(...)..."
        }
      ]
    }
  ]
}
```

### `execute_validation.py`

Run validation gate commands from an implementation plan and capture results.

**Purpose**: Execute all bash commands in the "Validation Gate" section of the plan. Used by the executor to verify that a building block is complete and working.

**Usage**:
```bash
python execute_validation.py auth_caching_plan.md
```

**Output**:
```json
{
  "success": true,
  "results": [
    {
      "command": "pytest tests/auth/test_jwt_service.py -v",
      "success": true,
      "stdout": "PASSED",
      "stderr": ""
    }
  ]
}
```

**Exit Code**:
- 0 = All validations passed
- 1 = One or more validations failed

### `rollback_workspace.py`

Execute rollback commands and reset workspace to clean state.

**Purpose**: Safely revert all changes made during a building block execution. Used when a validation gate fails and the executor needs to rollback.

**Usage**:
```bash
# With plan file (runs explicit rollback commands + git reset)
python rollback_workspace.py auth_caching_plan.md

# Without plan file (just git reset)
python rollback_workspace.py
```

**Output**:
```json
{
  "success": true,
  "results": [
    {
      "command": "python manage.py migrate auth 0001",
      "success": true,
      "stdout": "Migrated to 0001",
      "stderr": ""
    },
    {
      "command": "git reset --hard HEAD",
      "success": true,
      "stdout": "HEAD is now at ...",
      "stderr": ""
    },
    {
      "command": "git clean -fd",
      "success": true,
      "stdout": "Removing ...",
      "stderr": ""
    }
  ]
}
```

**Safety**: Always performs `git reset --hard HEAD` and `git clean -fd` as final safety measure, even if explicit rollback commands fail.

### `update_status.py`

Update the progress journal markdown file with execution state.

**Purpose**: Maintain the progress journal (single source of truth for execution state) so that any agent can resume after interruption.

**Usage**:
```bash
python update_status.py PROGRESS.md 1 COMPLETE "Created CacheManager class"
python update_status.py PROGRESS.md 2 IN_PROGRESS "Starting OAuth integration"
python update_status.py PROGRESS.md 3 FAILED "Validation gate failed: pytest returned 1"
```

**Status Values**:
- `IN_PROGRESS` — Currently executing this phase
- `COMPLETE` — Phase succeeded
- `FAILED` — Phase failed validation
- `ROLLED_BACK` — Phase was rolled back due to failure

### `setup_env.sh`

Source this script before manually running skills to configure environment variables.

**Usage**:
```bash
source setup_env.sh

# Now you can run skills manually:
python parse_plan.py $PLAN_FILE
python execute_validation.py $PLAN_FILE
```

**Environment Variables Set**:
- `PROJECT_ROOT` — Project root directory (defaults to `.`)
- `PLAN_FILE` — Path to implementation plan (defaults to `$PROJECT_ROOT/implementation_plan.md`)
- `PROGRESS_FILE` — Path to progress journal (defaults to `$PROJECT_ROOT/PROGRESS.md`)
- `LAUNCH_CMD` — Command to launch the app (auto-detected from docker-compose.yml, manage.py, package.json, go.mod, or user-specified)

---

## Plan File Format

All scripts expect implementation plans to follow this structure:

```markdown
# {feature}_{phase}_implementation_plan.md

## Overview
...

## Building Block 1: {Name}

### 1. Codebase Impact Analysis
...

### 2. Execution Steps
1. Create src/auth/cache.py
2. Run migrations
...

### 3. Code Snippets

**Interface (src/auth/cache.py)**:
```python
class CacheManager:
    def get(self, key): pass
```

### 4. Acceptance Criteria
...

### 5. Validation Gate
```bash
pytest tests/auth/test_cache.py -v
python -c "from src.auth.cache import CacheManager; ..."
```

### 6. Rollback Plan
```bash
git checkout src/auth/cache.py
python manage.py migrate auth 0001
```

## Building Block 2: ...
```

---

## Progress Journal Format

Scripts maintain a progress journal to enable resumption:

```markdown
# Execution Progress Journal

**Plan**: {feature}_{phase}_implementation_plan.md
**Started**: 2026-06-22T14:30:00Z
**Last Updated**: 2026-06-22T14:35:00Z
**Executing Agent**: Claude Opus

## Overall Status
- [x] Building Block 1 — JWT Service
- [ ] Building Block 2 — Middleware Integration

## Current Phase
**Phase**: 2 — Middleware Integration
**Status**: IN_PROGRESS

## Last Completed Action
Created CacheManager class with get/set methods; all unit tests passed.

## Next Action Required
Integrate CacheManager into auth middleware. Update src/middleware/auth.py to use CacheManager().get() for token caching.

## Files Modified This Session
- src/auth/cache.py — Created CacheManager class
- tests/auth/test_cache.py — Created unit tests

## Failures & Decisions
- Phase 1 validation initially failed: missing __init__ method in CacheManager
- Fixed: Added self._cache = {} initialization
- Revalidated: All tests passed
```

---

## Usage from GitHub Copilot

These scripts are invoked automatically by the `@executor` agent. You don't need to run them manually unless testing.

However, you can run them manually for debugging:

```bash
# Setup environment
cd /Users/paul_sylvester/Development/AgenticWorkflow
source .agents/skills/core-workflow/setup_env.sh

# Parse a plan
python .agents/skills/core-workflow/parse_plan.py $PLAN_FILE

# Run validation
python .agents/skills/core-workflow/execute_validation.py $PLAN_FILE

# Update progress
python .agents/skills/core-workflow/update_status.py $PROGRESS_FILE 1 COMPLETE "Phase 1 done"

# Rollback if needed
python .agents/skills/core-workflow/rollback_workspace.py $PLAN_FILE
```

---

## Integration with Other Projects

These skills are **portable** and **language-agnostic**:

1. Copy `.agents/skills/core-workflow/` to any project
2. Copy `.github/instructions/` to any project (customize as needed)
3. Source `setup_env.sh` to configure paths
4. Skills work with any tech stack (Python, Node.js, Go, etc.)

The scripts only assume:
- Bash is available
- Python 3 is available
- Git is available
- Implementation plan follows the standard format

---

## Troubleshooting

### parse_plan.py returns empty results
- Verify plan file uses level-2 headers (`## Building Block 1:`)
- Verify code snippets are in triple-backticks with language specified

### execute_validation.py fails
- Check that all commands in Validation Gate section are valid bash
- Verify dependencies are installed (pytest, npm, etc.)
- Try running the command manually to debug

### rollback_workspace.py can't find git
- Ensure project is a git repository (`git init` if needed)
- Verify git is in PATH (`which git`)

### Progress journal not updating
- Verify `update_status.py` has write permissions to the file
- Check that progress file path is correct
- Verify JSON status is valid (COMPLETE, FAILED, IN_PROGRESS, ROLLED_BACK)

---

See also:
- `.github/agents/executor.agent.md` — Executor agent documentation
- `AGENTS.md` — Agent descriptions and usage
