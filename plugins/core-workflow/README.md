# Antigravity Agent Configuration

This directory contains customizations, rules, and skills for the Antigravity agent in this project.

## Setup Instructions for Other Projects

To make these skills reproducible in other repositories, ensure the following dependencies are installed in your project's virtual environment.

### Core Workflow Skills

The Python scripts in the `skills` directory are designed to be generic and portable. They respect the following environment variables:
- `PROJECT_ROOT`: The root directory of the project (defaults to the current working directory).
- `LAUNCH_CMD`: A custom command to launch the app (if not provided, `launch_app.py` will try to auto-detect based on `docker-compose.yml`, `manage.py`, or `package.json`).

To quickly configure your terminal environment when testing or using these skills manually, source the provided helper script:
```bash
source setup_env.sh
```

### FastContext Integration

The `fastcontext` skill requires the FastContext CLI to be available in the environment where the agent runs commands.

1. Ensure your project uses a virtual environment (e.g., `.venv`) and that it is activated.
2. Install FastContext directly from its GitHub repository:
   ```bash
   pip install git+https://github.com/microsoft/fastcontext.git
   ```
3. Copy the `.agents` folder (or the relevant `plugin.json` configuration and `skills/fastcontext.md`) to the new repository.

This guarantees that the `Bash(fastcontext *)` tool calls made by the agent will succeed.
