---
name: core-workflow-base
description: >
  Core Workflow Base Instructions. Use when planning, reviewing, or executing features.
  Establishes the Planning → Review → Execute flow, Ponytail philosophy basics, and strict phase-by-phase methodology.
  Applies globally to all agent work in this project.
applyTo: "**"
---

# Core Workflow: Planning → Review → Execute

These instructions establish the foundation for all feature development in this workspace.

## The Three Phases

Every non-trivial feature follows this sequence:

### Phase 1: The Architect (Planning)
- **Input**: User's feature request
- **Output**: `{feature}_{phase}_implementation_plan.md` with detailed phases
- **Behavior**: Explore codebase, understand patterns, create strict plan
- **Halt**: "Plan created. Summon @review to begin critique."
- **Agent**: `@architect`

### Phase 2: The Review Council (Adversarial Critique)
- **Input**: Implementation plan
- **Output**: Refined plan battle-tested against 9 personas
- **Behavior**: Attack → Resolve loop for each persona
- **Halt**: "Plan finalized. Ready for @executor?"
- **Agent**: `@review`

### Phase 3: The Executor (Implementation)
- **Input**: Approved implementation plan
- **Output**: Working code + progress journal
- **Behavior**: Strict phase-by-phase execution with validation gates and rollback
- **Halt**: "All phases complete. Ready for final testing."
- **Agent**: `@executor`

## When to Use Each Phase

**Never skip phases.**

- **Trivial tasks** (typo fixes, simple file edits): Skip planning, go direct to execution
- **Small features** (one building block, <100 LOC): Can use abbreviated review (3-phase review instead of 9)
- **Major features** (multi-phase, >500 LOC, cross-module): Full pipeline (architect + full review + executor)
- **Architectural changes**: Always full pipeline
- **Security changes**: Always full pipeline (security persona must review)

## Halt & Approval Gates

- **After Architect**: User must summon @review (not automatic)
- **After Review**: User must approve plan and summon @executor (not automatic)
- **After Executor**: User notified; execution is complete

**Exception: @orchestrator agent** can chain all three automatically without halt points (see Orchestrator Mode below).

## Planning Mode Default

For any non-trivial request:
1. Default to planning mode
2. Create/refine implementation plan
3. Do not write code until plan is approved
4. Confirm user intent before proceeding

## Codebase Harmony

All plans must:
- Leverage existing patterns and conventions
- Respect current frameworks and ORMs
- Reuse existing error handling and logging
- Align with current module structure
- Account for technical debt and known limitations

If the plan requires breaking these conventions, explicitly call it out and ask user for confirmation.

## Progress Tracking & Resumption

All multi-phase work creates a progress journal (`{feature}_{phase}_PROGRESS.md`):
- Tracks current phase, last completed action, next action required
- Enables resumption without re-reading the full plan
- Any agent can resume from the **Next Action Required** section

### Hybrid Persistence Model

**Files** = Source of truth:
- Implementation plan (contract)
- Progress journal (execution state)
- Code changes (deliverables)

**Memory** = Session cache:
- Current phase metadata
- Recent decisions
- Plan summary

Memory syncs to file after major state changes.

## Ponytail Philosophy: The Laziness Ladder

Before writing any code, stop at the first rung that holds:

1. **YAGNI**: Does this need to be built at all?
2. **stdlib**: Does the standard library already do this? Use it.
3. **native**: Does a native platform feature cover it? Use it.
4. **dependency**: Does an already-installed dependency solve it? Use it.
5. **one-liner**: Can this be one line? Make it one line.
6. **minimum**: Only then—write the minimum code that works.

### Core Ponytail Rules

- No abstractions that weren't explicitly requested
- No new dependency if avoidable
- No boilerplate nobody asked for
- **Deletion over addition**; boring over clever; fewest files possible
- Pick the edge-case-correct stdlib option (lazy ≠ careless)

## Building Blocks & Atomicity

Implementation plans break features into "Building Blocks":
- Each block is independently testable
- Each block has a validation gate
- Each block can be rolled back cleanly
- Blocks are executed in strict sequence
- No block can break previous blocks

## Validation Gates & Rollback

**Every phase must have**:
- A **Validation Gate** (test commands proving the phase works)
- A **Rollback Plan** (commands to safely revert the workspace)

**Validation gate fails**:
1. Executor attempts ONE autonomous fix
2. If fix succeeds: proceed to next phase
3. If fix fails: automatically rollback entire phase, halt and notify user

## Security & Coding Standards

All code must adhere to `.github/instructions/security-coding-standards.instructions.md`:
- Secret handling (environment variables only)
- Configuration safety (secure defaults)
- Input validation at trust boundaries
- Parameterized queries (no SQL injection)
- No hardcoded secrets, API keys, or credentials

## Documentation & Comments

Every significant module, function, or class must include:
- Docstrings explaining *what* and *why* (not just *what*)
- Inline comments for complex logic
- Examples in docstrings if non-obvious

Avoid comments that restate code ("increment i by 1" for `i += 1`).

## Testing Requirements

All non-trivial code must have:
- Unit tests for core logic
- Integration tests at module boundaries
- Edge case tests
- Security-sensitive operations tested explicitly

Use the standard testing framework for the language/stack.

## Prohibited Behaviors

Agents must **never**:
- Generate insecure code
- Suggest disabling security middleware or checks
- Expose stack traces or internal errors to end users
- Produce harmful, abusive, or discriminatory content
- Generate code violating privacy or data protection laws

## When Unsure

- Ask clarifying questions
- Default to the safest implementation
- Do not assume user intent—ask for confirmation
- Do not proceed without clarity

## Orchestrator Mode

The `@orchestrator` agent chains Architect → Review → Executor automatically without halting between phases. Use when:
- Fully autonomous end-to-end execution desired
- User will not be interrupted during phases
- Plan is well-scoped and low-risk

See `.github/agents/orchestrator.agent.md` for orchestrator mode implementation.

---

See also:
- [AGENTS.md](../AGENTS.md) — Agent descriptions and summoning syntax
- `.github/instructions/ponytail-rules.instructions.md` — Detailed Ponytail philosophy
- `.github/instructions/security-coding-standards.instructions.md` — Security requirements
- `.github/instructions/development-instructions.instructions.md` — Development standards
