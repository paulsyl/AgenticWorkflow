# ADR 0003: Vertical Slicing as Default Phase Strategy

**Status:** Accepted
**Date:** 2026-07-18

## Context

The original Architect produced `Phase-*.md` files as **horizontal layers** (Phase 1: Database, Phase 2: API, Phase 3: UI). This meant Phase 1 couldn't be demo'd or tested end-to-end without Phase 2 and 3.

Industry best practice (tracer bullet development, mattpocock/skills `/to-tickets`) strongly favours vertical slices.

## Decision

Phases default to **vertical slices** — each phase cuts a narrow but complete path through every layer (schema, API, service, UI, tests).

- A completed phase is demoable or verifiable on its own.
- Each phase is sized to fit in a single agent context window.
- Prefactoring gets its own early phase.
- **Wide refactors are the exception:** A mechanical change whose blast radius fans across the whole codebase (rename a column, retype a shared symbol) uses expand-contract rather than vertical slicing.

## Consequences

- **Positive:** Each phase delivers visible, testable progress. Failures are localised to one feature slice, not one layer across all features. The Upstream Escape Hatch is more useful — if Phase N fails, only one feature is blocked, not an entire layer.
- **Negative:** Vertical slicing requires more architectural thought — the Architect must understand all layers, not just one. Some changes genuinely are horizontal (schema migrations, shared type changes) and must be handled as exceptions.
- **Trade-off:** The Architect prompt now includes explicit guidance for both vertical slices (default) and the expand-contract pattern (exception for wide refactors).
