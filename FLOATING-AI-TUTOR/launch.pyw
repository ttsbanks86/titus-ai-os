"""Floating AI Tutor — Standalone launcher (no terminal window)."""
import subprocess
import sys
import os

def main():
    # Get the directory this script lives in
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_py = os.path.join(script_dir, "src", "main.py")

    # Launch main.py as a detached process with no console window
    creation_flags = (
        subprocess.CREATE_NO_WINDOW        # no console
        | subprocess.DETACHED_PROCESS      # fully detached from parent
    )

    subprocess.Popen(
        [sys.executable, main_py],
        cwd=script_dir,
        creationflags=creation_flags,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
    )

if __name__ == "__main__":
    main()
