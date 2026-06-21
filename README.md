# Antigravity Global Agents & Plugins

This repository serves as a central hub for all custom global agents, rules, and plugins used in your Antigravity projects.

## Structure

- `GEMINI.md`: Global instructions for the Antigravity agent. These rules apply across all projects where this file is referenced.
- `plugins/`: A directory containing all your agent plugins.
  - `core-workflow/`: Custom agent rules and Python automation scripts for strict phase-by-phase implementation, validation, and rollback workflows.
  - `template-plugin/`: A boilerplate to help you quickly set up new plugins, skills, and agents.
- `scripts/`: Useful bash scripts for automating your environment setup.

## Installation

To make these plugins available to your local Antigravity IDE across all projects, you can use the provided installation script. This script will safely symlink the plugins from this repository directly into your IDE's plugin directory (`~/.gemini/config/plugins/`).

Run the following command from the repository root:

```bash
./scripts/install_plugins.sh
```

## Creating a New Plugin

1. Copy the `plugins/template-plugin` directory and rename it to your new plugin's name.
2. Update the `plugin.json` file inside your new directory with the appropriate name, description, rules, and skills mapping.
3. Add any Python tools to the `skills/` directory.
4. Add any subagent definitions to the `agents/` directory.
5. Re-run `./scripts/install_plugins.sh` to link your new plugin.
