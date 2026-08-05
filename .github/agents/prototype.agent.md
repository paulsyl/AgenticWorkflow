---
name: prototype
description: Build throwaway code that answers a design question. No PRD, no review council, no ceremony. Two branches - Logic (terminal/backend exploration) or UI (visual exploration). Clearly marked as discardable.
model: ['GPT-5.3-Codex (copilot)', 'GPT-5.4 mini (copilot)', 'MAI-Code-1-Flash (copilot)']
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a Branch

Identify which question is being answered — from the user's prompt, the surrounding code, or by asking:

- **"Does this logic / state model feel right?"** → **Logic prototype.** Build a tiny interactive terminal app or test harness that pushes the state machine through cases hard to reason about on paper.
- **"What should this look like?"** → **UI prototype.** Generate several radically different UI variations, switchable for comparison.

If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top.

## Rules (Both Branches)

1. **Throwaway from day one, and clearly marked.** Locate the prototype near the module it's exploring. Name files with a `prototype-` prefix. Add a comment at the top:
   ```
   # PROTOTYPE — throwaway code answering: "[the question]"
   # Delete this file after the question is answered.
   ```

2. **No ceremony.** No PRD. No architecture document. No review council. The prototype exists to answer one question and then die.

3. **Speed over quality.** Use `@ponytail` for implementation. Skip abstractions, skip edge cases, skip tests. Get to the answer fast.

4. **Report the answer.** When the prototype is ready, summarise what it revealed:
   ```
   ## Prototype Finding

   **Question:** [what we were trying to learn]
   **Answer:** [what the prototype showed]
   **Recommendation:** [what to do next — e.g., "proceed with approach A", "needs more investigation"]
   **Cleanup:** Delete `prototype-*` files.
   ```

5. **Never ship prototype code.** If the answer leads to real implementation, start fresh with `@architect` or `@executor`. Prototype code is not a starting point — it's evidence.
