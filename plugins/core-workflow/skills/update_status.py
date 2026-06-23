#!/usr/bin/env python3
import sys, os, re

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]): sys.exit(1)
    
    file_path = sys.argv[1]
    status = sys.argv[2].upper() if len(sys.argv) > 2 else "COMPLETE"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "**Status:**" in content:
        content = re.sub(r'\*\*Status:\*\*.*', f'**Status:** {status}', content)
    else:
        content = f"**Status:** {status}\n\n" + content

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f'{{"success": true, "message": "File updated to {status}"}}')

if __name__ == "__main__": main()
