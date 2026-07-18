# ADR 0001: Composable Skills Over Monolithic Pipeline

**Status:** Accepted
**Date:** 2026-07-18

## Context

The original core-workflow enforced a rigid 4-stage pipeline (Specifier → Architect → Review Council → Executor) that all work had to pass through. Benchmarking against industry best practice (mattpocock/skills, Anthropic's agent patterns) revealed this creates ceremonial overhead for the 80% of tasks that don't need the full ceremony.

## Decision

Each stage is now an **independently invocable skill** with a proper SKILL.md file. The orchestrator exists as an **optional** skill that chains all stages together — it is not the default entry point.

- Bug fixes and small changes can go directly to `@executor`.
- Exploratory work uses `@prototype` with zero ceremony.
- Complex features use the full pipeline via `@orchestrator`.

## Consequences

- **Positive:** Engineers choose the right level of ceremony per task. Token cost scales with task complexity. Individual skills can be tested and improved independently.
- **Negative:** Engineers must make a judgment call about which skill to invoke. Risk of skipping important stages on tasks that actually need them. Mitigated by the "never move to build mode unless explicitly asked" global rule, which prevents the agent from autonomously skipping review.
- **Trade-off:** The "never move to build" safety rail in `global_gemini_rules.md` stays. The agent will always default to planning mode. The composability is for the *human* to decide when to skip stages, not the agent.
