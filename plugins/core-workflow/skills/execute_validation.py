#!/usr/bin/env python3
import sys, re, subprocess, json, os

def main():
    if len(sys.argv) < 2: sys.exit(1)
    arg = sys.argv[1]
    cmds = [arg]
    if arg.endswith(".md") and os.path.exists(arg):
        # ponytail: naive regex for markdown blocks in Validation Gate
        match = re.search(r"##\s*(?:5\.\s*)?Validation Gate(.*?)(?=##|$)", open(arg).read(), re.S | re.I)
        cmds = re.findall(r"```.*?\n(.*?)\n```", match.group(1), re.S) if match else []
        cmds = [line.strip() for b in cmds for line in b.split('\n') if line.strip() and not line.startswith('#')]

    res = []
    for c in cmds:
        print(f"Executing: {c}")
        p = subprocess.run(["bash", "-c", c], text=True, capture_output=True)
        res.append({"command": c, "success": p.returncode == 0, "stdout": p.stdout, "stderr": p.stderr})

    success = all(r["success"] for r in res)
    print(json.dumps({"success": success, "results": res}, indent=2))
    if not success: sys.exit(1)

if __name__ == "__main__": main()
