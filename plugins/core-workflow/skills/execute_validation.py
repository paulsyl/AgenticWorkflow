#!/usr/bin/env python3
import sys, subprocess, json, os

def main():
    if len(sys.argv) < 2: sys.exit(1)
    arg = sys.argv[1]
    
    cmds = []
    if arg.endswith(".json") and os.path.exists(arg):
        with open(arg, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if len(sys.argv) > 2:
            phase_num = int(sys.argv[2])
            phase = next((p for p in data.get("phases", []) if p.get("phase_number") == phase_num), None)
            if phase and phase.get("validation_command"):
                cmds.append(phase.get("validation_command"))
        else:
            for p in data.get("phases", []):
                if p.get("validation_command"): cmds.append(p.get("validation_command"))
    else:
        cmds.append(arg)

    res = []
    for c in cmds:
        print(f"Executing: {c}")
        p = subprocess.run(["bash", "-c", c], text=True, capture_output=True)
        res.append({"command": c, "success": p.returncode == 0, "stdout": p.stdout, "stderr": p.stderr})

    success = all(r["success"] for r in res)
    print(json.dumps({"success": success, "results": res}, indent=2))
    if not success: sys.exit(1)

if __name__ == "__main__": main()
