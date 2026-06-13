#!/usr/bin/env python3
import sys
import os
import re
import subprocess
import json

def extract_validation_commands(plan_path):
    if not os.path.exists(plan_path):
        return None, f"File {plan_path} not found"

    with open(plan_path, "r", encoding="utf-8") as f:
        content = f.read()

    validation_match = re.search(r"##\s+(?:5\.\s+)?Validation Gate(.*?)(?=##\s+|$)", content, re.DOTALL | re.IGNORECASE)
    if not validation_match:
        return [], "No Validation Gate section found"

    section_text = validation_match.group(1)
    # Extract commands inside markdown code blocks (```bash ... ``` or ```sh ... ``` or just ``` ... ```)
    commands = re.findall(r"```(?:bash|sh)?\n(.*?)\n```", section_text, re.DOTALL)
    
    # Flatten commands in case there are multiple lines in a single code block
    flat_commands = []
    for block in commands:
        for line in block.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):  # ignore comments
                flat_commands.append(line)

    return flat_commands, None

def run_command_in_correct_dir(cmd):
    # Parse wsl --cd /path/to/dir command
    # e.g., wsl --cd /home/paulsyl/projects/DigitalGolfScorecard/app npm run test ...
    wsl_cd_match = re.match(r"^wsl\s+--cd\s+(\S+)\s+(.+)$", cmd)
    if wsl_cd_match:
        target_dir = wsl_cd_match.group(1)
        actual_cmd = wsl_cd_match.group(2)
    else:
        # Default to current directory or workspace root
        target_dir = os.getcwd()
        actual_cmd = cmd
        # If the command starts with 'wsl ', strip it since we are already inside WSL
        if actual_cmd.startswith("wsl "):
            actual_cmd = actual_cmd[4:].strip()

    print(f"Running: '{actual_cmd}' in directory: '{target_dir}'")
    
    try:
        # Run command using bash
        result = subprocess.run(
            ["bash", "-c", actual_cmd],
            cwd=target_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return {
            "command": actual_cmd,
            "cwd": target_dir,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    except Exception as e:
        return {
            "command": actual_cmd,
            "cwd": target_dir,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(e),
            "success": False
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: execute_validation.py <path_to_plan_md | raw_command>")
        sys.exit(1)

    arg = sys.argv[1]
    
    if arg.endswith(".md"):
        # It's an implementation plan path
        commands, error = extract_validation_commands(arg)
        if error:
            print(json.dumps({"success": False, "error": error}, indent=2))
            sys.exit(1)
        
        if not commands:
            print(json.dumps({"success": False, "error": "No validation commands found in plan"}, indent=2))
            sys.exit(1)
            
        results = []
        all_passed = True
        for cmd in commands:
            res = run_command_in_correct_dir(cmd)
            results.append(res)
            if not res["success"]:
                all_passed = False
                
        output = {
            "success": all_passed,
            "results": results
        }
        print(json.dumps(output, indent=2))
        if not all_passed:
            sys.exit(1)
    else:
        # It's a raw command line
        res = run_command_in_correct_dir(arg)
        print(json.dumps(res, indent=2))
        if not res["success"]:
            sys.exit(1)

if __name__ == "__main__":
    main()
