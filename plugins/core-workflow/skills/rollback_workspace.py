#!/usr/bin/env python3
import sys, os, subprocess, json

def run(cmd):
    print(f"Executing: {cmd}")
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
    return {"command": cmd, "success": p.returncode == 0, "stdout": p.stdout, "stderr": p.stderr}

def main():
    cmds = []
    if len(sys.argv) > 1 and sys.argv[1].endswith(".json") and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if len(sys.argv) > 2:
            phase_num = int(sys.argv[2])
            phase = next((p for p in data.get("phases", []) if p.get("phase_number") == phase_num), None)
            if phase and phase.get("rollback_command"):
                cmds.append(phase.get("rollback_command"))
        else:
            for p in data.get("phases", []):
                if p.get("rollback_command"): cmds.append(p.get("rollback_command"))

    res = [run(c) for c in cmds] + [run("git reset --hard HEAD"), run("git clean -fd")]
    success = all(r["success"] for r in res)
    print(json.dumps({"success": success, "results": res}, indent=2))
    if not success: sys.exit(1)

if __name__ == "__main__": main()
