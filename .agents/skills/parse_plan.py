#!/usr/bin/env python3
import sys
import os
import re
import json

def parse_plan(file_path):
    if not os.path.exists(file_path):
        return {"error": f"File {file_path} not found"}

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extracted data structure
    plan_data = {
        "title": "",
        "status": "pending",
        "building_blocks": [],
        "validation_gate": "",
        "rollback_plan": ""
    }

    # Extract Title (e.g. # [x] React Native Framework Setup... or # React Native...)
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        plan_data["title"] = title
        if "[x]" in title.lower() or "complete" in title.lower():
            plan_data["status"] = "complete"

    # Extract building blocks
    # A building block is usually "## Building Block X: ..."
    # and has sub-headers "### 1. Execution Steps" and "### 2. Code Snippets"
    blocks = re.split(r"^##\s+Building Block\s+\d+:\s*(.+)$", content, flags=re.MULTILINE)
    
    # The split results in [prefix, block1_title, block1_content, block2_title, block2_content, ...]
    if len(blocks) > 1:
        prefix = blocks[0]
        for i in range(1, len(blocks), 2):
            block_title = blocks[i].strip()
            block_body = blocks[i+1] if i+1 < len(blocks) else ""
            
            # Stop if we hit the validation gate or other major section
            if "##" in block_title:
                break
            
            # Clean up the body to remove subsequent sections
            end_of_block = block_body.find("\n## ")
            if end_of_block != -1:
                block_body = block_body[:end_of_block]

            # Parse execution steps and snippets within this block
            steps = ""
            snippets = []
            
            steps_match = re.search(r"### 1\.\s+Execution Steps(.*?)(?=### 2\.\s+Code Snippets|$)", block_body, re.DOTALL)
            if steps_match:
                steps = steps_match.group(1).strip()
            
            snippets_match = re.search(r"### 2\.\s+Code Snippets(.*?)$", block_body, re.DOTALL)
            if snippets_match:
                snippets_content = snippets_match.group(1).strip()
                # Find all markdown code blocks preceded by a label line
                code_blocks = re.findall(r"([^\n]+?)\n```(\w*)\n(.*?)\n```", snippets_content, re.DOTALL)
                for cb in code_blocks:
                    label, lang, code = cb
                    snippets.append({
                        "label": label.strip().strip("*").strip(":").strip(),
                        "language": lang.strip(),
                        "code": code.strip()
                    })

            plan_data["building_blocks"].append({
                "name": block_title,
                "execution_steps": steps,
                "snippets": snippets
            })

    # Extract Validation Gate
    validation_match = re.search(r"##\s+(?:5\.\s+)?Validation Gate(.*?)(?=##\s+|$)", content, re.DOTALL | re.IGNORECASE)
    if validation_match:
        plan_data["validation_gate"] = validation_match.group(1).strip()

    # Extract Rollback Plan
    rollback_match = re.search(r"##\s+(?:6\.\s+)?Rollback Plan(.*?)(?=##\s+|$)", content, re.DOTALL | re.IGNORECASE)
    if rollback_match:
        plan_data["rollback_plan"] = rollback_match.group(1).strip()

    return plan_data

def main():
    if len(sys.argv) < 2:
        print("Usage: parse_plan.py <path_to_plan_md> [section]")
        sys.exit(1)

    file_path = sys.argv[1]
    section = sys.argv[2] if len(sys.argv) > 2 else None

    data = parse_plan(file_path)
    if "error" in data:
        print(json.dumps(data, indent=2))
        sys.exit(1)

    if section:
        sect = section.lower()
        if sect in ["steps", "execution_steps"]:
            for idx, block in enumerate(data["building_blocks"]):
                print(f"--- Block {idx+1}: {block['name']} ---")
                print(block["execution_steps"])
                print()
        elif sect in ["snippets", "code_snippets"]:
            for idx, block in enumerate(data["building_blocks"]):
                print(f"--- Block {idx+1}: {block['name']} Snippets ---")
                for snip in block["snippets"]:
                    print(f"File/Label: {snip['label']}")
                    print(f"```{snip['language']}\n{snip['code']}\n```")
                    print()
        elif sect in ["validation", "validation_gate"]:
            print(data["validation_gate"])
        elif sect in ["rollback", "rollback_plan"]:
            print(data["rollback_plan"])
        else:
            print(f"Unknown section: {section}. Choose from: steps, snippets, validation, rollback.")
    else:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
