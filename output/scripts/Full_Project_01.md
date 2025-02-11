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

# File: ..\..\scripts\setup.py

**Binary file cannot be displayed.**

---

# ..\..\scripts\__init__.py
## File: ..\..\scripts\__init__.py

```py
# ..\..\scripts\__init__.py
# Auto-generated __init__.py file

```

---

