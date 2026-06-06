---
description: This document defines how Antigravity should behave when assisting with this Django project. The goal is to ensure **secure**, **maintainable**, and **production‑ready** code while preventing unsafe or harmful patterns.
applyTo: '**'
---

# Django Website Creation Instructions for Antigravity

## Core Principles

- Always prioritise **security**, **data protection**, and **privacy**.
- Default to **Django best practices** and **OWASP recommendations**.
- Avoid generating code that exposes secrets, credentials, or sensitive logic.
- Prefer clarity and maintainability over cleverness or shortcuts.

---

## Security Requirements

### 1. Secret Handling

- Never hard‑code secrets, API keys, passwords, tokens, or database credentials.
- Always use environment variables via `os.environ` or Django’s `settings`.
- When generating examples, use placeholders like `"YOUR_SECRET_HERE"`.

### 2. Django Settings Safety

Copilot must:

- Default `DEBUG = False` unless explicitly asked otherwise.
- Use secure defaults:
  - `SECURE_HSTS_SECONDS = 31536000`
  - `SECURE_SSL_REDIRECT = True`
  - `SESSION_COOKIE_SECURE = True`
  - `CSRF_COOKIE_SECURE = True`
- Never suggest `ALLOWED_HOSTS = ["*"]`.

### 3. Authentication & Authorization

- Use Django’s built‑in auth system unless explicitly instructed otherwise.
- Never implement custom password hashing.
- Encourage use of:
  - `django.contrib.auth`
  - `LoginRequiredMixin`
  - `PermissionRequiredMixin`

### 4. Database Safety

- Avoid raw SQL unless absolutely necessary.
- When raw SQL is required, enforce parameterised queries.
- Prefer Django ORM for all CRUD operations.

### 5. Input Validation

- Always validate and sanitise user input.
- Use Django Forms or DRF Serializers for validation.
- Never trust request data directly.

### 6. File Upload Safety

- Validate file types and sizes.
- Never store uploaded files in the project root.
- Use Django’s `FileField` or `ImageField` with safe storage backends.

---

## Coding Standards

### 1. Project Structure

Copilot should follow Django’s recommended structure:

- Separate apps by domain.
- Use `templates/<app_name>/...`
- Use `static/<app_name>/...`

### 2. Views

- Prefer class‑based views over function‑based views.
- Use `ListView`, `DetailView`, `CreateView`, etc., when appropriate.

### 3. URLs

- Use `path()` instead of `url()`.
- Namespace all app URLs.

### 4. Models

- Use explicit `related_name` for relationships.
- Avoid circular imports.
- Use `__str__` methods for readability.

---

## Testing Requirements

Antigravity must:

- Generate tests for new features.
- Use Django’s `TestCase` or DRF’s `APITestCase`.
- Include tests for:
  - Permissions
  - Validation
  - Model behaviour
  - Security‑sensitive logic

---

## Documentation Requirements

- Every generated module must include docstrings.
- Complex logic must include inline comments.
- Copilot should generate README updates when adding major features.

---

## Prohibited Behaviours

Antigravity must **never**:

- Generate insecure code.
- Suggest disabling security middleware.
- Expose stack traces or internal errors.
- Produce harmful, abusive, or discriminatory content.
- Generate code that violates privacy or data‑protection laws.

---

## When Unsure

If Antigravity is uncertain about the user’s intent, it should:

- Ask clarifying questions.
- Default to the safest possible implementation.
