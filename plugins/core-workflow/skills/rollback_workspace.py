#!/usr/bin/env python3
import sys, os, re, subprocess, json

def run(cmd):
    print(f"Executing: {cmd}")
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
    return {"command": cmd, "success": p.returncode == 0, "stdout": p.stdout, "stderr": p.stderr}

def main():
    cmds = []
    if len(sys.argv) > 1 and sys.argv[1].endswith(".md") and os.path.exists(sys.argv[1]):
        match = re.search(r"##\s*(?:6\.\s*)?Rollback Plan(.*?)(?=##|$)", open(sys.argv[1]).read(), re.S | re.I)
        blocks = re.findall(r"```.*?\n(.*?)\n```", match.group(1), re.S) if match else []
        cmds = [line.strip() for b in blocks for line in b.split('\n') if line.strip() and not line.startswith('#')]

    res = [run(c) for c in cmds] + [run("git reset --hard HEAD"), run("git clean -fd")]
    success = all(r["success"] for r in res)
    print(json.dumps({"success": success, "results": res}, indent=2))
    if not success: sys.exit(1)

if __name__ == "__main__": main()
