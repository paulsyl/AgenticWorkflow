# AGENTS: Quick Reference

GitHub Copilot agents in AgenticWorkflow. Use `@agent-name` to summon.

---

## Agent Roster

| Agent | Role | When to Use | Input | Output | Halts After |
|-------|------|-----------|-------|--------|------------|| **@orchestrator** | Automation | "Build feature X end-to-end" | Requirements | Plan → Review → Implementation | Feature complete or blocker found || **@architect** | Planning | "Add feature X" or "Design Y" | Requirements, questions | Implementation plan with building blocks | Plan file created |
| **@review** | Critique | "Review this plan" | Implementation plan file | 9-phase review, APPROVED/CONDITIONAL/REJECTED | Review complete, recommendation given |
| **@executor** | Build | "Execute this plan" | Approved plan file | Implemented feature, progress journal | All blocks complete or validation fails |
| **@ponytail** | Simplify | "Simplify this code" | Code file or snippet | Line-by-line suggestions (YAGNI, stdlib, etc.) | Suggestions output |

---

## Detailed Guide

### @orchestrator: End-to-End Automation Agent

**What it does**: Chains Architect → Review → Executor automatically without halting between phases.

**When to use**:
- "Build a complete payment system"
- "Implement social login feature end-to-end"
- "Autonomously deliver the 2FA feature"
- When you want design through implementation without manual halt points

**What it creates**:
- Implementation plan (Phase 1: Design)
- Reviewed plan with critique notes (Phase 2: Review)
- Fully implemented feature with progress journal (Phase 3: Execute)
- All artifacts created automatically

**Example**:
```
User: "Add two-factor authentication"
@orchestrator:
  1. Phase 1: Asks questions → Designs plan → Creates {feature}_implementation_plan.md
  2. Phase 2: Reviews plan through 9 perspectives → Approves → Updates plan
  3. Phase 3: Executes blocks → Validates → Completes → Creates progress journal
  4. Halts: "Feature delivered. All validation passed. Ready to merge."
```

**Tool restrictions**: Full execution across all phases (read-only during design, full execution during build)

**Halt behavior**: Only halts on completion or critical blocker; no intermediate halt points

**When NOT to use**: Security/compliance-critical changes (use @architect → @review → @executor for human approval gates)

**Next step after**: Review generated code, run full test suite, deploy

---

### @architect: Planning Agent

**What it does**: Designs features systematically, breaks them into phases and building blocks.

**When to use**:
- "Design two-factor authentication for our user system"
- "How should we integrate the payment service?"
- "Create a plan for adding real-time notifications"
- "Design the database schema for feature X"

**What it creates**:
```
{feature}_{phase}_implementation_plan.md
├── Codebase Impact Analysis (High/Medium/Low)
├── Building Blocks (1..N)
│   ├── Code changes
│   ├── Execution steps
│   ├── Code snippets
│   ├── Acceptance criteria
│   ├── Validation gate (bash commands)
│   └── Rollback plan (bash commands)
└── Summary & next steps
```

**Example**:
```
User: "Add JWT authentication"
@architect:
  1. Asks: "What frameworks do you use? ExpireTokenAfter? Refresh tokens?"
  2. Explores: codebase/models/user.py, existing auth service
  3. Plans: 2 phases (backend OTP service + API endpoint)
  4. Creates: `user_jwt_auth_phase1_implementation_plan.md`
  5. Halts: "Plan ready. Summon @review to critique."
```

**Tool restrictions**: Read-only (code search, file exploration)

**Next step after**: Summon `@review`

---

### @review: Adversarial Review Council

**What it does**: Critiques plans using 9 perspectives (Architecture, Data Flow, Security, Reliability, Simplicity, Performance, Deployment, Quality, Human).

**When to use**:
- "Review the JWT auth plan" (share plan file)
- After @architect creates a plan and you want to catch issues early

**The 9 Review Perspectives**:
1. **Architect** — Is the design sound? Does it fit existing patterns?
2. **DataKeeper** — How does data flow? Are boundaries respected?
3. **Guardian** — What are security implications?
4. **Reliability** — How do we handle failures and edge cases?
5. **Minimalist** — Can we do this more simply? YAGNI?
6. **Performance** — Will this be fast enough? N+1 queries?
7. **DevOps** — How do we deploy safely? Can we rollback?
8. **QA** — Is the plan testable? What about regressions?
9. **Human** — Is this ready? Risk/benefit? Any blockers?

**Output for each perspective**:
```
## [Perspective]: [Name]

### Proposal
[What does the plan propose?]

### Attack
[What are the risks or issues?]

### Resolve
[How should the plan address these?]
```

**Final recommendation**: ✅ **APPROVED** | ⚠️ **CONDITIONAL** | ❌ **REJECTED**

**Example**:
```
User: "Review this plan" (shares JWT auth plan)
@review:
  1. Runs through all 9 perspectives
  2. Finds: "OTP expiration not handled, rollback plan missing git operations"
  3. Recommends: CONDITIONAL (needs 2 fixes)
  4. Halts: "Recommendation: CONDITIONAL. Address these issues, then re-summon @review."
```

**Tool restrictions**: Read plan, write suggestions only (no code changes)

**Next steps**:
- If APPROVED: Summon `@executor`
- If CONDITIONAL: Fix issues in plan, re-summon `@review`
- If REJECTED: Revise with `@architect`, re-review

---

### @executor: Implementation Executor

**What it does**: Executes approved plans block-by-block, running validation gates and rollbacks on failure.

**When to use**:
- "Execute this approved plan" (share approved plan file)
- To implement a feature that passed @review

**What it tracks**:
```
{feature}_{phase}_PROGRESS.md
├── Completed blocks (with timestamps, validation results)
├── Current block (with last action, next action for resumption)
├── Failed blocks (with error, rollback status)
└── Notes (deployment blockers, dependencies, etc.)
```

**Execution for each block**:
1. Read execution steps from plan
2. Perform each step
3. Run validation gate (bash commands)
4. Result: ✅ PASS → Mark complete, move next
5. Result: ❌ FAIL → Try ONE fix, revalidate
6. Still failing? → Run rollback plan, HALT with error

**Safety features**:
- Progress journal enables resumption after interruption
- Each block validated independently
- Rollback plan ready for each block
- Auto git safety: `git reset --hard HEAD && git clean -fd` after rollback

**Example**:
```
User: "Execute this JWT auth plan"
@executor:
  1. Block 1: Add OTP field to User model → validates ✅
  2. Block 2: Create OTP service → validates ✅
  3. Block 3: Add API endpoint → validates ✅
  4. All blocks done → Halts: "Implementation complete. Ready for testing."
```

**Tool restrictions**: Full execution capability (read/write/execute/terminal)

**Next steps**:
- Test in development environment
- Deploy to staging
- Merge to main

---

### @ponytail: Code Simplification Reviewer

**What it does**: Reviews code for unnecessary complexity using the Laziness Ladder (delete, stdlib, yagni, shrink, etc.).

**When to use**:
- "Review this code for simplification opportunities"
- After writing a function/module
- Before code review to simplify in advance

**Output format**:
```
L{line}: {tag} {issue}. {replacement}.

L3: delete Unused import requests. Remove: import requests
L12: yagni Constructor has 9 unused parameters. Simplify: def __init__(self, id, email):
L25: shrink Nested loop can be list comprehension. Replace: [item for user in users for item in user.items()]

net: -15 lines possible. Applying these reduces complexity and improves maintainability.
```

**Tags**:
- **delete** — Remove dead code entirely
- **stdlib** — Use standard library instead
- **native** — Use language features instead of boilerplate
- **dependency** — Consolidate dependencies
- **yagni** — Remove unused/unnecessary (YAGNI principle)
- **shrink** — Simplify/condense logic
- **indent** — Reduce nesting

**Example**:
```
User: "Review this code for simplification"
@ponytail:
  L1: delete Unused import logging
  L5: stdlib Use json instead of simplejson
  L15: yagni Remove optional params never used
  L30: shrink Combine two loops
  net: -8 lines possible
```

**Tool restrictions**: Read and suggest only (no code modification)

**Next steps**: Apply suggestions manually or ask @executor to refactor

---

## Workflow: Two Approaches

### Option 1: Autonomous End-to-End (@orchestrator)

```
User: "Build feature X"
@orchestrator:
  → Chains all phases automatically
  → Returns completed feature
  → Halts only on completion or blocker
```

**Use when**: You want autonomous delivery without interruption

---

### Option 2: Manual Three-Phase Flow (with halt points)

### Step 1: Design Phase (@architect)
```
User: "Add social login (Google OAuth)"
@architect: 
  → Asks clarifying questions
  → Explores codebase auth patterns
  → Creates detailed plan with phases
  → Halts: "Plan ready. Summon @review."
```

### Step 2: Review Phase (@review)
```
User: "Review the plan" (shares plan file)
@review:
  → Runs 9-perspective review
  → Identifies issues: "Secret management unclear, PKCE not mentioned"
  → Recommends: CONDITIONAL (2 fixes needed)
  → Halts: "Address these issues, then re-summon @review."
```

### Step 3: Refinement (back to @architect)
```
User: "@architect, let's update the plan for PKCE and secrets via .env"
@architect:
  → Updates plan document
  → Re-summons @review? Or ready?
```

### Step 4: Final Review (@review again)
```
User: "Review again" (shares updated plan)
@review:
  → Re-runs 9-perspective review
  → Issues resolved ✅
  → Recommends: APPROVED
  → Halts: "Plan approved. Ready for implementation. Summon @executor."
```

### Step 5: Implementation Phase (@executor)
```
User: "Let's build it" (shares approved plan)
@executor:
  → Block 1: Database schema → ✅ validated
  → Block 2: OAuth endpoints → ✅ validated
  → Block 3: Frontend integration → ✅ validated
  → All done → Halts: "Implementation complete. Test and deploy."
```

### Step 6: Optional Code Review (@ponytail)
```
User: "Simplify the code before we deploy"
@ponytail:
  → L45: delete Unused UserTokenCache abstraction
  → L78: stdlib Use urllib instead of requests
  → net: -30 lines
  → Halts: Recommendations output
```

---

## Key Principles

### Planning First
Always use @architect before jumping to code. Planning time saves 3x in implementation.

### Halt Points Matter
Each agent halts at a clear decision point. You decide what's next.

### Atomic Blocks
Features break into independently-valuable blocks with validation and rollback.

### Lazy but Right
Use @ponytail to simplify without sacrificing security, edge cases, or clarity.

---

## Quick Command Reference

| Goal | Command |
|------|---------|| Build feature end-to-end (autonomous) | `@orchestrator` → share requirements || Design a feature | `@architect` → share requirements |
| Review a plan | `@review` → share plan file path |
| Implement approved plan | `@executor` → share approved plan file path |
| Simplify code | `@ponytail` → share code file or snippet |
| Resume interrupted work | `@executor` → share plan; it reads progress journal |

---

## Need Help?

- **Understanding agents**: See [copilot-instructions.md](copilot-instructions.md)
- **Extending agents**: See [.github/CUSTOMIZATION.md](.github/CUSTOMIZATION.md)
- **Workflow details**: See `.github/instructions/` directory
- **Automation skills**: See `.agents/skills/README.md`

---

Last updated: $(date)
Repository: AgenticWorkflow
