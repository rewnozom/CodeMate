# Project Details

# Table of Contents
- [..\scripts\deploy.sh](#-scripts-deploysh)
- [..\scripts\run_tests.sh](#-scripts-run_testssh)
- [..\scripts\setup.py](#-scripts-setuppy)
- [..\scripts\__init__.py](#-scripts-__init__py)


# ..\..\scripts\deploy.sh
## File: ..\..\scripts\deploy.sh

```sh
# ..\..\scripts\deploy.sh
# scripts/deploy.sh
#!/bin/bash

# Deploy script
echo "Deploying agent system..."

# Create dist directory
mkdir -p dist

# Clean previous build
rm -rf dist/*

# Copy source files
cp -r src dist/
cp -r config dist/

# Copy requirements
cp requirements/prod.txt dist/requirements.txt

# Create necessary directories
mkdir -p dist/logs
mkdir -p dist/temp
mkdir -p dist/workspace

echo "Deployment completed"
```

---

# ..\..\scripts\run_tests.sh
## File: ..\..\scripts\run_tests.sh

```sh
# ..\..\scripts\run_tests.sh
# scripts/run_tests.sh
#!/bin/bash

# Run all tests
echo "Running tests..."
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

# ..\..\scripts\setup.py
## File: ..\..\scripts\setup.py

```py
# ..\..\scripts\setup.py
#!/usr/bin/env python
"""
scripts/setup.py

This script serves two purposes:

1. Environment Setup Mode:
   --------------------------
   When executed with the command-line argument "setupenv", this script installs
   development dependencies (from requirements/dev.txt) and creates necessary directories
   (logs, temp, workspace, etc.). This helps set up your development environment.

   Example usage:
       python scripts/setup.py setupenv

2. Packaging Mode:
   ---------------
   When executed without the "setupenv" argument, this script calls setuptools.setup()
   with the packaging metadata so that your project (named "rewnozom-codemate") can be
   installed as a package and expose the CLI entry point "cmate". You can install the package
   using pip (e.g., pip install -e .).

   Packaging metadata includes:
       - name: "rewnozom-codemate"
       - version: "0.0.03"
       - description: A brief description of CodeMate
       - long_description: The contents of README.md (in Markdown)
       - author: "Tobias Raanaes"
       - url: "https://github.com/rewnozom/CodeMate"
       - python_requires: ">=3.10"

Usage:
  For environment setup:
      python scripts/setup.py setupenv

  For packaging (this is typically invoked via pip or build tools):
      python scripts/setup.py sdist bdist_wheel
"""

import subprocess
import sys
from pathlib import Path
import io
import os

# --------------------------------------------------
# Environment Setup Mode
# --------------------------------------------------
if len(sys.argv) > 1 and sys.argv[1] == "setupenv":
    def setup_environment():
        """Set up the development environment:
        
        - Install dependencies from requirements/dev.txt.
        - Create necessary directories (logs, temp, workspace, etc.).
        """
        try:
            print("Installing development dependencies from requirements/dev.txt ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements/dev.txt"])
            
            # List of directories to create
            directories = [
                "logs",
                "logs/metrics",
                "logs/errors",
                "temp",
                "temp/cache",
                "temp/workflow_states",
                "workspace"
            ]
            
            for directory in directories:
                Path(directory).mkdir(parents=True, exist_ok=True)
            
            print("Environment setup completed successfully.")
        except Exception as e:
            print(f"Error setting up environment: {str(e)}")
            sys.exit(1)
    
    setup_environment()
    sys.exit(0)

# --------------------------------------------------
# Packaging Mode: Call setuptools.setup()
# --------------------------------------------------
from setuptools import setup, find_packages

# Read the long description from README.md (assumes README.md is in the project root)
here = Path(__file__).parent.parent  # scripts folder's parent is the project root
readme_path = here / "README.md"
if readme_path.exists():
    with io.open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = ""

setup(
    name="rewnozom-codemate",
    version="0.0.03",
    description="CodeMate – Din AI-drivna kodassistent. Let AI build, improve, and test code for you.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tobias Raanaes",
    url="https://github.com/rewnozom/CodeMate",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "typer",
        "rich",
        "prompt_toolkit",
        "watchdog",
        "psutil",
        "python-dotenv",
        "transformers",
        # Add other dependencies as needed.
    ],
    entry_points={
        "console_scripts": [
            "cmate = cmate.main:app"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

```

---

# ..\..\scripts\__init__.py
## File: ..\..\scripts\__init__.py

```py
# ..\..\scripts\__init__.py
# Auto-generated __init__.py file

```

---

