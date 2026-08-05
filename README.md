# Agentic Workflow (Single Source of Truth)

A token-optimized, multi-harness software development workflow supporting both **Antigravity & Gemini** and **GitHub Copilot & Visual Studio Code**.

> [!IMPORTANT]
> **Developer Directives: Modifying Agents**
> All agent modifications **MUST** be made exclusively inside the `agents/` directory (e.g., `agents/specifier-grill.md`).
> 
> **NEVER** edit files in `skills/` or `.github/agents/` directly — those are compiled build outputs that will be overwritten.
> 
> After making any change in `agents/`, run `./scripts/deploy.sh` (or `python scripts\compile_and_deploy.py` on Windows) to recompile and redeploy across all target environments.

---

## Architecture: Single Source of Truth (`agents/`)

All agents are defined **once** as canonical master templates in `agents/`. 

```text
AgenticWorkflow/
├── agents/                           # 🎯 SINGLE SOURCE OF TRUTH (Master Templates)
│   ├── specifier-grill.md
│   ├── specifier-adversary.md
│   ├── architect.md
│   ├── review-council.md
│   ├── executor.md
│   ├── orchestrator.md
│   ├── setup-workflow.md
│   ├── prototype.md
│   ├── ponytail*.md
│   └── qa-*.md
├── scripts/
│   ├── compile_and_deploy.py         # 🐍 Cross-OS Compiler & Deployer (macOS, Linux/WSL, Windows)
│   └── deploy.sh                     # 🚀 Single deployment wrapper
├── .gitignore                        # 🛡️ Ignores compiled build outputs (skills/, .github/)
└── README.md
```

---

## 🚀 Deployment & Re-deployment Workflow

When modifying or creating an agent:

1. **Edit**: Make your changes in `agents/<agent-name>.md`.
2. **Deploy**: Run the single deployment script:
   - **macOS / Linux / WSL**: `./scripts/deploy.sh`
   - **Windows Native**: `python scripts\compile_and_deploy.py`

### What Deployment Does Automatically:
1. **Compiles Antigravity Skills**: Generates `skills/<name>/SKILL.md` for Antigravity & Gemini.
2. **Compiles Copilot Agents**: Generates `.github/agents/<name>.agent.md` for GitHub Copilot.
3. **Deploys Globally**:
   - **Antigravity**: Deploys to `~/.gemini/config/skills/` (and `%USERPROFILE%\.gemini\config\skills\` if WSL/Windows).
   - **Copilot**: Deploys to VS Code user prompts, builtin profile agents, and Copilot CLI (`~/.copilot/agents/`).

---

## Available Agents & Skills (17 Total)

### Core Workflow (4-Stage SDLC)

| Agent / Skill | Purpose |
|---------------|---------|
| `specifier-grill` | Adversarial grilling, alignment, and PRD generation — captures scope in conversation |
| `specifier-adversary` | Counter-grilling of alignment summary (pinned to different model family) to break bias |
| `architect` | Translate PRDs into vertical-sliced technical blueprints (`Phase-*.md`) |
| `review-council` | Multi-persona validation (Security & Resilience, Data Integrity, Pragmatism & Scope, Testability) |
| `executor` | Phase-by-phase implementation with escape hatch via `@ponytail` |
| `orchestrator` | Build-loop automation (`architect` → `review-council` → `executor`) |
| `prototype` | Throwaway exploration code — no ceremony |
| `setup-workflow` | Initialize workflow directories and configuration |

### Ponytail (Lazy Senior Dev Mode)

| Agent / Skill | Purpose |
|---------------|---------|
| `ponytail` | Forces simplest solution: YAGNI, stdlib first, minimal code |
| `ponytail-review` | Over-engineering focused code review |
| `ponytail-audit` | Whole-repo audit for complexity |
| `ponytail-debt` | Track deliberate simplifications |
| `ponytail-help` | Quick reference card |

### QA Workflow (Black-Box Testing)

| Agent / Skill | Purpose |
|---------------|---------|
| `qa-orchestrator` | Full QA pipeline |
| `qa-architect` | Design test plans from PRD/BRD (zero codebase access) |
| `qa-execution` | Execute tests against live app, record raw observations |
| `qa-analyzer` | Audit results, produce PASS/FAIL/BLOCKED verdicts |

---

## Workflow Directory Structure

After running setup (`/setup-core-workflow` or `@setup-workflow`):

```text
AgentWorkflow/
├── 01_requirements/
│   └── <phase>/
│       ├── alignment.md    # Self-contained grilling output (scope, glossary, decisions)
│       ├── challenge.md    # Adversary challenge log
│       └── PRD.md          # Immutable requirements contract
├── 02_architecture/
│   └── iterations/<iter>/Phase-*.md
├── 03_reviews/
│   └── <phase>/<iter>/<phase>-review.md
└── 04_execution/
    └── PROGRESS.md
```
