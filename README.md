# Antigravity Global Agents & Plugins

This repository is the central nervous system for your Antigravity IDE. It defines global instructions, strict development philosophies, and custom agent plugins that standardize how work is executed across *all* of your projects. 

## Purpose

The primary goal of this repository is to enforce **resilient, secure, and deterministic software engineering practices**. By standardizing our agent rules and skills globally, we ensure that every project benefits from:

1. **The "Ponytail" Philosophy:** A pragmatic approach that prioritizes laziness, simplicity, and minimum viable code. No boilerplate, no over-engineering, and no unnecessary abstractions (YAGNI).
2. **Adversarial Review Gates:** A robust council of agent personas (Architect, Security Auditor, Reliability Engineer, SDET, etc.) that ruthlessly critique and attack implementation plans *before* any code is written.
3. **Deterministic Execution:** Strict phase-by-phase execution of approved implementation plans, backed by custom Python skills that validate success or automatically rollback the workspace on failure.

## Repository Structure

- `GEMINI.md`: Global instructions outlining core principles, security requirements, and coding standards. These rules apply universally.
- `.antigravityignore`: A global ignore file preventing agents from accessing or modifying sensitive or irrelevant directories.
- `plugins/`: The core engine of this repository.
  - `core-workflow/`: Contains the `architect`, `multi-agent-review`, and `executor` rules, alongside robust python skills for plan parsing, validation, app launching, and workspace rollback.
  - `ponytail/`: Contains the rules and skills for enforcing the lazy senior developer philosophy.
  - `template-plugin/`: A boilerplate to help you quickly scaffold new agent plugins.
- `scripts/`: Environment and installation scripts.

## Usage Notes

Once installed, these agents and rules are globally available in any workspace you open.

### Summoning the Agents

You can trigger specific workflows by summoning the defined agents in your chat:

1. **The Architect (`@architect`)**: Use when requesting a new feature or system design. The architect will actively explore your codebase and output a strict `{feature}_{phase}_implementation_plan.md` that includes a Codebase Impact Analysis with a High/Medium/Low refactoring rating.
2. **The Adversarial Council (`@adversarial-review`)**: Summon this agent to review an existing implementation plan. It will spawn 8 distinct personas to attack the plan for security vulnerabilities, architectural flaws, environmental resilience, and "ponytail" pragmatism.
3. **The Executor (`@executor`)**: Once a plan is reviewed and approved, summon the executor. It will strictly build the plan phase-by-phase, running validation tests, updating progress journals, and automatically rolling back changes if the tests fail.

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
