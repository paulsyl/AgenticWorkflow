#!/usr/bin/env python3
import sys
import os
import re
import json

def update_status(plan_path, status):
    if not os.path.exists(plan_path):
        return False, f"File {plan_path} not found"

    with open(plan_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        return False, "File is empty"

    # Find the title (usually the first line starting with #)
    title_idx = -1
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            title_idx = idx
            break

    if title_idx == -1:
        return False, "No markdown title line found (starting with '# ')"

    title_line = lines[title_idx].strip()
    
    # Strip existing status tags like [x], [ ], [/] from the title prefix
    # e.g., "# [x] Title text" -> "Title text"
    title_text = re.sub(r"^#\s*(?:\[[x /]\]\s*)?", "", title_line)
    
    # Strip "(COMPLETE)" or "(IN PROGRESS)" suffixes
    title_text = re.sub(r"\s+\((?:COMPLETE|IN PROGRESS|PENDING)\)$", "", title_text, flags=re.IGNORECASE)

    status = status.lower()
    if status in ["complete", "x"]:
        new_title = f"# [x] {title_text} (COMPLETE)\n"
    elif status in ["in-progress", "progress", "/"]:
        new_title = f"# [/] {title_text} (IN PROGRESS)\n"
    elif status in ["pending", "todo", " "]:
        new_title = f"# [ ] {title_text}\n"
    else:
        return False, f"Invalid status: '{status}'. Choose from: complete, in-progress, pending"

    lines[title_idx] = new_title

    with open(plan_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return True, f"Updated plan status to {status.upper()}"

def main():
    if len(sys.argv) < 3:
        print("Usage: update_status.py <path_to_plan_md> <complete|in-progress|pending>")
        sys.exit(1)

    plan_path = sys.argv[1]
    status = sys.argv[2]

    success, msg = update_status(plan_path, status)
    print(json.dumps({"success": success, "message": msg}, indent=2))
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
