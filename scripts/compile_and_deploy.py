#!/usr/bin/env python3
"""
compile_and_deploy.py

Single Source of Truth compiler and cross-platform deployer for Agentic Workflow.
Reads master agent definitions from `agents/*.md` and automatically:
1. Compiles Antigravity Skills into `skills/<name>/SKILL.md`
2. Compiles GitHub Copilot Agents into `.github/agents/<name>.agent.md`
3. Cross-platform deploys to macOS, Linux/WSL, and Windows Native target profiles.
"""

import json
import os
import platform
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "agents"
SKILLS_DIR = REPO_ROOT / "skills"
COPILOT_AGENTS_DIR = REPO_ROOT / ".github" / "agents"

# Model slug mapping for Copilot CLI format
MODEL_SLUGS = {
    "Claude Sonnet 4.6 (copilot)": "claude-sonnet-4.6",
    "GPT-5.4 (copilot)": "gpt-5.4",
    "GPT-5.3-Codex (copilot)": "gpt-5.3-codex",
    "GPT-5.4 mini (copilot)": "gpt-5.4-mini",
    "MAI-Code-1-Flash (copilot)": "mai-code-1-flash",
}


def get_target_paths():
    """Resolves deployment paths across macOS, Linux/WSL, and Windows Native."""
    system = platform.system().lower()
    home = Path.home()
    
    paths = {
        "antigravity": [],
        "copilot_prompts": [],
        "copilot_cli": [],
        "vscode_settings": None
    }

    if system == "darwin":  # macOS
        vscode_dir = home / "Library" / "Application Support" / "Code" / "User"
        paths["antigravity"].append(home / ".gemini" / "config" / "skills")
        paths["copilot_prompts"].append(vscode_dir / "prompts" / "agents")
        paths["copilot_prompts"].append(vscode_dir / "profiles" / "builtin" / "agents")
        paths["copilot_cli"].append(home / ".copilot" / "agents")
        paths["vscode_settings"] = vscode_dir / "settings.json"

    elif system == "windows":  # Windows Native
        appdata = Path(os.environ.get("APPDATA", home / "AppData" / "Roaming"))
        vscode_dir = appdata / "Code" / "User"
        paths["antigravity"].append(home / ".gemini" / "config" / "skills")
        paths["copilot_prompts"].append(vscode_dir / "prompts" / "agents")
        paths["copilot_prompts"].append(vscode_dir / "profiles" / "builtin" / "agents")
        paths["copilot_cli"].append(home / ".copilot" / "agents")
        paths["vscode_settings"] = vscode_dir / "settings.json"

    else:  # Linux / WSL Ubuntu
        vscode_dir = home / ".config" / "Code" / "User"
        paths["antigravity"].append(home / ".gemini" / "config" / "skills")
        paths["copilot_prompts"].append(vscode_dir / "prompts" / "agents")
        paths["copilot_cli"].append(home / ".copilot" / "agents")
        paths["vscode_settings"] = vscode_dir / "settings.json"

        # WSL Special Case: Check if Windows user directory is mounted under /mnt/c/Users
        wsl_c_users = Path("/mnt/c/Users")
        if wsl_c_users.exists():
            for win_user in wsl_c_users.iterdir():
                if win_user.is_dir() and win_user.name not in ["Public", "Default", "Default User", "desktop.ini"]:
                    win_gemini = win_user / ".gemini" / "config" / "skills"
                    if win_gemini.parent.exists():
                        paths["antigravity"].append(win_gemini)
                    
                    win_vscode = win_user / "AppData" / "Roaming" / "Code" / "User"
                    if win_vscode.exists():
                        paths["copilot_prompts"].append(win_vscode / "prompts" / "agents")
                        paths["copilot_prompts"].append(win_vscode / "profiles" / "builtin" / "agents")

    return paths


def parse_master_template(template_path: Path):
    """Parses a master markdown template in agents/*.md."""
    text = template_path.read_text(encoding="utf-8")
    frontmatter = {}
    content = text

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if match:
        fm_text, content = match.groups()
        for line in fm_text.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()
                if val.startswith("[") and val.endswith("]"):
                    items = [i.strip().strip("'\"") for i in val[1:-1].split(",")]
                    frontmatter[key] = items
                else:
                    frontmatter[key] = val

    return frontmatter, content, text


def compile_antigravity_skill(stem: str, text: str) -> str:
    """Transforms template into Antigravity SKILL.md format."""
    # Replace config path
    text = text.replace(".github/workflow-config.md", ".agents/core-workflow-config.md")
    # Replace setup skill call
    text = text.replace("@setup-workflow", "/setup-core-workflow")
    text = text.replace("@setup-core-workflow", "/setup-core-workflow")
    # Clean up any Copilot specific model frontmatter
    text = re.sub(r"^model:\s*\[.*?\]\n?", "", text, flags=re.MULTILINE)
    text = re.sub(r"^models:\s*\n(\s+.*\n)*", "", text, flags=re.MULTILINE)
    return text


def compile_copilot_agent(stem: str, text: str) -> str:
    """Transforms template into GitHub Copilot .agent.md format."""
    # Replace config path
    text = text.replace(".agents/core-workflow-config.md", ".github/workflow-config.md")
    # Replace setup skill call
    text = text.replace("/setup-core-workflow", "@setup-workflow")
    text = text.replace("@setup-core-workflow", "@setup-workflow")
    return text


def convert_model_for_cli(text: str) -> str:
    """Converts array model frontmatter to scalar model slug for Copilot CLI compatibility."""
    def cli_model(match):
        models = [item.strip().strip("'\"") for item in match.group(1).split(",")]
        for m in models:
            if m in MODEL_SLUGS:
                return f"model: {MODEL_SLUGS[m]}"
        return f"model: {models[0]}"

    return re.sub(r"^model:\s*\[([^\n]+)\]$", cli_model, text, flags=re.MULTILINE)


def build_and_deploy():
    if not AGENTS_DIR.exists():
        print(f"Error: {AGENTS_DIR} directory does not exist.")
        sys.exit(1)

    master_files = list(AGENTS_DIR.glob("*.md"))
    if not master_files:
        print(f"Error: No master template files found in {AGENTS_DIR}.")
        sys.exit(1)

    print(f"Found {len(master_files)} master agent templates in agents/")
    print("Compiling targets...")

    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    COPILOT_AGENTS_DIR.mkdir(parents=True, exist_ok=True)

    antigravity_count = 0
    copilot_count = 0

    for master_file in master_files:
        stem = master_file.stem
        raw_text = master_file.read_text(encoding="utf-8")

        # 1. Compile Antigravity Skill
        skill_text = compile_antigravity_skill(stem, raw_text)
        skill_sub_dir = SKILLS_DIR / stem
        skill_sub_dir.mkdir(parents=True, exist_ok=True)
        (skill_sub_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
        antigravity_count += 1

        # 2. Compile Copilot Agent
        agent_text = compile_copilot_agent(stem, raw_text)
        agent_file = COPILOT_AGENTS_DIR / f"{stem}.agent.md"
        agent_file.write_text(agent_text, encoding="utf-8")
        copilot_count += 1

    print(f"  ✓ Compiled {antigravity_count} Antigravity Skills -> skills/<name>/SKILL.md")
    print(f"  ✓ Compiled {copilot_count} Copilot Agents -> .github/agents/<name>.agent.md")

    # 3. Deploy to System Target Paths
    target_paths = get_target_paths()
    print("\nDeploying to environment target profiles...")

    # Deploy Antigravity Skills
    deployed_ag = set()
    for ag_base in target_paths["antigravity"]:
        try:
            ag_base.mkdir(parents=True, exist_ok=True)
            for skill_dir in SKILLS_DIR.iterdir():
                if skill_dir.is_dir():
                    dest = ag_base / skill_dir.name
                    dest.mkdir(parents=True, exist_ok=True)
                    for item in skill_dir.iterdir():
                        if item.is_file():
                            shutil.copy2(item, dest / item.name)
            deployed_ag.add(str(ag_base))
        except Exception as e:
            pass

    for d in sorted(deployed_ag):
        print(f"  ✓ [Antigravity Skills] -> {d}")

    # Deploy Copilot Prompts & CLI
    deployed_cp = set()
    for cp_prompt_dir in target_paths["copilot_prompts"]:
        try:
            cp_prompt_dir.mkdir(parents=True, exist_ok=True)
            for agent_file in COPILOT_AGENTS_DIR.glob("*.agent.md"):
                shutil.copy2(agent_file, cp_prompt_dir / agent_file.name)
            deployed_cp.add(str(cp_prompt_dir))
        except Exception as e:
            pass

    for cp_cli_dir in target_paths["copilot_cli"]:
        try:
            cp_cli_dir.mkdir(parents=True, exist_ok=True)
            for agent_file in COPILOT_AGENTS_DIR.glob("*.agent.md"):
                cli_text = convert_model_for_cli(agent_file.read_text(encoding="utf-8"))
                (cp_cli_dir / agent_file.name).write_text(cli_text, encoding="utf-8")
            deployed_cp.add(str(cp_cli_dir))
        except Exception as e:
            pass

    for d in sorted(deployed_cp):
        print(f"  ✓ [Copilot Agents] -> {d}")

    # Register VS Code settings
    settings_file = target_paths["vscode_settings"]
    if settings_file:
        try:
            if settings_file.exists():
                with settings_file.open(encoding="utf-8") as f:
                    settings = json.load(f)
            else:
                settings_file.parent.mkdir(parents=True, exist_ok=True)
                settings = {}

            locations = settings.setdefault("chat.agentFilesLocations", {})
            for cp_dir in target_paths["copilot_prompts"]:
                locations[str(cp_dir)] = True
            
            with settings_file.open("w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
                f.write("\n")
            print(f"  ✓ [VS Code Settings] -> Registered locations in {settings_file}")
        except Exception:
            pass

    print("\n✅ Build and Deployment Complete!")


if __name__ == "__main__":
    build_and_deploy()
