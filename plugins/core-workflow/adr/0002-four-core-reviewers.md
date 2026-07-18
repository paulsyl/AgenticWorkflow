# ADR 0002: Four Core Reviewers Over Nine

**Status:** Accepted
**Date:** 2026-07-18

## Context

The original Review Council had 9 specialized personas (Security, Performance, DB Schema, Data Flow, Resilience, Pragmatism, UI/UX, Deployment, QA/SDET). A single LLM was asked to role-play all 9 sequentially.

Problems identified:
- **Synthetic agreement:** After 3-4 personas, the model produces diminishing returns. Later personas rarely surface genuinely new issues because the same weights give 9 opinions.
- **Token cost:** Each review cycle burns the full architecture + PRD context 9 times.
- **No diversity of reasoning:** One model playing 9 roles has no real diversity — it's not equivalent to 9 different human specialists.

## Decision

Collapse to **4 core personas** that always run:
1. 🔒 **Security & Resilience** (merged from Security + Resilience)
2. 🗄️ **Data Integrity** (merged from DB Schema + Data Flow)
3. 🧹 **Pragmatism & Scope** (kept — highest signal-to-noise ratio)
4. 🧪 **Testability** (kept — QA/SDET)

**3 optional personas** invoked only when the change touches their area:
- ⚡ Performance — database queries, scale targets
- 🎨 UI/UX — user-facing changes
- 🚀 Deployment — infra/CI/CD changes

## Consequences

- **Positive:** ~55% reduction in review token cost. Higher signal-to-noise ratio. Core personas cover the most critical cross-cutting concerns.
- **Negative:** Performance, UI/UX, or Deployment issues could slip through if the optional personas aren't invoked when needed. Mitigated by the core 4 flagging when an optional persona should be consulted.
- **Upgrade path:** If multi-model agent orchestration becomes practical (e.g., actual separate model instances for each persona), consider re-expanding to the full set. The optional personas already exist as defined personas that can be promoted back to core.
