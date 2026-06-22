#!/usr/bin/env python3
"""
execute_validation.py

Execute validation gate commands from an implementation plan.
Extracts bash commands from the Validation Gate section and runs them.

Usage:
  python execute_validation.py <plan_file>
  
Returns JSON with execution results:
  {
    "success": true/false,
    "results": [
      {
        "command": "pytest tests/...",
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


def extract_validation_commands(plan_file):
    """Extract bash commands from Validation Gate section of plan."""
    if not os.path.exists(plan_file):
        print(f"Error: Plan file not found: {plan_file}", file=sys.stderr)
        return []
    
    try:
        with open(plan_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading plan file: {e}", file=sys.stderr)
        return []
    
    # Extract Validation Gate section (level 2 or 3 header)
    match = re.search(r"##\s+(?:5\.\s+)?Validation Gate(.*?)(?=##|$)", content, re.S | re.I)
    if not match:
        return []
    
    validation_content = match.group(1)
    
    # Extract all bash code blocks
    commands = []
    for block_match in re.finditer(r"```(?:bash|sh)?\n(.*?)\n```", validation_content, re.S):
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
        print("Usage: python execute_validation.py <plan_file>", file=sys.stderr)
        sys.exit(1)
    
    plan_file = sys.argv[1]
    
    # Extract commands from the plan
    commands = extract_validation_commands(plan_file)
    
    if not commands:
        print(json.dumps({
            "success": True,
            "message": "No validation commands found",
            "results": []
        }, indent=2))
        sys.exit(0)
    
    # Execute each command
    results = []
    all_success = True
    
    for cmd in commands:
        print(f"Executing: {cmd}", flush=True)
        result = run(cmd)
        result["command"] = cmd
        results.append(result)
        
        if not result["success"]:
            all_success = False
            print(f"  ❌ FAILED", flush=True)
            if result["stderr"]:
                print(f"  Error: {result['stderr'][:200]}", flush=True)
        else:
            print(f"  ✅ PASSED", flush=True)
    
    # Output results as JSON
    output = {
        "success": all_success,
        "results": results
    }
    print(json.dumps(output, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()
