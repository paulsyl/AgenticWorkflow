#!/usr/bin/env python3
import sys
import os
import re
import subprocess
import json

def extract_rollback_commands(plan_path):
    if not os.path.exists(plan_path):
        return None, f"File {plan_path} not found"

    with open(plan_path, "r", encoding="utf-8") as f:
        content = f.read()

    rollback_match = re.search(r"##\s+(?:6\.\s+)?Rollback Plan(.*?)(?=##\s+|$)", content, re.DOTALL | re.IGNORECASE)
    if not rollback_match:
        return [], "No Rollback Plan section found"

    section_text = rollback_match.group(1)
    # Extract commands inside markdown code blocks (```bash ... ``` or ```sh ... ``` or just ``` ... ```)
    commands = re.findall(r"```(?:bash|sh)?\n(.*?)\n```", section_text, re.DOTALL)
    
    flat_commands = []
    for block in commands:
        for line in block.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):  # ignore comments
                flat_commands.append(line)

    return flat_commands, None

def run_command(cmd, cwd=None):
    if cwd is None:
        cwd = os.getcwd()
    
    # Strip wsl prefixes if running inside WSL
    if cmd.startswith("wsl "):
        # Check for wsl --cd /path/to/dir
        wsl_cd_match = re.match(r"^wsl\s+--cd\s+(\S+)\s+(.+)$", cmd)
        if wsl_cd_match:
            cwd = wsl_cd_match.group(1)
            cmd = wsl_cd_match.group(2)
        else:
            cmd = cmd[4:].strip()

    print(f"Executing: '{cmd}' in '{cwd}'")
    try:
        res = subprocess.run(
            ["bash", "-c", cmd],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return {
            "command": cmd,
            "exit_code": res.returncode,
            "stdout": res.stdout,
            "stderr": res.stderr,
            "success": res.returncode == 0
        }
    except Exception as e:
        return {
            "command": cmd,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "success": False
        }

def main():
    plan_path = sys.argv[1] if len(sys.argv) > 1 else None
    results = []
    
    # 1. Execute plan-specific rollback if provided
    if plan_path and plan_path.endswith(".md"):
        print(f"Extracting rollback commands from plan: {plan_path}")
        commands, error = extract_rollback_commands(plan_path)
        if error:
            print(f"Warning: could not extract plan rollback commands: {error}")
        elif commands:
            for cmd in commands:
                res = run_command(cmd)
                results.append(res)
                if not res["success"]:
                    print(f"Rollback command failed: {cmd}\nError: {res['stderr']}")

    # 2. Force Git hard reset & clean untracked files
    print("Executing Git hard reset & cleaning workspace...")
    git_reset_res = run_command("git reset --hard HEAD")
    results.append(git_reset_res)
    
    git_clean_res = run_command("git clean -fd")
    results.append(git_clean_res)
    
    success = git_reset_res["success"] and git_clean_res["success"]
    
    output = {
        "success": success,
        "results": results
    }
    print(json.dumps(output, indent=2))
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
