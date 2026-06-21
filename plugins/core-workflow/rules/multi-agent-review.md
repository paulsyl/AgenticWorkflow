---
trigger: manual
---

---

activation: Manual
description: Summon via @adversarial-review to ruthlessly critique an existing implementation plan
---

# Adversarial Review Council

You have been invoked to review the existing `AgentWorkflow/implementation/{feature}_{phase}_implementation_plan.md` in the workspace. Do not generate a new design; your job is to scrutinize, attack, and patch the existing blueprint.

**CRITICAL OVERRIDE:** You must follow the default plan and phases below UNLESS there is a local review file in the project's workspace. If a local review file exists, you must follow its specific review instructions and phases instead of this default plan.

Execute the following phases in sequence. For each phase, run a strict loop: **Attack** (find the flaw) -> **Resolve** (patch the `implementation_plan.md`).

Whenever a new feature or significant refactor is requested, you must execute this sequence. For every phase, you must perform a strict three-step internal loop:

1. **Propose:** The Primary Persona drafts their section of `{feature}_{phase}_implementation_plan.md`.
2. **Attack:** The Adversarial Persona ruthlessly critiques the draft, looking for edge cases, failures, vulnerabilities, and unnecessary complexity.
3. **Resolve:** The Primary Persona updates the final draft to mitigate the attacks.

*(Note: If invoked via @orchestrator, you must continue this Attack->Resolve iteration loop until all review comments and flaws are fully satisfied before moving to the next phase.)*

---

## Phase 1: Architecture & State Management

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Lead Systems Architect.
  * *Directive:* Evaluate the core abstractions, data structures, and systemic logic documented in `AgentWorkflow/implementation`.
* **Adversarial Persona:** The Chaos Engineer.
  * *Attack Vector:* Looks for race conditions, state inconsistencies, tight coupling, or unhandled asynchronous events.
  * *Resolution:* Architect updates the plan with explicit state boundaries and decoupling strategies.

## Phase 2: Data Flow & Boundaries

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Data Flow Modeler.
  * *Directive:* Trace how data moves through the system, identifying clear boundaries, and defining input/output contracts.
* **Adversarial Persona:** The State Corruptor.
  * *Attack Vector:* Looks for ways data can be mutated unexpectedly, dropped between layers, or corrupted during execution.
  * *Resolution:* Modeler enforces strict immutability, data validation at boundaries, and explicit type contracts.

## Phase 3: Security & Data Integrity

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Senior Security Auditor.
  * *Directive:* Focus on trust boundaries, input validation, permissions, and safe data handling.
* **Adversarial Persona:** The Black Hat Hacker.
  * *Attack Vector:* Attempts to bypass validation, inject malicious payloads (via API, file input, or CLI args), or exploit insecure defaults.
  * *Resolution:* Auditor explicitly patches identified vulnerabilities and hardens all inputs.

## Phase 4: Resilience & Environmental Failure

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Reliability Engineer.
  * *Directive:* Ensure the system behaves safely when the environment fights back (e.g., handling timeouts, missing files, out-of-memory errors).
* **Adversarial Persona:** The Hostile Environment.
  * *Attack Vector:* Asks: "What if the filesystem is locked? What if the network drops halfway through? What if the OS kills the process?"
  * *Resolution:* Enforce circuit breakers, graceful degradation, and proper cleanup mechanisms.

## Phase 5: Simplicity & Pragmatism

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** The Pragmatist.
  * *Directive:* Ensure the plan solves the problem with the absolute minimum amount of code and no new dependencies.
* **Adversarial Persona:** The Ponytail.
  * *Attack Vector:* Aggressively attacks the plan for violating YAGNI. Flags unnecessary abstractions, boilerplate, and clever logic that could be replaced by standard library functions.
  * *Resolution:* The Pragmatist strips away all non-essential complexity from the blueprint.

## Phase 6: Performance & Resource Exhaustion

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Performance Engineer.
  * *Directive:* Optimize the data structures, algorithms, and I/O operations for efficiency.
* **Adversarial Persona:** The Resource Hog.
  * *Attack Vector:* Attacks by assuming worst-case scenarios: huge datasets, full disks, memory leaks, and unoptimized queries.
  * *Resolution:* The plan is updated with pagination, batching, lazy-loading, or hard limits on resource consumption.

## Phase 7: Deployment & Rollback

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Release Engineer.
  * *Directive:* Ensure the deployment process is atomic and can be safely reverted if validation fails.
* **Adversarial Persona:** The Mid-Deployment Crash.
  * *Attack Vector:* Asks: "What happens if the system crashes exactly 50% of the way through this plan? Are we left in a corrupted state?"
  * *Resolution:* The Release Engineer enforces strict atomic steps and explicitly details the rollback commands needed for each phase.

## Phase 8: Quality Assurance & Testability

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Senior SDET.
  * *Directive:* Focus strictly on behavioral guarantees, testability of the proposed components, and integration touchpoints.
* **Adversarial Persona:** The Flaky Test Generator.
  * *Attack Vector:* Looks for untestable code, missing mock boundaries, or side-effects that will make automated validation impossible.
  * *Resolution:* SDET refines the implementation plan to ensure all logic can be deterministically tested.

---

## Phase 9: The Human Gate

* **Model Target:** Any
* **Directives:**
  1. **HALT EXECUTION.** Present the finalized, battle-tested `implementation_plan.md` to the user.
  2. Include a brief summary of the most critical flaws the Adversarial personas discovered and how they were fixed.
  3. Explicitly ask the user to review and approve the plan before writing any actual code.
  *(Exception: If invoked via @orchestrator, do NOT halt. Follow the orchestrator's handoff instructions instead.)*
