#!/usr/bin/env python3
"""
sync_agent_ignores.py - Harness Ignore Sync Utility
Reads workspace-root .agentignore and non-destructively syncs its rules to 
target agent harness ignore files using sentinel comment blocks.
ponytail: simple file-based sentinel search & replace using standard library only.
"""
import os
import sys

BEGIN_SENTINEL = "# --- BEGIN AGENTIC WORKFLOW IGNORE ---"
END_SENTINEL = "# --- END AGENTIC WORKFLOW IGNORE ---"

DEFAULT_IGNORE_CONTENT = """# Master .agentignore
# Media & Binaries
*.png
*.jpg
*.jpeg
*.gif
*.webp
*.ico
*.mp4
*.mov
*.mp3
*.wav
*.pdf
*.zip
*.tar.gz
*.7z
*.exe
*.dll
*.so
*.dylib
*.bin
*.iso

# Model Weights & Large Datasets
*.onnx
*.pth
*.safetensors
*.parquet
*.sqlite
*.db

# Lockfiles
package-lock.json
pnpm-lock.yaml
yarn.lock
Cargo.lock
poetry.lock

# Build & Cache Directories
node_modules/
dist/
build/
.venv/
.next/
.git/
coverage/
__pycache__/
"""

TARGET_FILES = [
    ".antigravityignore",
    ".copilotignore",
    ".github/copilot-ignore",
    ".claudeignore",
    ".ignore",
]

def ensure_master_ignore(root_dir):
    master_path = os.path.join(root_dir, ".agentignore")
    if not os.path.exists(master_path):
        with open(master_path, "w", encoding="utf-8") as f:
            f.write(DEFAULT_IGNORE_CONTENT)
    with open(master_path, "r", encoding="utf-8") as f:
        return f.read()

def merge_sentinel_block(existing_content, new_rules):
    block = f"{BEGIN_SENTINEL}\n{new_rules.strip()}\n{END_SENTINEL}\n"
    if BEGIN_SENTINEL in existing_content and END_SENTINEL in existing_content:
        before = existing_content.split(BEGIN_SENTINEL)[0]
        after = existing_content.split(END_SENTINEL)[1]
        if after.startswith("\n"):
            after = after[1:]
        return before + block + after
    else:
        prefix = existing_content.rstrip() + "\n\n" if existing_content.strip() else ""
        return prefix + block

def sync_ignores(root_dir="."):
    master_rules = ensure_master_ignore(root_dir)
    for target_rel in TARGET_FILES:
        target_path = os.path.join(root_dir, target_rel)
        parent = os.path.dirname(target_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        existing = ""
        if os.path.exists(target_path):
            try:
                with open(target_path, "r", encoding="utf-8") as f:
                    existing = f.read()
            except PermissionError as e:
                print(f"⚠️ Warning: Permission denied reading {target_path}: {e}", file=sys.stderr)
                continue

        merged = merge_sentinel_block(existing, master_rules)
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(merged)
        except PermissionError as e:
            print(f"⚠️ Warning: Permission denied writing to {target_path}: {e}", file=sys.stderr)

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    sync_ignores(root)
    print("✅ Harness ignore files synced successfully.")
