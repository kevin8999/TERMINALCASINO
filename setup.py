#!/usr/bin/env python3
"""
Cross-platform script to run Terminal Casino with the virtual environment.
"""
import subprocess
import sys
import os
from pathlib import Path

def create_venv():
    """Create a virtual environment if it doesn't exist."""

    root_dir = Path(__file__).parent
    
    # Determine the venv Python executable
    if sys.platform == "win32":
        venv_python = root_dir / ".venv" / "Scripts" / "activate"
    else:
        venv_python = root_dir / ".venv" / "bin" / "activate"
    
    # Create venv if it doesn't exist
    if not venv_python.exists():
        print(f"Error: Virtual environment not found at {venv_python.parent}")
        subprocess.run("python3 -m venv .venv", shell='/bin/bash', cwd=str(root_dir))
        print("Virtual environment created.")

    # Activate the virtual environment
    if sys.platform == "win32":
        activate_command = f"{venv_python}"
    else:
        activate_command = f"source {venv_python}"
    
    subprocess.run(activate_command, shell='/bin/bash', cwd=str(root_dir))

def install_dependencies():
    """Install dependencies in the virtual environment."""
    root_dir = Path(__file__).parent
    if sys.platform == "win32":
        pip_executable = root_dir / ".venv" / "Scripts" / "pip"
    else:
        pip_executable = root_dir / ".venv" / "bin" / "pip"
    
    subprocess.run(f"{pip_executable} install -r requirements.txt", shell='/bin/bash', cwd=str(root_dir))

    print("\n")
    print("-" * 50, end="\n\n")
    print("✅ Dependencies installed.")
    print("Please activate the virtual environment with:", end="\n\n")

    if sys.platform == "win32":
        print(f"\t{root_dir / '.venv' / 'Scripts' / 'activate'}")
    else:
        print(f"\tsource {root_dir / '.venv' / 'bin' / 'activate'}")

    print()

    print("Then, run the app with:\n\n"
          "\tpython -m casino.main")

    print()
    print("-" * 50)
    print()

if __name__ == "__main__":
    create_venv()
    install_dependencies()
