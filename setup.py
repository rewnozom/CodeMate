#!/usr/bin/env python
"""
setup.py

This script serves two purposes:

1. **Environment Setup Mode:**
   --------------------------------
   When executed with the command-line argument `"setupenv"`, this script installs
   development dependencies (from `requirements/dev.txt`) and creates necessary directories
   (`logs`, `temp`, `workspace`, etc.) for setting up the development environment.

   Example usage:
       python setup.py setupenv

2. **Packaging Mode:**
   --------------------------------
   When executed without the `"setupenv"` argument, this script calls `setuptools.setup()`
   with the packaging metadata, allowing the project (`rewnozom-codemate`) to be installed
   as a package and expose the CLI entry point `"cmate"`.

   Example usage:
       python setup.py sdist bdist_wheel
       pip install -e .

   Packaging metadata includes:
       - name: `"rewnozom-codemate"`
       - version: `"0.0.3"`
       - description: `"CodeMate – Din AI-drivna kodassistent"`
       - long_description: `"Contents of README.md"`
       - author: `"Tobias Raanaes"`
       - url: `"https://github.com/rewnozom/CodeMate"`
       - python_requires: `">=3.10"`
"""

import subprocess
import sys
from pathlib import Path
import io
import os
from setuptools import setup, find_packages

# --------------------------------------------------
# Environment Setup Mode
# --------------------------------------------------
if len(sys.argv) > 1 and sys.argv[1] == "setupenv":
    def setup_environment():
        """Set up the development environment:
        
        - Install dependencies from `requirements/dev.txt`.
        - Create necessary directories (`logs`, `temp`, `workspace`, etc.).
        """
        try:
            print("📦 Installing development dependencies from requirements/dev.txt ...")
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
            
            print("✅ Environment setup completed successfully.")
        except Exception as e:
            print(f"❌ Error setting up environment: {str(e)}")
            sys.exit(1)
    
    setup_environment()
    sys.exit(0)

# --------------------------------------------------
# Packaging Mode: Call setuptools.setup()
# --------------------------------------------------

# Project root directory
here = Path(__file__).parent

# Read the long description from README.md
readme_path = here / "README.md"
if readme_path.exists():
    with io.open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
else:
    long_description = "CodeMate – Your AI-powered coding assistant."

setup(
    name="rewnozom-codemate",
    version="0.0.3",
    description="CodeMate – Din AI-drivna kodassistent. Let AI build, improve, and test code for you.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tobias Raanaes",
    author_email="contact@rewnozom.com",
    url="https://github.com/rewnozom/CodeMate",

    # Automatically discover and include packages inside the `cmate` directory
    packages=find_packages(),
    package_dir={"": "."},  # Root-level package directory

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
        "numpy",
        "pandas",
        "openai",
        "anthropic",
        # Add other dependencies as needed.
    ],

    # Define the CLI entry point that runs `cmate/__main__.py`
    entry_points={
        "console_scripts": [
            "cmate = cmate.__main__:app"
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    python_requires=">=3.10",
)
