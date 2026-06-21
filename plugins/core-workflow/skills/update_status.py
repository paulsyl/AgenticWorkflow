#!/usr/bin/env python3
import sys, os, re

def main():
    if len(sys.argv) < 3 or not os.path.exists(sys.argv[1]): sys.exit(1)
    lines = open(sys.argv[1], "r", encoding="utf-8").readlines()
    if not lines: sys.exit(1)

    for i, line in enumerate(lines):
        if line.startswith("# "):
            clean_title = re.sub(r"^#\s*(?:\[[x /]\]\s*)?", "", line).strip()
            clean_title = re.sub(r"\s+\((?:COMPLETE|IN PROGRESS|PENDING)\)$", "", clean_title, flags=re.I)
            
            st = sys.argv[2].lower()
            if st in ["complete", "x"]: lines[i] = f"# [x] {clean_title} (COMPLETE)\n"
            elif st in ["in-progress", "progress", "/"]: lines[i] = f"# [/] {clean_title} (IN PROGRESS)\n"
            else: lines[i] = f"# [ ] {clean_title}\n"
            
            open(sys.argv[1], "w", encoding="utf-8").writelines(lines)
            print(f'{{"success": true, "message": "Updated to {st}"}}')
            return
    sys.exit(1)

if __name__ == "__main__": main()
