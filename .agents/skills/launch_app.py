#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import signal

def main():
    workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    mock_server_dir = os.path.join(workspace_dir, "mock-server")

    print("🚀 Starting local environment for Digital Golf Scorecard...")

    # 1. Start the Mock API Server in the background
    print("👉 Launching Mock API Server (port 3001)...")
    try:
        # Open a log file for mock server output
        log_file = open(os.path.join(workspace_dir, "mock-server.log"), "w")
        mock_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=mock_server_dir,
            stdout=log_file,
            stderr=log_file,
            text=True,
            preexec_fn=os.setsid  # run in a separate process group to allow clean killing
        )
        print("✅ Mock API Server started in the background (logs in mock-server.log)")
    except Exception as e:
        print(f"❌ Failed to start Mock API Server: {e}")
        sys.exit(1)

    # Allow a brief moment for mock server to bind to port
    time.sleep(2)

    # 2. Start the Expo Application in the foreground (interactive)
    print("👉 Launching Expo Application...")
    expo_process = None
    try:
        expo_process = subprocess.Popen(
            ["npm", "run", "start"],
            cwd=workspace_dir
        )
        
        # Wait for Expo to finish (blocks terminal and keeps it interactive)
        expo_process.wait()

    except KeyboardInterrupt:
        print("\n👋 Stopping development servers...")
    except Exception as e:
        print(f"❌ Error during execution: {e}")
    finally:
        # 3. Clean up processes on exit
        print("🧹 Cleaning up background processes...")
        
        if expo_process and expo_process.poll() is None:
            try:
                expo_process.terminate()
            except:
                pass

        if mock_process and mock_process.poll() is None:
            try:
                # Kill the entire process group of the mock server
                os.killpg(os.getpgid(mock_process.pid), signal.SIGTERM)
                print("✅ Mock API Server stopped.")
            except Exception as e:
                print(f"⚠️ Warning: Could not cleanly stop Mock API Server: {e}")
                
        log_file.close()
        print("✨ Local development environment stopped.")

if __name__ == "__main__":
    main()
