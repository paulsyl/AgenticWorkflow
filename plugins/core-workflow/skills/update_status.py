#!/usr/bin/env python3
import sys, os, json

def main():
    if len(sys.argv) < 3 or not os.path.exists(sys.argv[1]): sys.exit(1)
    
    file_path = sys.argv[1]
    phase_num = int(sys.argv[2])
    status = sys.argv[3].lower() if len(sys.argv) > 3 else "complete"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = False
    for p in data.get("phases", []):
        if p.get("phase_number") == phase_num:
            p["status"] = status
            updated = True
            break
            
    if updated:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f'{{"success": true, "message": "Phase {phase_num} updated to {status}"}}')
    else:
        print(f'{{"success": false, "message": "Phase {phase_num} not found"}}')
        sys.exit(1)

if __name__ == "__main__": main()
