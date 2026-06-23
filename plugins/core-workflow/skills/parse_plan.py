#!/usr/bin/env python3
import sys, json, os

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        sys.exit(1)
    
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if len(sys.argv) > 2:
        phase_num = int(sys.argv[2])
        phase = next((p for p in data.get("phases", []) if p.get("phase_number") == phase_num), None)
        if not phase:
            sys.exit(1)
        
        if len(sys.argv) > 3:
            sect = sys.argv[3].lower()
            if "step" in sect:
                print("\n".join(phase.get("execution_steps", [])))
            elif "snip" in sect:
                for fname, code in phase.get("code_snippets", {}).items():
                    print(f"File: {fname}\n```\n{code}\n```\n")
            elif "val" in sect:
                print(phase.get("validation_command", ""))
            elif "roll" in sect:
                print(phase.get("rollback_command", ""))
        else:
            print(json.dumps(phase, indent=2))
    else:
        print(json.dumps(data, indent=2))

if __name__ == "__main__": main()
