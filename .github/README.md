# Agentic Workflow for GitHub Copilot

A structured, phase-based software development workflow adapted for GitHub Copilot. Originally designed for Google Antigravity IDE, now fully compatible with GitHub Copilot's agent system.

## Quick Start

1. Invoke `@setup-workflow` to configure the workflow for your repository
2. Define your project scope in `AgentWorkflow/00_scope/Project-scope.md`
3. Start with `@specifier-grill` for requirements alignment, or use `@orchestrator` for the full pipeline

## Available Agents

### Core Workflow (4-Stage SDLC)

| Agent | Purpose |
|-------|---------|
| `@orchestrator` | Full pipeline automation — chains all stages autonomously |
| `@specifier-grill` | Adversarial grilling to align understanding before planning |
| `@specifier-prd` | Generate immutable Product Requirements Documents |
| `@architect` | Translate PRDs into vertical-sliced technical blueprints |
| `@review-council` | Multi-persona validation (Security, Data, Pragmatism, Testability) |
| `@executor` | Phase-by-phase implementation with escape hatch |
| `@prototype` | Throwaway exploration code — no ceremony |

### QA Workflow (Black-Box Testing)

| Agent | Purpose |
|-------|---------|
| `@qa-orchestrator` | Full QA pipeline — chains architect → execution → analyzer |
| `@qa-architect` | Design test plans from PRD/BRD (zero codebase access) |
| `@qa-execution` | Execute tests against live app, record raw observations |
| `@qa-analyzer` | Audit results, produce PASS/FAIL/BLOCKED verdicts |

### Ponytail (Lazy Senior Dev Mode)

| Agent | Purpose |
|-------|---------|
| `@ponytail` | Forces simplest solution: YAGNI, stdlib first, minimal code |
| `@ponytail-review` | Over-engineering focused code review |
| `@ponytail-audit` | Whole-repo audit for complexity |
| `@ponytail-debt` | Track deliberate simplifications |
| `@ponytail-help` | Quick reference card |

### Setup

| Agent | Purpose |
|-------|---------|
| `@setup-workflow` | Initialize workflow directories and configuration |

## Workflow Directory Structure

After running `@setup-workflow`:

```
AgentWorkflow/
├── 00_scope/
│   ├── Project-scope.md    # Your project description
│   └── CONTEXT.md          # Domain glossary (built during grilling)
├── 01_requirements/
│   └── <phase>/PRD.md      # Immutable requirements contracts
├── 02_architecture/
│   ├── System-Architecture.md
│   └── iterations/<iter>/Phase-*.md
├── 03_reviews/
│   └── review_log.md
├── 04_execution/
│   └── PROGRESS.md
└── 05_Testing/
    ├── test_plan.json      # QA Architect output
    ├── execution_log.json  # QA Execution output
    └── audit_log.json      # QA Analyzer output
```

## The 4-Stage Pipeline

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  STAGE 1        │    │  STAGE 2        │    │  STAGE 3        │    │  STAGE 4        │
│  Specifier      │───▶│  Architect      │───▶│  Review Council │───▶│  Executor       │
│  (Grill + PRD)  │    │  (Blueprints)   │    │  (Validation)   │    │  (Build)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
                              ▲                       │
                              └───────────────────────┘
                                  (REJECT → iterate)
```

## When to Use What

| Scenario | Agent(s) |
|----------|----------|
| New major feature | `@orchestrator` (full ceremony) |
| Quick bug fix | `@ponytail` directly |
| Explore a design question | `@prototype` |
| Review PR for bloat | `@ponytail-review` |
| Audit entire codebase | `@ponytail-audit` |
| Just the requirements | `@specifier-grill` → `@specifier-prd` |
| Just the architecture | `@architect` |
| Black-box testing | `@qa-orchestrator` (full QA pipeline) |
| Design test cases only | `@qa-architect` |
| Analyze test results | `@qa-analyzer` |

## Core Principles

- **Security first**: OWASP recommendations, no hardcoded secrets
- **Ponytail philosophy**: The best code is the code never written
- **Vertical slicing**: Each phase delivers a demoable feature, not a horizontal layer
- **Planning mode default**: Never move to build mode without explicit approval
- **Upstream escape hatch**: Max 2 fix attempts before escalating to Architect
