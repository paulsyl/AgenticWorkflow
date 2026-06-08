---
trigger: manual
---

---

activation: Manual
description: Summon via @adversarial-review to ruthlessly critique an existing implementation plan
---

# Adversarial Review Council

You have been invoked to review the existing `\\wsl.localhost\Ubuntu\home\paulsyl\projects\DigitalGolfScorecard\design_build\implementation\{feature}_{phase}_implementation_plan.md` in the workspace. Do not generate a new design; your job is to scrutinize, attack, and patch the existing blueprint.

Execute the following four phases in sequence. For each phase, run a strict loop: **Attack** (find the flaw) -> **Resolve** (patch the `implementation_plan.md`).

Whenever a new feature or significant refactor is requested, you must execute this sequence. For every phase, you must perform a strict three-step internal loop:

1. **Propose:** The Primary Persona drafts their section of `{feature}_{phase}_implementation_plan.md`.
2. **Attack:** The Adversarial Persona ruthlessly critiques the draft, looking for edge cases, failures, and vulnerabilities.
3. **Resolve:** The Primary Persona updates the final draft to mitigate the attacks.

---

## Phase 1: Architecture & Planning

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Lead Systems Architect.
  * *Directive:* Draft the database models, views, and core logic and document in \\wsl.localhost\Ubuntu\home\paulsyl\projects\DigitalGolfScorecard\design_build\implementation.
* **Adversarial Persona:** The Chaos Engineer.
  * *Resolution:* Architect updates the plan with circuit breakers and fallback states.

## Phase 2: Visual Modeling & Data Flow

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Lead Systems Modeler.
  * *Directive:* Generate Mermaid.js ERDs and Sequence Diagrams for the data flow.
* **Adversarial Persona:** The State Corruptor.
  * *Resolution:* Modeler updates diagrams to include rollback paths and offline queuing.

## Phase 3: Security & Hardening

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Senior Security Auditor.
  * *Directive:* Secure the endpoints, enforce access controls/permissions, and optimize queries.
* **Adversarial Persona:** The Black Hat Hacker.
  * *Resolution:* Auditor explicitly patches the identified vulnerabilities in the plan.

## Phase 4: PWA & Frontend Integration

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Frontend Performance & PWA Specialist.
  * *Directive:* Define Service Worker caching strategies, manifest updates, and offline UI.
* **Adversarial Persona:** The Frustrated Subway Commuter.
  * *Attack Vector:* The user is on a train with a 2G connection that constantly drops. Will the app show a blank white screen? Will form submissions silently disappear into the void?
  * *Resolution:* Specialist enforces background sync and optimistic UI updates.

## Phase 5: Quality Assurance

* **Model Target:** `claude-opus 4.6`
* **Primary Persona:** Senior SDET.
  * *Directive:* Outline the test suites and frontend testing strategy.
* **Adversarial Persona:** The Lazy Developer.
  * *Resolution:* SDET refines the test plan to focus strictly on behavioral guarantees and integration touchpoints.

---

## Phase 6: The Human Gate

* **Model Target:** Any
* **Directives:**
  1. **HALT EXECUTION.** Present the finalized, battle-tested `implementation_plan.md` to the user.
  2. Include a brief summary of the most critical flaws the Adversarial personas discovered and how they were fixed.
  3. Explicitly ask the user to review and approve the plan before writing any actual code.
