# Agentic Workflow (Single Source of Truth)

A token-optimized, multi-harness software development workflow supporting both **Antigravity & Gemini** and **GitHub Copilot & Visual Studio Code**.

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
├── skills/                           # ⚙️ Compiled Antigravity Skills (skills/<name>/SKILL.md)
├── .github/agents/                   # ⚙️ Compiled Copilot Agents (.github/agents/<name>.agent.md)
├── scripts/
│   ├── compile_and_deploy.py         # 🐍 Cross-OS Compiler & Deployer (macOS, Linux/WSL, Windows)
│   └── deploy.sh                     # 🚀 Single deployment wrapper
└── README.md
```

---

## 🚀 Deployment (Cross-OS Support)

A single deployment command compiles the master templates from `agents/` into target-specific formats and deploys them to all detected user profile locations across **macOS**, **Linux / WSL Ubuntu**, and **Windows Native (CMD / PowerShell)**.

### macOS / Linux / WSL:
```bash
./scripts/deploy.sh
```

### Windows Native (PowerShell / CMD):
```powershell
python scripts\compile_and_deploy.py
```

### What Deployment Does Automatically:
1. **Compiles Antigravity Skills**: Generates `skills/<name>/SKILL.md` for Antigravity & Gemini.
2. **Compiles Copilot Agents**: Generates `.github/agents/<name>.agent.md` for GitHub Copilot.
3. **Deploys Globally**:
   - **Antigravity**: Deploys to `~/.gemini/config/skills/` (and `%USERPROFILE%\.gemini\config\skills\` if WSL/Windows).
   - **Copilot**: Deploys to VS Code user prompts, builtin profile agents, and Copilot CLI (`~/.copilot/agents/`).

---

## Available Agents & Skills (18 Total)

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
