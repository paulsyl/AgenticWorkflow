#!/usr/bin/env python3
"""
parse_plan.py

Parse an implementation plan markdown file and extract structured data.
Returns JSON with extracted sections for the executor to use.

Usage:
  python parse_plan.py <plan_file> [section]
  
  Sections: "step", "snip", "val", "roll"
  If no section specified, returns full JSON structure.

Example:
  python parse_plan.py auth_caching_plan.md
  python parse_plan.py auth_caching_plan.md step
"""

import sys
import re
import json
import os


def parse_plan(filename):
    """Parse implementation plan markdown and extract structured data."""
    if not os.path.exists(filename):
        print(f"Error: File not found: {filename}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Extract plan title
    title_match = re.search(r"^#\s+(.+)$", content, re.M)
    title = title_match.group(1).strip() if title_match else ""
    
    # Extract building blocks (sections starting with "## Building Block")
    blocks = re.split(r"^##\s+Building Block\s+\d+:\s*(.+)$", content, flags=re.M)
    
    # Extract validation gate and rollback plan (global sections)
    validation_gate = ""
    validation_match = re.search(r"##\s+(?:5\.\s+)?Validation Gate(.*?)(?=##|$)", content, re.S | re.I)
    if validation_match:
        validation_gate = validation_match.group(1).strip()
    
    rollback_plan = ""
    rollback_match = re.search(r"##\s+(?:6\.\s+)?Rollback Plan(.*?)(?=##|$)", content, re.S | re.I)
    if rollback_match:
        rollback_plan = rollback_match.group(1).strip()
    
    data = {
        "title": title,
        "filename": filename,
        "status": "pending",
        "validation_gate": validation_gate,
        "rollback_plan": rollback_plan,
        "building_blocks": []
    }
    
    # Process building blocks
    if len(blocks) > 1:
        for i in range(1, len(blocks), 2):
            block_title = blocks[i].strip() if i < len(blocks) else ""
            block_body = (blocks[i+1].split("\n## ")[0] if i+1 < len(blocks) else "")
            
            # Extract execution steps
            steps_match = re.search(r"### 1\.\s+Execution Steps(.*?)### 2\.\s+Code Snippets", block_body, re.S)
            steps = steps_match.group(1).strip() if steps_match else ""
            
            # Extract code snippets
            snip_match = re.search(r"### 2\.\s+Code Snippets(.*)", block_body, re.S)
            snip_content = snip_match.group(1) if snip_match else ""
            
            # Parse code snippets into labeled blocks
            snippets = []
            for match in re.finditer(r"([^\n]+)\n```(\w*)\n(.*?)\n```", snip_content, re.S):
                label, language, code = match.groups()
                snippets.append({
                    "label": label.strip().strip("*:-"),
                    "language": language.strip(),
                    "code": code.strip()
                })
            
            data["building_blocks"].append({
                "name": block_title,
                "execution_steps": steps,
                "snippets": snippets,
                "validation_gate": validation_gate,
                "rollback_plan": rollback_plan
            })
    
    return data


def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_plan.py <plan_file> [section]", file=sys.stderr)
        print("Sections: step (steps), snip (snippets), val (validation), roll (rollback)", file=sys.stderr)
        sys.exit(1)
    
    plan_file = sys.argv[1]
    data = parse_plan(plan_file)
    
    # If a specific section is requested, print just that section
    if len(sys.argv) > 2:
        section = sys.argv[2].lower()
        
        if "step" in section:
            # Print execution steps for all building blocks
            for i, block in enumerate(data["building_blocks"]):
                print(f"--- Building Block {i+1}: {block['name']} ---")
                print(block['execution_steps'])
                print()
        
        elif "snip" in section:
            # Print code snippets for all building blocks
            for i, block in enumerate(data["building_blocks"]):
                for snippet in block["snippets"]:
                    print(f"File/Label: {snippet['label']}")
                    print(f"```{snippet['language']}")
                    print(snippet['code'])
                    print("```")
                    print()
        
        elif "val" in section:
            # Print validation gates
            print(data["validation_gate"])
        
        elif "roll" in section:
            # Print rollback plan
            print(data["rollback_plan"])
    
    else:
        # No section specified; print full JSON
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
