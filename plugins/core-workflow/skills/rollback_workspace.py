#!/usr/bin/env python3
import sys, os, subprocess, json, re

def run(cmd):
    print(f"Executing: {cmd}")
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
    return {"command": cmd, "success": p.returncode == 0, "stdout": p.stdout, "stderr": p.stderr}

def main():
    cmds = []
    if len(sys.argv) > 1 and sys.argv[1].endswith(".md") and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()
        
        match = re.search(r'-\s*\*\*Rollback:\*\*\s*`(.+?)`', content)
        if match:
            cmds.append(match.group(1))

    res = [run(c) for c in cmds] + [run("git reset --hard HEAD"), run("git clean -fd")]
    success = all(r["success"] for r in res)
    print(json.dumps({"success": success, "results": res}, indent=2))
    if not success: sys.exit(1)

if __name__ == "__main__": main()
