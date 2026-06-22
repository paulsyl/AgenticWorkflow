# AgenticWorkflow: GitHub Copilot Global Agent Framework

An enterprise-grade agentic workflow framework for GitHub Copilot. Combines three specialized agents (Architect → Review Council → Executor) with the "Ponytail" lazy developer philosophy to deliver robust, battle-tested software.

**Purpose**: Standardize how features are planned, reviewed, and implemented across all your projects.

---

## Quick Start

### 1. Install Globally

```bash
cd /Users/paul_sylvester/Development/AgenticWorkflow
./scripts/install-global.sh
```

This creates symlinks in your user-level GitHub Copilot configuration, making agents available in any workspace.

### 2. Use in Any Project

Open any project in VS Code and invoke:

```
@architect
Design a caching layer for the auth system. Current latency: 500ms, target: 100ms.
```

Follow the workflow:
1. **@architect** creates implementation plan
2. **@review** critiques the plan (9-phase adversarial review)
3. **@executor** implements the approved plan with validation gates

### 3. (Optional) Sync to Workspace

For project-specific customization:

```bash
cd /your/project
/path/to/AgenticWorkflow/scripts/sync-workspace.sh
```

This copies agents/instructions to `.github/` for workspace-local override.

---

## Core Components

### Three Specialized Agents

| Agent | Role | Input | Output | Halts? |
|-------|------|-------|--------|--------|
| **@architect** | Planner | Feature request | `{feature}_{phase}_implementation_plan.md` | Yes, after planning |
| **@review** | Critic | Implementation plan | Refined plan + attack/resolution log | Yes, after 9-phase review |
| **@executor** | Builder | Approved plan | Working code + progress journal | Yes, after completion |

### Four Instructions (Always-On)

1. **core-workflow-base** — Planning → Review → Execute flow, halt/approval gates
2. **ponytail-rules** — Lazy developer philosophy (YAGNI, stdlib, deletion)
3. **security-coding-standards** — Security requirements (secrets, validation, auth, database)
4. **development-instructions** — Project structure, testing, documentation

### Python Skills (Portable Automation)

Located in `.agents/skills/core-workflow/`:
- `parse_plan.py` — Extract plan sections
- `execute_validation.py` — Run validation gates
- `rollback_workspace.py` — Revert failed phases
- `update_status.py` — Track progress
- `setup_env.sh` — Configure environment variables

---

## The Workflow: Planning → Review → Execute

### Phase 1: The Architect

**Use case**: You want to plan a feature

```
@architect
Design OAuth 2.0 integration for our mobile app. Replace session-based auth.
Current: Session cookies. Target: Stateless JWT + refresh tokens. Scope: Web API only.
```

**Output**: Structured implementation plan with:
- Codebase Impact Analysis (High/Medium/Low refactoring rating)
- Building Blocks (atomic, independent phases)
- For each block:
  - Execution Steps (exact files to create/modify)
  - Code Snippets (interface specs)
  - Acceptance Criteria (definition of done)
  - Validation Gate (test commands)
  - Rollback Plan (revert commands)

**Halt**: Architect saves plan and halts. User must summon @review.

### Phase 2: The Adversarial Review Council

**Use case**: Plan is ready; you want to catch flaws before coding

```
@review
Review the implementation plan at AgentWorkflow/implementation/oauth_plan.md
```

**Review Process** (9 phases):
1. **Architecture & State** — Chaos engineer attacks for race conditions, coupling
2. **Data Flow & Boundaries** — State corruptor attacks for data validation gaps
3. **Security & Attack Surface** — Security auditor attacks for injection, auth, secrets
4. **Reliability & Error Handling** — SRE attacks for cascading failures, recovery gaps
5. **Simplicity & Pragmatism** — Ponytail attacks for YAGNI, over-engineering, boilerplate
6. **Performance & Resources** — Resource hog attacks for inefficiency, memory leaks
7. **Deployment & Rollback** — Release engineer attacks for atomic operations
8. **Quality & Testability** — SDET attacks for untestable code, missing mocks
9. **Human Gate** — Summarize critical fixes and request approval

For each phase, the review loop:
1. **Propose** — Primary persona reads and proposes updates
2. **Attack** — Adversarial persona finds flaws
3. **Resolve** — Plan is updated to fix flaws

**Output**: Battle-tested plan with documented attacks + resolutions

**Halt**: Review Council halts with: "Plan is ready. Approve for @executor?"

### Phase 3: The Executor

**Use case**: Plan is approved; time to build

```
@executor
Proceed with AgentWorkflow/implementation/oauth_plan.md. I've approved it.
```

**Execution Process** (strict, phase-by-phase):
1. Read building block from plan
2. Execute Execution Steps (create/modify files)
3. Run Validation Gate (test commands)
4. If pass → mark COMPLETE, continue to next block
5. If fail → attempt ONE autonomous fix, re-validate
6. If still fail → automatically rollback entire workspace, halt with details

**Output**: Working code + progress journal (`{feature}_{phase}_PROGRESS.md`)

**Progress Journal**: Single source of truth for execution state
- Enables resumption if interrupted
- Any agent can resume from "Next Action Required"
- Hybrid persistence: Files (source of truth) + Memory (session cache)

**Halt**: Executor halts when all blocks are complete with: "Ready for final testing."

---

## The Ponytail Philosophy: Lazy Senior Developer

Before writing ANY code, stop at the first rung that holds:

1. **YAGNI**: Does this need to be built at all?
2. **stdlib**: Does the standard library already do this? Use it.
3. **native**: Does a native platform feature cover it? Use it.
4. **dependency**: Does an already-installed dependency solve it? Use it.
5. **one-liner**: Can this be one line? Make it one line.
6. **minimum**: Only then—write the minimum code that works.

**Rules**:
- No abstractions without two implementations
- No config that never changes
- Deletion over addition; boring over clever
- Fewest files possible
- Lazy ≠ careless (pick edge-case-correct solutions)

**Used when**: Writing code, reviewing for simplicity, or via `@ponytail` agent.

---

## Repository Structure

```
AgenticWorkflow/
├── .github/
│   ├── agents/                          # Custom agents
│   │   ├── architect.agent.md           # Planning agent
│   │   ├── review.agent.md              # Review agent
│   │   ├── executor.agent.md            # Execution agent
│   │   └── ponytail.agent.md            # Simplification agent
│   └── instructions/                    # Always-on instructions
│       ├── core-workflow-base.instructions.md      # Main workflow
│       ├── ponytail-rules.instructions.md          # Laziness rules
│       ├── security-coding-standards.instructions.md
│       └── development-instructions.instructions.md
├── .agents/
│   └── skills/core-workflow/            # Portable Python automation
│       ├── parse_plan.py                # Parse plan markdown
│       ├── execute_validation.py        # Run validation gates
│       ├── rollback_workspace.py        # Revert changes
│       ├── update_status.py             # Track progress
│       └── setup_env.sh                 # Config helper
├── scripts/
│   ├── install-global.sh                # Global installation
│   └── sync-workspace.sh                # Workspace sync
├── .antigravityignore                   # Global ignore patterns
├── copilot-instructions.md              # Root-level defaults
├── AGENTS.md                            # Agent quick reference
└── README.md                            # This file
```

---

## Installation Options

### Option A: Global Installation (Recommended)

Makes agents available in **all** projects:

```bash
cd /Users/paul_sylvester/Development/AgenticWorkflow
./scripts/install-global.sh
```

Agents are installed to: `~/Library/Application Support/Code/User/prompts/copilot-antigravity/`

✅ **Pros**: Cross-project reuse, automatic updates via symlinks
❌ **Cons**: Requires explicit global setup

### Option B: Workspace-Local

Create `.github/` in your project root:

```bash
cd /your/project
/path/to/AgenticWorkflow/scripts/sync-workspace.sh
```

This copies agents/instructions to `.github/` for project-specific customization.

✅ **Pros**: Project-specific overrides, version control, team sharing
❌ **Cons**: Duplicated files if using in many projects

### Option C: Both (Hybrid)

Install globally for default behavior, then override specific agents/instructions in `.github/` for project-specific needs.

**Workspace files take precedence over global files.**

---

## Memory & Session Persistence

### Hybrid Persistence Model

**Files** (source of truth):
- Implementation plan (`{feature}_{phase}_implementation_plan.md`)
- Progress journal (`{feature}_{phase}_PROGRESS.md`)
- Code changes (your codebase)

**GitHub Copilot Memory** (session cache):
- Current phase metadata
- Recent decisions
- Plan summary for quick lookup

**How it works**:
1. Executor reads progress journal from file
2. Caches current phase in memory for fast access
3. After each major state change, syncs back to file
4. If session ends, next agent reads from file and rebuilds memory

**Resumption**: Any agent can resume work by reading the progress journal's "Next Action Required" section.

---

## Security Requirements (Built-In)

All code must adhere to:

- ✅ **Secrets**: Environment variables only (never hardcoded)
- ✅ **Validation**: Input validation at all trust boundaries
- ✅ **Auth/Authz**: Established frameworks, no custom password hashing
- ✅ **Database**: Parameterized queries, no raw SQL without ORM
- ✅ **CORS/Cookies**: Secure defaults (HttpOnly, Secure, SameSite)
- ✅ **Errors**: No stack traces leaked to users

See `.github/instructions/security-coding-standards.instructions.md` for details.

---

## Customization

### Adding a New Agent

1. Create `.github/agents/my-agent.agent.md`
2. Define YAML frontmatter: `name`, `description`, `applyTo`
3. Add agent instructions in markdown
4. Test by summoning `@my-agent`

See `.github/CUSTOMIZATION.md` for detailed guide.

### Adding a New Instruction

1. Create `.github/instructions/my-rules.instructions.md`
2. Define YAML frontmatter: `name`, `description`, `applyTo` (file glob pattern)
3. Add rule content in markdown
4. Instruction auto-applies to matching files

### Creating Custom Skills

1. Create `.agents/skills/my-skill/`
2. Add Python/bash scripts (portable, environment-agnostic)
3. Create `.agents/skills/my-skill/SKILL.md` documentation
4. Reference in executor or custom agent

---

## Troubleshooting

### Agents not appearing in Copilot

- Run `./scripts/install-global.sh` to install globally
- Or copy `.github/` to your project for workspace-local setup
- Restart VS Code after installation

### YAML frontmatter errors

- Ensure `name` field matches file name (e.g., `architect.agent.md` → `name: architect`)
- Quote descriptions containing colons: `description: "Use when: planning"`
- Use 2-space indentation (not tabs)

### Skills not executing

- Verify Python 3 and Bash are available
- Check file permissions: `chmod +x .agents/skills/core-workflow/*.py`
- Set up environment: `source .agents/skills/core-workflow/setup_env.sh`
- Test manually: `python parse_plan.py your-plan.md`

### Progress journal not syncing

- Verify executor has write permissions to directory
- Check that plan file path is correct
- Ensure plan follows standard format (level-2 headers for building blocks)

---

## Advanced Usage

### Chaining with Orchestrator (Future)

Future version will support `@orchestrator` agent that automatically chains:
Architect → Review → Executor without halting between phases.

### Integration with Your Build System

Custom hooks can integrate Copilot workflows with your CI/CD:
- Auto-trigger validation gates in your build pipeline
- Create deployment tickets after executor completes
- Notify team of plan approvals

---

## Contributing & Extending

Want to add features to AgenticWorkflow?

1. Fork the repository (or create a branch in your workspace)
2. Add new agents/skills/instructions to `.github/` or `.agents/skills/`
3. Test locally
4. Update documentation
5. Run global install to use updated version: `./scripts/install-global.sh`

---

## Design Philosophy

AgenticWorkflow embodies these principles:

1. **Planning First** — Design before coding; catch flaws early
2. **Adversarial Review** — 9-persona review council attacks plans from every angle
3. **Deterministic Execution** — Strict phase-by-phase execution with validation and rollback
4. **Ponytail Laziness** — Minimum viable code, stdlib first, deletion over addition
5. **Resumable Progress** — Progress journals enable resumption after interruption
6. **Portable Skills** — Python automation scripts work in any tech stack
7. **Global & Local** — Install globally for all projects, override locally for customization

---

## Related Documentation

- **AGENTS.md** — Quick reference for all agents
- **.github/CUSTOMIZATION.md** — Deep dive into extending agents/instructions
- **.github/instructions/** — Four core instruction files
- **.agents/skills/README.md** — Skill documentation and usage
- **copilot-instructions.md** — Workspace-level defaults

---

## Support & Questions

For issues or questions:
1. Check `.github/CUSTOMIZATION.md` for customization help
2. Review `.agents/skills/README.md` for skill troubleshooting
3. See specific instruction files for detailed rules

---

**Version**: 1.0.0  
**Last Updated**: 2026-06-22  
**License**: MIT (feel free to customize for your projects)
