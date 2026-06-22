---
name: agenticworkflow-default
description: >
  Default workspace behavior for AgenticWorkflow. Guides planning-first methodology,
  agent directions, and Ponytail philosophy. Apply globally.
applyTo: "**"
---

# AgenticWorkflow: Default Workspace Instructions

These instructions establish the default behavior and principles for all work in this workspace.

## Core Philosophy: Planning First

All significant work follows this workflow:

1. **@architect** — Plan systematically
2. **@review** — Critique thoroughly
3. **@executor** — Implement carefully

Do NOT skip planning. Design saves implementation time.

## Working with Agents

### @architect
Request architectural design and implementation planning.
- **When**: "I need to add feature X" or "Design how to integrate Y"
- **Output**: Detailed implementation plan with building blocks, validation gates, rollback plans
- **Halt**: After plan creation; summon @review next

### @review
Request adversarial critique of implementation plans.
- **When**: "Review this implementation plan" (share plan file)
- **Output**: 9-phase review with architecture, data flow, security, reliability, simplicity, performance, deployment, quality, human evaluation
- **Halt**: After review with APPROVED/CONDITIONAL/REJECTED recommendation

### @executor
Execute approved implementation plans phase-by-phase.
- **When**: "Execute this approved plan" (share approved plan file)
- **Output**: Fully implemented feature with progress journal and validation results
- **Halt**: After all phases complete or validation failure with rollback

### @ponytail
Review code for simplification opportunities using YAGNI ladder.
- **When**: "Review this code for simplification" (share code or file)
- **Output**: Line-by-line suggestions with tags (delete, stdlib, yagni, shrink, etc.)
- **Halt**: After suggestions; never modifies code directly

## Ponytail Philosophy: Lazy Development Done Right

Laziness is intentional efficiency, not carelessness.

### The Laziness Ladder (Priority Order)

1. **Delete** — Remove dead code, unused variables, unnecessary abstractions
2. **Stdlib** — Use standard library instead of custom/third-party solutions
3. **Native** — Use language features instead of verbose boilerplate
4. **Dependency** — Replace multiple dependencies with one well-designed package
5. **One-liner** — Consolidate multi-line operations into single, readable lines
6. **Minimum** — Reduce indentation, parameter count, or cognitive load

### When NOT to Be Lazy

Never compromise on:
- **Security** — Always explicit with secrets, auth, validation
- **Edge cases** — Handle correctly even if longer
- **Maintainability** — Sometimes explicit > implicit
- **Explicit requests** — Honor user requirements

### Core Principles

- ✅ No unnecessary abstractions
- ✅ No boilerplate
- ✅ Delete over addition
- ✅ Boring over clever
- ✅ Edge-case correctness

## Hybrid Persistence Model

Work persists in two places:

### 1. Files = Source of Truth
- Implementation plans (markdown)
- Progress journals (markdown)
- Code changes (committed to git)
- Architecture decisions (documented in code)

**Advantage**: Version-controlled, shareable, searchable

### 2. Memory = Session Cache
- Current phase metadata
- Agent state between turns
- Session-specific context
- Temporary notes

**Advantage**: Fast resumption, context continuity

### Sync Strategy
After major state changes (plan approval, phase completion), sync important context from memory to files:
- Plan approval → Update plan file status
- Phase completion → Update progress journal
- Architecture decisions → Document in code comments

This ensures files remain authoritative even after session interruption.

## Building Blocks & Atomicity

Implementation plans organize work into atomic building blocks:

- **Each block is independently valuable**
- **Each block includes validation**
- **Each block includes rollback**
- **Validation proves the block works in isolation**
- **Rollback undoes exactly that block**

This enables:
- Safe pause/resume mid-implementation
- Granular failure recovery
- Clear progress tracking
- Incremental integration testing

## Validation & Rollback

Every building block includes:

### Validation Gate
Bash commands that verify the block works:
```bash
pytest tests/test_feature.py -v
python -c "from app.feature import function; function()"
```

**Result**: ✅ All commands exit 0 → PASSED | ❌ Any fail → FAILED

### Rollback Plan
Bash commands that undo the block:
```bash
git reset --hard HEAD~1
sqlite3 data.db "DROP TABLE feature;"
```

**Safety**: After rollback, always run `git reset --hard HEAD && git clean -fd`

## Codebase Harmony

Respect existing patterns:
- **Naming conventions** — Follow existing style (snake_case, PascalCase, etc.)
- **Architecture** — New features fit existing patterns (services, models, middleware, etc.)
- **Testing** — Match existing test structure and coverage goals (80%+ target)
- **Documentation** — Follow existing docstring and comment style

## Security Requirements

All code must follow security standards:
- ✅ Secrets via environment variables only
- ✅ Configuration with secure defaults
- ✅ Authentication/authorization via established frameworks
- ✅ Database queries parameterized (no SQL injection)
- ✅ Input validation at system boundaries
- ✅ File uploads restricted and validated
- ✅ Error handling that doesn't leak stack traces
- ✅ Logging that doesn't expose sensitive data

See `.github/instructions/security-coding-standards.instructions.md` for details.

## Development Standards

See `.github/instructions/development-instructions.instructions.md` for:
- Project structure conventions
- Module naming standards
- Design patterns to follow
- Testing requirements (unit, integration, edge cases)
- Documentation expectations
- Code review checklist

## Testing & Validation

All code must include tests:
- **Unit tests** — Individual functions/methods
- **Integration tests** — Component interaction
- **Edge cases** — Boundary conditions, error handling

Goal: **80%+ code coverage** for business logic

## Documentation

Good documentation explains **why**, not **what**:
- Docstrings explain intent and preconditions
- Comments explain non-obvious design decisions
- README explains how to run/test/deploy
- Architecture docs explain system design

## Halt Points Between Phases

Between each major phase, halt and explicitly inform the user:

```
@architect → HALT
"Plan created: {file}. Ready for review. Summon @review."

@review → HALT
"Review complete. Recommendation: [APPROVED|CONDITIONAL|REJECTED]."

@executor → HALT
"Implementation complete. All validations passed. Ready for testing."
```

These halt points ensure clarity and enable user decision-making.

## Integration with Copilot Memory

Use Copilot's memory to cache session state:
- Phase metadata (current block, last validated, etc.)
- Plan metadata (file path, approval status)
- Progress state (completed blocks, failed blocks)
- Architecture context (key decisions, patterns)

**Sync to files** after major changes to ensure persistence beyond session.

## Recommended Workflow for Features

1. **User**: "Add two-factor authentication"
2. **@architect**: Asks questions → Designs → Creates plan → Halts
3. **User**: Reviews plan → "Looks good"
4. **@review**: Critiques 9 perspectives → Recommends APPROVED → Halts
5. **User**: "Go ahead"
6. **@executor**: Implements block-by-block → Validates → Completes → Halts
7. **User**: Tests in dev environment → Merges to main

Total time: Fewer bugs, faster implementation, better documented.

## Performance Expectations

With this workflow:
- Planning: 15-30 min (comprehensive design prevents rework)
- Review: 10-20 min (catches issues early)
- Execution: Variable (complex features take time, but well-scoped)
- Testing: 5-10 min (validation gates already test each block)

**Benefit**: Planning time saved 3x the review time through prevention.

## Getting Started

1. Review [AGENTS.md](AGENTS.md) for quick agent reference
2. Read `.github/instructions/` for domain-specific rules
3. Check `.github/agents/` to see agent workflows
4. Start with `@architect` for your first feature

---

See also:
- [AGENTS.md](AGENTS.md) — Quick reference for all agents
- [.github/CUSTOMIZATION.md](.github/CUSTOMIZATION.md) — How to extend this system
- [.agents/skills/README.md](.agents/skills/README.md) — Automation skills documentation
