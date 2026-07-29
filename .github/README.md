# Agentic Workflow for GitHub Copilot

A structured, phase-based software development workflow for GitHub Copilot's agent system.

## Quick Start

1. Invoke `@setup-workflow` to configure the workflow for your repository
2. Define your project scope in `AgentWorkflow/00_scope/Project-scope.md`
3. Start with `@specifier-grill` for requirements alignment, or use `@orchestrator` for the full pipeline

## Available Agents

### Core Workflow (4-Stage SDLC)

| Agent | Purpose |
|-------|---------|
| `@orchestrator` | Build-loop automation (architect → review-council → executor). Runs after the specifier loop is complete. |
| `@specifier-grill` | Adversarial grilling to align understanding before planning |
| `@specifier-adversary` | Different-model-family counter-grilling of the alignment summary; runs before the PRD |
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
│   ├── CONTEXT.md          # Domain glossary (built during grilling)
│   └── grilling/           # Confirmed alignment summaries
├── 01_requirements/
│   └── <phase>/PRD.md      # Immutable requirements contracts
├── 02_architecture/
│   ├── System-Architecture.md
│   └── iterations/<iter>/Phase-*.md
├── 03_reviews/
│   └── <phase>/<iter>/<phase>-review.md
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
│  Specifier     │───▶│  Architect      │───▶│  Review Council │───▶│  Executor       │
│  Grill ↔ Adv    │    │  (Blueprints)   │    │  (Validation)   │    │  (Build)        │
│  → PRD          │    └────────────────┘    └────────────────┘    └────────────────┘
└────────────────┘            ▲                       │
                             └───────────────────────┘
                                  (REJECT → iterate)
```

Stage 1 has its own internal loop:

```
@specifier-grill  ──▶  @specifier-adversary  ──▶  @specifier-prd
       ▲                     │
       └────────────────────┘
         (escalation → amend alignment)
```

The adversary runs on a different model family from the grill to break shared model bias.

## When to Use What

| Scenario | Agent(s) |
|----------|----------|
| New major feature | Manual specifier loop (`@specifier-grill` → `@specifier-adversary` → `@specifier-prd`), then `@orchestrator` for the build ceremony |
| Quick bug fix | `@ponytail` directly |
| Explore a design question | `@prototype` |
| Review PR for bloat | `@ponytail-review` |
| Audit entire codebase | `@ponytail-audit` |
| Just the requirements | `@specifier-grill` → `@specifier-adversary` → `@specifier-prd` |
| Stress-test an existing alignment | `@specifier-adversary` |
| Just the architecture | `@architect` |
| Black-box testing | `@qa-orchestrator` (full QA pipeline) |
| Design test cases only | `@qa-architect` |
| Analyze test results | `@qa-analyzer` |

## AI Model Configuration

All agents use **fallback model arrays** to ensure compatibility with your GitHub Copilot subscription. Models are attempted in priority order; the first available model is used.

### Model Strategy

- **Deep reasoning agents** (architect, orchestrator, review-council, specifier-grill): `Claude Sonnet 4.6` → `GPT-5.4` → `GPT-5.3-Codex`
- **Adversary agent** (specifier-adversary): `GPT-5.4` → `GPT-5.3-Codex` — **pinned to a different family from `@specifier-grill`** to break shared model bias when challenging the alignment
- **Builder agents** (executor, prototype): `GPT-5.3-Codex` → `GPT-5.4 mini` → `MAI-Code-1-Flash`
- **Fast/lightweight agents** (ponytail, ponytail-review, ponytail-help): `GPT-5.4 mini` → `MAI-Code-1-Flash` → `GPT-5.3-Codex`
- **QA agents** (qa-architect, qa-analyzer, qa-orchestrator): `GPT-5.4` → `Claude Sonnet 4.6` → `GPT-5.3-Codex`

### Why Fallback Arrays?

- **No single-model dependency**: If a preferred model is unavailable or your plan changes, agents gracefully fall back to the next option.
- **Subscription-safe defaults**: All models in the fallback chains are GA (Generally Available) in standard Copilot Pro and Business plans; no Opus/premium-only models as defaults.
- **Predictable behavior**: The first-available strategy is deterministic and explicit in the agent frontmatter.

### Deployment

Agents are deployed to VS Code and Copilot CLI locations for cross-workspace availability:

```bash
# Deploy to user-level VS Code and Copilot CLI locations
./scripts/deploy-agents.sh
```

This deploys two compatible formats:

- `~/Library/Application Support/Code/User/prompts/agents/` keeps the source `.agent.md` files with model fallback arrays for VS Code.
- `~/Library/Application Support/Code/User/profiles/builtin/agents/` keeps the source `.agent.md` files with model fallback arrays for VS Code profiles.
- `~/.copilot/agents/` receives Copilot CLI-compatible copies where model fallback arrays are converted to scalar model slugs, because the CLI currently rejects array-valued `model` frontmatter.

After deployment, reload VS Code or restart to refresh the agent picker. In Copilot CLI, use `/agent` interactively or `copilot --agent <name>` from the shell.

## Core Principles

- **Security first**: OWASP recommendations, no hardcoded secrets
- **Ponytail philosophy**: The best code is the code never written
- **Vertical slicing**: Each phase delivers a demoable feature, not a horizontal layer
- **Planning mode default**: Never move to build mode without explicit approval
- **Upstream escape hatch**: Max 2 fix attempts before escalating to Architect
