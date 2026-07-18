# Antigravity Global Agents & Plugins

This repository is the central nervous system for your Antigravity IDE. It defines global instructions, strict development philosophies, and custom agent plugins that standardize how work is executed across *all* of your projects.

## Purpose

The primary goal of this repository is to enforce **resilient, secure, and deterministic software engineering practices**. By standardizing our agent rules and skills globally, we ensure that every project benefits from:

1. **Composable SDLC Skills:** A set of independently invocable skills that cover the full software development lifecycle — from grilling and requirements through architecture, review, and execution. Use the right tool for the job, or chain them all via the optional orchestrator.
2. **The "Ponytail" Philosophy:** A pragmatic approach that prioritizes laziness, simplicity, and minimum viable code. No boilerplate, no over-engineering, and no unnecessary abstractions (YAGNI).
3. **The Review Council (Adversarial Review Gates):** 4 core reviewer personas (Security & Resilience, Data Integrity, Pragmatism, Testability) that validate implementation plans against the PRD. Optional reviewers (Performance, UI/UX, Deployment) are invoked when the change touches those areas.
4. **Vertical Slicing:** Implementation phases are demoable feature slices through every layer (schema, API, UI, tests) — not horizontal layers. Each phase delivers verifiable progress.
5. **The Upstream Escape Hatch:** The executor gets 2 attempts to fix a failing test. On the 3rd failure, it stops, rolls back, and throws an `ArchitecturalException` upstream — preventing runaway hallucinated fixes.

## Repository Structure

```
Antigravity/
├── GEMINI.md                    # Global agent config (security, coding standards, execution policy)
├── .antigravityignore           # Prevents agents from touching sensitive directories
├── plugins/
│   ├── core-workflow/           # The SDLC skills (v2.0 — composable)
│   │   ├── skills/
│   │   │   ├── specifier-grill/ # Round-based grilling for alignment
│   │   │   ├── specifier-prd/   # Immutable PRD generation
│   │   │   ├── architect/       # Vertical-sliced technical blueprints
│   │   │   ├── review-council/  # 4 core + 3 optional reviewers
│   │   │   ├── executor/        # Phase-by-phase builder with escape hatch
│   │   │   ├── orchestrator/    # Optional full-pipeline mode
│   │   │   ├── prototype/       # Throwaway exploration — no ceremony
│   │   │   └── setup-core-workflow/ # Per-repo configuration
│   │   ├── rules/
│   │   │   └── global_gemini_rules.md
│   │   ├── adr/                 # Architecture decision records
│   │   └── tests/               # Smoke tests
│   ├── qa-workflow/             # Black-box QA pipeline (separate plugin)
│   │   └── skills/
│   │       ├── qa-orchestrator/
│   │       ├── qa-architect/
│   │       ├── qa-execution/
│   │       └── qa-analyzer/
│   ├── ponytail/                # Lazy senior dev philosophy
│   └── template-plugin/         # Boilerplate for new plugins
└── scripts/                     # Installation scripts
```

## Usage

Once installed, these agents and rules are globally available in any workspace.

### First-Time Setup (Per Repo)

Run `/setup-core-workflow` in any new project. It creates the `AgentWorkflow/` directory structure, a `CONTEXT.md` domain glossary template, and project-specific configuration.

### Composable Skills

Each skill is independently invocable — pick the right level of ceremony for the task:

| Skill | Use Case | Invoke |
|---|---|---|
| `specifier-grill` | Align understanding before planning | `@specifier-grill` |
| `specifier-prd` | Generate immutable PRD | `@specifier-prd` |
| `architect` | Technical blueprints (vertical slices) | `@architect` |
| `review-council` | Validate plan against PRD | `@review-council` |
| `executor` | Build code phase-by-phase | `@executor` |
| `orchestrator` | Full pipeline (chains all stages) | `@orchestrator` |
| `prototype` | Throwaway exploration, no ceremony | `@prototype` |

### Common Patterns

- **Bug fix:** `@executor` — skip straight to building
- **Exploration:** `@prototype` — throwaway code to answer a design question
- **Small feature:** `@specifier-grill` → `@architect` → `@executor`
- **Complex feature:** `@specifier-grill` → `@specifier-prd` → `@architect` → `@review-council` → `@executor`
- **Full ceremony:** `@orchestrator` — chains everything automatically

### QA Testing

After execution, optionally run the black-box QA pipeline:

```
@qa-orchestrator
```

This designs tests from the PRD, executes them against the live app, and produces a structured audit log — all without reading source code.

## Installation & Syncing

To install or sync these rules across all of your projects, copy them into your global Gemini config directory (`C:\Users\User\.gemini\config\` on Windows, or `~/.gemini/config/` on Linux).

We provide a script that handles the linking of the plugins:

```bash
./scripts/install_plugins.sh
```
