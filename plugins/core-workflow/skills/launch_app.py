#!/usr/bin/env python3
import os, subprocess, sys

def main():
    cwd = os.environ.get("PROJECT_ROOT", os.getcwd())
    cmd = os.environ.get("LAUNCH_CMD")

    print(f"🚀 Starting app in {cwd}...")
    if not cmd:
        # ponytail: heuristic auto-detect
        if os.path.exists(os.path.join(cwd, "docker-compose.yml")):
            cmd = "docker compose up"
        elif os.path.exists(os.path.join(cwd, "manage.py")):
            cmd = "source .venv/bin/activate && python manage.py runserver"
        elif os.path.exists(os.path.join(cwd, "package.json")):
            cmd = "npm start"
        else:
            print("❌ No LAUNCH_CMD set and no auto-detectable config found.")
            sys.exit(1)

    print(f"👉 Executing: {cmd}")
    try:
        subprocess.run(["bash", "-c", cmd], cwd=cwd)
    except KeyboardInterrupt:
        print("\n👋 Stopped.")
    finally:
        if "docker compose" in cmd:
            subprocess.run(["bash", "-c", "docker compose down"], cwd=cwd, stderr=subprocess.DEVNULL)

if __name__ == "__main__": main()
