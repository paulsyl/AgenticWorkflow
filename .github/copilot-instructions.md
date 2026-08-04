# Software Development Instructions

## Core Principles

- Always prioritise **security**, **data protection**, and **privacy**.
- Default to **industry best practices** and **OWASP recommendations**.
- Avoid generating code that exposes secrets, credentials, or sensitive logic.
- Prefer clarity and maintainability over cleverness or shortcuts.
- **No software may be installed directly on this machine.** Use appropriate repository safeguards (e.g., Docker containers, virtual environments, or `node_modules`) to isolate all tools, dependencies, and execution environments.

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

## Coding Standards (Ponytail Protocol)

Apply the "Ponytail" (lazy senior dev) mindset for all coding activities. The best code is the code never written.

### 1. The Simplest Path (YAGNI)
Before writing any code, stop at the first rung that holds:
1. Does this need to be built at all?
2. Does the standard library already do this? Use it.
3. Does a native platform feature cover it? Use it.
4. Does an already-installed dependency solve it? Use it.
5. Can this be one line? Make it one line.
6. Only then: write the minimum code that works.

### 2. Implementation Rules
- **No unnecessary abstractions**: Only build what was explicitly requested.
- **Minimal dependencies**: Avoid new dependencies if a native/stdlib feature works.
- **Zero boilerplate**: Deletion over addition. Boring over clever. Fewest files possible.
- **Edge-case correctness**: Pick the edge-case-correct option when two stdlib approaches are the same size.
- **Deferrals**: Mark intentional simplifications with a `ponytail:` comment, naming the ceiling and the upgrade path.

### 3. Non-Negotiables (Not Lazy About)
- Input validation at trust boundaries, error handling that prevents data loss, security, and accessibility.
- Non-trivial logic must leave ONE runnable check behind (the smallest thing that fails if the logic breaks).

---

## Project Structure & Organisation

Every repository and application must be laid out sensibly, following the conventions of its language/framework. Prefer the ecosystem's idiomatic layout over a custom one.

- **Follow ecosystem conventions**: Use the standard structure for the stack (e.g. `src/` layout for Python packages, `src/`/`tests/` for Node, `cmd/`/`internal/`/`pkg/` for Go, framework CLIs' generated layout for Django/Next.js/etc.). Do not invent a bespoke layout when a conventional one exists.
- **Separate concerns by directory**: Keep source, tests, docs, scripts, and configuration in clearly named top-level directories. Tests live alongside or mirror the source tree; they are never mixed into production code paths.
- **One clear entry point**: The way to build, run, and test the project must be obvious and consistent (a documented command or task, not tribal knowledge).
- **Root hygiene**: Keep the repository root uncluttered — configuration and metadata files only. No stray scripts, scratch files, build output, or secrets committed to the root.
- **Predictable naming**: Use consistent, descriptive names for files and directories following the stack's casing conventions. Group related modules; avoid dumping everything in one directory.
- **Isolate dependencies and generated output**: Dependencies, build artifacts, caches, and local data must live in ignored directories (see `.gitignore`/`.copilotignore`), never committed.
- **Config at the boundary**: Environment-specific configuration is externalised (env vars / config files), never hard-coded or scattered through the codebase.

---

## Testing Requirements

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

### README.md (Mandatory)

Every project must ship with a well-written, comprehensive `README.md` at its root. Create it if it is missing and keep it current whenever features, setup, or usage change. At minimum it must cover:

1. **Project title & description** — what it does and the problem it solves.
2. **Features** — key capabilities at a glance.
3. **Prerequisites** — required runtimes, tools, and versions.
4. **Installation** — step-by-step setup, isolated per repository policy (containers/virtual envs/`node_modules`; no global installs on the host).
5. **Configuration** — required environment variables and config files, using placeholders (e.g. `YOUR_SECRET_HERE`); never commit real secrets.
6. **Usage** — concrete, copy-pasteable commands and examples showing how to run the application and exercise its main features.
7. **Testing** — how to run the test suite.
8. **Project structure** — a short map of the key directories and their purpose.
9. **License** (where applicable).

Write for a newcomer who has never seen the project. Keep instructions accurate, runnable, and free of secrets.

---

## Prohibited Behaviours

**Never**:

- Generate insecure code.
- Suggest disabling security middleware or checks.
- Expose stack traces or internal errors to end users.
- Produce harmful, abusive, or discriminatory content.
- Generate code that violates privacy or data‑protection laws.

---

## When Unsure

- Ask clarifying questions.
- Default to the safest possible implementation.

## Agent Autonomy & Execution Policy

- Mode: Always default to Planning Mode for non-trivial tasks.
- Terminal Gate: Do not run build commands, infrastructure provisioning, or database mutations without an explicit user review checkpoint.
- **Never move to build mode unless explicitly asked. The default is always planning mode.**
