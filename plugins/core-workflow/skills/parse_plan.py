#!/usr/bin/env python3
import sys, re, json, os

def main():
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]): sys.exit(1)
    content = open(sys.argv[1], "r", encoding="utf-8").read()
    
    # ponytail: naive regex extraction for predefined plan format
    title_match = re.search(r"^#\s+(.+)$", content, re.M)
    blocks = re.split(r"^##\s+Building Block\s+\d+:\s*(.+)$", content, flags=re.M)
    
    data = {
        "title": title_match.group(1).strip() if title_match else "",
        "status": "complete" if title_match and ("[x]" in title_match.group(1).lower() or "complete" in title_match.group(1).lower()) else "pending",
        "validation_gate": (re.search(r"##\s*(?:5\.\s*)?Validation Gate(.*?)(?=##|$)", content, re.S | re.I) or [None, ""])[1].strip(),
        "rollback_plan": (re.search(r"##\s*(?:6\.\s*)?Rollback Plan(.*?)(?=##|$)", content, re.S | re.I) or [None, ""])[1].strip(),
        "building_blocks": []
    }

    if len(blocks) > 1:
        for i in range(1, len(blocks), 2):
            b_title, b_body = blocks[i].strip(), (blocks[i+1].split("\n## ")[0] if i+1 < len(blocks) else "")
            steps = (re.search(r"### 1\.\s+Execution Steps(.*?)### 2\.\s+Code Snippets", b_body, re.S) or [None, ""])[1].strip()
            snip_content = (re.search(r"### 2\.\s+Code Snippets(.*)", b_body, re.S) or [None, ""])[1]
            data["building_blocks"].append({
                "name": b_title, "execution_steps": steps,
                "snippets": [{"label": l.strip().strip("*:-"), "language": lang, "code": code.strip()} 
                             for l, lang, code in re.findall(r"([^\n]+)\n```(\w*)\n(.*?)\n```", snip_content, re.S)]
            })

    if len(sys.argv) > 2:
        sect = sys.argv[2].lower()
        if "step" in sect:
            for i, b in enumerate(data["building_blocks"]): print(f"--- Block {i+1}: {b['name']} ---\n{b['execution_steps']}\n")
        elif "snip" in sect:
            for i, b in enumerate(data["building_blocks"]):
                for s in b["snippets"]: print(f"File/Label: {s['label']}\n```{s['language']}\n{s['code']}\n```\n")
        elif "val" in sect: print(data["validation_gate"])
        elif "roll" in sect: print(data["rollback_plan"])
    else:
        print(json.dumps(data, indent=2))

if __name__ == "__main__": main()
