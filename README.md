# Antigravity Global Agents & Plugins

This repository is the central nervous system for your Antigravity IDE. It defines global instructions, strict development philosophies, and custom agent plugins that standardize how work is executed across *all* of your projects. 

## Purpose

The primary goal of this repository is to enforce **resilient, secure, and deterministic software engineering practices**. By standardizing our agent rules and skills globally, we ensure that every project benefits from:

1. **The 4-Stage Grounded SDLC:** A strict, contract-driven software development lifecycle where ambiguity is systematically eliminated before architecture is designed, and where architecture is rigorously tested before code is written.
2. **The "Ponytail" Philosophy:** A pragmatic approach that prioritizes laziness, simplicity, and minimum viable code. No boilerplate, no over-engineering, and no unnecessary abstractions (YAGNI).
3. **The Review Council (Adversarial Review Gates):** A robust council of 9 specialized agent personas (Security, Performance, DB Schema, etc.) that ruthlessly critique and validate implementation plans against the canonical product requirements.
4. **Deterministic Execution:** Strict phase-by-phase execution of Markdown-based implementation blueprints, backed by custom Python skills that validate success, allow limited autonomous fixes (Upstream Escape Hatch), or automatically rollback the workspace and throw architectural exceptions.

## Repository Structure

- `global_gemini_rules.md`: Global instructions outlining core principles, security requirements, and the Ponytail coding protocol. These rules apply universally.
- `.antigravityignore`: A global ignore file preventing agents from accessing or modifying sensitive or irrelevant directories.
- `plugins/`: The core engine of this repository.
  - `core-workflow/`: Contains the `orchestrator`, `specifier`, `architect`, `multi-agent-review` (The Review Council), and `executor` rules, alongside robust python skills for Markdown plan parsing, validation, and workspace rollback.
  - `ponytail/`: Contains the rules and skills for enforcing the lazy senior developer philosophy.
  - `template-plugin/`: A boilerplate to help you quickly scaffold new agent plugins.
- `scripts/`: Environment and installation scripts.

## Usage Notes

Once installed, these agents and rules are globally available in any workspace you open.

### Summoning the Agents

You can trigger the fully automated end-to-end SDLC pipeline using `@orchestrator`, or you can trigger specific stages manually by summoning the defined agents in your chat:

1. **The Specifier (`@specifier`) - STAGE 1**: Use when defining a new feature. Refuses to generate a `PRD.md` until all ambiguity chasms in your raw scope are resolved via an Interrogation Loop.
2. **The Architect (`@architect`) - STAGE 2**: Translates the immutable `PRD.md` into technical blueprints, generating technical diagrams (`System-Architecture.md`) and atomic execution steps (`iterations/<iteration_name>/Phase-*.md` files).
3. **The Review Council (`@reviewcouncil`) - STAGE 3**: Summon this council of 9 personas to validate the Architect's plan strictly against the PRD constraints. They output `PASS` or `REJECT` and iterate until unanimous approval.
4. **The Executor (`@executor`) - STAGE 4**: Once a plan is reviewed and approved, summon the builder. It will strictly build the phase files phase-by-phase using the `@ponytail` agent, run validation tests, and automatically roll back changes and throw an `ArchitecturalException` if a test fails 3 times.

### Local Environment Setup

The `core-workflow` skills (like `launch_app.py` and `execute_validation.py`) rely on standard environment variables to be fully generic across projects.
If you need to test these skills manually or configure a non-standard app launch command, source the helper script:

```bash
cd plugins/core-workflow
source setup_env.sh
```

*Note: By default, the `launch_app.py` script will auto-detect your project type (e.g., Docker, NPM, or Python Virtual Environments) without requiring manual configuration.*

## Installation & Syncing

To install or sync these rules across all of your projects, you must copy them into your global Gemini config directory (`C:\Users\User\.gemini\config\` on Windows, or `~/.gemini/config/` on Linux). 

We provide a convenient bash script that handles the linking of the plugins for you. Run the following command from the root of this repository whenever you make updates:

```bash
./scripts/install_plugins.sh
```
