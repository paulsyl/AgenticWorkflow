---
name: ponytail-help
description: Quick-reference card for all ponytail modes, agents, and commands. One-shot display, not a persistent mode.
---

# Ponytail Help

Display this reference card when invoked. One-shot, do NOT change mode, write flag files, or persist anything.

## Levels

| Level | Trigger | What changes |
|-------|---------|--------------|
| **Lite** | `/ponytail lite` | Build what's asked, name the lazier alternative in one line. |
| **Full** | `/ponytail` | The ladder enforced: YAGNI → stdlib → native → one line → minimum. Default. |
| **Ultra** | `/ponytail ultra` | YAGNI extremist. Deletion before addition. Challenges requirements before building. |

Level sticks until changed or session end.

## Agents

| Agent | Trigger | What it does |
|-------|---------|--------------|
| **@ponytail** | `@ponytail` | Lazy mode itself. Simplest solution that works. |
| **@ponytail-review** | `@ponytail-review` | Over-engineering review: `L42: yagni: factory, one product. Inline.` |
| **@ponytail-audit** | `@ponytail-audit` | Whole-repo audit for over-engineering. |
| **@ponytail-debt** | `@ponytail-debt` | List all `ponytail:` comments as a debt ledger. |
| **@ponytail-help** | `@ponytail-help` | This card. |

## Deactivate

Say "stop ponytail" or "normal mode". Resume anytime with `@ponytail`.

## More

Full docs + examples: https://github.com/DietrichGebert/ponytail
