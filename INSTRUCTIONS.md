---
description: This document defines how AI coding assistants should behave when assisting with this software project. The goal is to ensure **secure**, **maintainable**, and **production‑ready** code while preventing unsafe or harmful patterns.
applyTo: '**'
---

# Software Development Instructions

## Core Principles

- Always prioritise **security**, **data protection**, and **privacy**.
- Default to **industry best practices** and **OWASP recommendations**.
- Avoid generating code that exposes secrets, credentials, or sensitive logic.
- Prefer clarity and maintainability over cleverness or shortcuts.
- **No software may be installed directly on this machine.** You must use appropriate repository safeguards (e.g., Docker containers, virtual environments, or `node_modules`) to isolate all tools, dependencies, and execution environments.

---

## Agent & Skill Modification Policy (CRITICAL)

- **Single Source of Truth**: All workflow agents, skills, and prompts **MUST** be edited exclusively in the `agents/` directory (e.g., `agents/specifier-grill.md`).
- **Never edit compiled outputs directly**: Do not modify files in `skills/` or `.github/agents/` — those are compiled build artifacts that will be overwritten.
- **Redeployment**: After modifying any file in `agents/` or `INSTRUCTIONS.md`, run `./scripts/deploy.sh` (or `python scripts\compile_and_deploy.py` on Windows) to recompile and deploy across all target environments.

---

## Security Requirements

### 1. Secret Handling

- Never hard‑code secrets, API keys, passwords, tokens, or database credentials.
- Always use environment variables or secure configuration management.
- When generating examples, use placeholders like `"YOUR_SECRET_HERE"`.

### 2. Configuration Safety

- Default to secure configurations unless explicitly asked otherwise.
- Never use wildcard origins (`*`) in CORS or allowed hosts unless strictly necessary and requested.
- Ensure secure cookie settings (HttpOnly, Secure, SameSite) are used where applicable.

### 3. Authentication & Authorization

- Use established authentication frameworks/libraries for the given tech stack unless explicitly instructed otherwise.
- Never implement custom password hashing.
- Enforce least privilege principles.

### 4. Database Safety

- Avoid raw SQL unless absolutely necessary.
- When raw SQL is required, enforce parameterised queries to prevent SQL injection.
- Prefer using an ORM or query builder when available.

### 5. Input Validation

- Always validate and sanitise user input.
- Use established validation libraries appropriate for the stack.
- Never trust client-provided data directly.

### 6. File Upload Safety

- Validate file types and sizes.
- Never store uploaded files directly in public web roots without sanitation.
- Use secure storage backends.

---

## Coding Standards

### 1. Project Structure

- Follow the recommended structure and conventions for the chosen framework/language.
- Keep the codebase modular and separate concerns logically.

### 2. Design Patterns

- Prefer established design patterns over ad-hoc solutions.
- Ensure code is modular, reusable, and loosely coupled.

### 3. Dependencies

- Use stable, maintained, and secure dependencies.
- Avoid introducing unnecessary third-party packages.
- All code must be commented appropriately so that the logic and meaning can be understood by a human.

---

## Testing Requirements

The AI assistant must:

- Generate unit and integration tests for new features.
- Use the standard testing framework for the specific language/stack.
- Include tests for:
  - Core business logic
  - Edge cases and validation
  - Security‑sensitive operations

---

## Documentation Requirements

- Every significant module, function, or class must include appropriate documentation (e.g., docstrings, JSDoc).
- Complex logic must include inline comments explaining *why* something is done, not just *what*.
- Generate README updates when adding major features.

---

## Prohibited Behaviours

The AI assistant must **never**:

- Generate insecure code.
- Suggest disabling security middleware or checks.
- Expose stack traces or internal errors to end users.
- Produce harmful, abusive, or discriminatory content.
- Generate code that violates privacy or data‑protection laws.

---

## When Unsure

If the AI assistant is uncertain about the user’s intent, it should:

- Ask clarifying questions.
- Default to the safest possible implementation.

---

## Agent Autonomy & Execution Policy

- Mode: Always default to Planning Mode for non-trivial tasks.
- Terminal Gate: Do not run build commands, infrastructure provisioning, or database mutations without an explicit user review checkpoint.
- Never move to build mode unless explicitly asked.
- The default is always planning mode.
