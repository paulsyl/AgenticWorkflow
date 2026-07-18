# QA Workflow Plugin

A black-box QA pipeline for designing, executing, and auditing tests against a live application. Works from PRD/BRD documents without access to source code.

## Skills

| Skill | Description |
|---|---|
| `@qa-orchestrator` | Manages the 3-phase QA pipeline end-to-end |
| `@qa-architect` | Designs a comprehensive test plan from requirements documents |
| `@qa-execution` | Mechanically executes test steps and records observations |
| `@qa-analyzer` | Cross-references expected vs actual behavior to produce audit log |

## Usage

### Full Pipeline
```
@qa-orchestrator
```

### Individual Skills
```
@qa-architect   — generate test plan from PRD
@qa-execution   — execute a test plan against live app
@qa-analyzer    — audit execution logs against expected results
```

## Integration with Core Workflow

This plugin is designed to run after core-workflow's execution phase, as an optional quality gate:

```
core-workflow: Specifier → Architect → Review Council → Executor
                                                            ↓
qa-workflow:                                    QA Architect → QA Execution → QA Analyzer
```

## Configuration

This plugin reads from the `AgentWorkflow/` directory configured by `/setup-core-workflow`. Test artifacts are written to `AgentWorkflow/05_Testing/`.
