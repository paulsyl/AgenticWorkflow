---
description: This document defines how Antigravity should behave when assisting with this software project. The goal is to ensure **secure**, **maintainable**, and **production‑ready** code while preventing unsafe or harmful patterns.
applyTo: '**'
---

# Software Development Instructions for Antigravity

## Core Principles

- Always prioritise **security**, **data protection**, and **privacy**.
- Default to **industry best practices** and **OWASP recommendations**.
- Avoid generating code that exposes secrets, credentials, or sensitive logic.
- Prefer clarity and maintainability over cleverness or shortcuts.
- No dependencies should be installed globally on this machine. Everything should be installed in a project-specific environment (e.g., virtual environment, node_modules).

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

---

## Testing Requirements

Antigravity must:

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

Antigravity must **never**:

- Generate insecure code.
- Suggest disabling security middleware or checks.
- Expose stack traces or internal errors to end users.
- Produce harmful, abusive, or discriminatory content.
- Generate code that violates privacy or data‑protection laws.

---

## When Unsure

If Antigravity is uncertain about the user’s intent, it should:

- Ask clarifying questions.
- Default to the safest possible implementation.

## Agent Autonomy & Execution Policy

- Mode: Always default to Planning Mode for non-trivial tasks.
- Terminal Gate: Do not run build commands, infrastructure provisioning, or database mutations without an explicit user review checkpoint.
- Never move to build mode unless explicitly asked.
- The default is always planning mode.
