#!/usr/bin/env python3
"""
rollback_workspace.py

Execute rollback commands from an implementation plan.
Extracts bash commands from the Rollback Plan section and runs them.
Also performs a git reset and git clean to ensure clean state.

Usage:
  python rollback_workspace.py <plan_file>
  
Returns JSON with rollback results:
  {
    "success": true/false,
    "results": [
      {
        "command": "...",
        "success": true/false,
        "stdout": "...",
        "stderr": "..."
      },
      ...
    ]
  }
"""

import sys
import os
import re
import subprocess
import json


def run(cmd):
    """Run a bash command and capture output."""
    try:
        process = subprocess.run(
            ["bash", "-c", cmd],
            text=True,
            capture_output=True,
            timeout=300  # 5 minute timeout
        )
        return {
            "success": process.returncode == 0,
            "returncode": process.returncode,
            "stdout": process.stdout,
            "stderr": process.stderr
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": "Command timed out after 300 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": f"Error: {str(e)}"
        }


def extract_rollback_commands(plan_file):
    """Extract bash commands from Rollback Plan section of plan."""
    if not os.path.exists(plan_file):
        return []
    
    try:
        with open(plan_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return []
    
    # Extract Rollback Plan section (level 2 or 3 header)
    match = re.search(r"##\s+(?:6\.\s+)?Rollback Plan(.*?)(?=##|$)", content, re.S | re.I)
    if not match:
        return []
    
    rollback_content = match.group(1)
    
    # Extract all bash code blocks
    commands = []
    for block_match in re.finditer(r"```(?:bash|sh)?\n(.*?)\n```", rollback_content, re.S):
        block_content = block_match.group(1)
        # Split by lines and filter out comments and empty lines
        lines = [
            line.strip()
            for line in block_content.split('\n')
            if line.strip() and not line.strip().startswith('#')
        ]
        commands.extend(lines)
    
    return commands


def main():
    if len(sys.argv) < 2:
        # No plan file specified; just do git reset and git clean
        commands = []
    else:
        plan_file = sys.argv[1]
        commands = extract_rollback_commands(plan_file)
    
    # Execute explicit rollback commands from the plan
    results = []
    all_success = True
    
    for cmd in commands:
        print(f"Executing rollback: {cmd}", flush=True)
        result = run(cmd)
        result["command"] = cmd
        results.append(result)
        
        if not result["success"]:
            all_success = False
            print(f"  ⚠️  Command returned non-zero (continuing)", flush=True)
        else:
            print(f"  ✅ Done", flush=True)
    
    # Always perform git reset and git clean as final safety measure
    print("Running git reset --hard HEAD...", flush=True)
    result = run("git reset --hard HEAD")
    result["command"] = "git reset --hard HEAD"
    results.append(result)
    if result["success"]:
        print(f"  ✅ Git reset complete", flush=True)
    else:
        print(f"  ⚠️  Git reset warning: {result['stderr'][:100]}", flush=True)
    
    print("Running git clean -fd...", flush=True)
    result = run("git clean -fd")
    result["command"] = "git clean -fd"
    results.append(result)
    if result["success"]:
        print(f"  ✅ Git clean complete", flush=True)
    else:
        print(f"  ⚠️  Git clean warning: {result['stderr'][:100]}", flush=True)
    
    # Output results as JSON
    output = {
        "success": all_success,
        "results": results
    }
    print(json.dumps(output, indent=2))
    
    # Exit with success if git operations succeeded (core requirement)
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
