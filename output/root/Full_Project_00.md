# Project Details

# Table of Contents
- [..\.dockerignore](#-dockerignore)
- [..\.editorconfig](#-editorconfig)
- [..\.env.development](#-envdevelopment)
- [..\.env.example](#-envexample)
- [..\.env.production](#-envproduction)
- [..\.gitignore](#-gitignore)
- [..\.gitlab-ci.yml](#-gitlab-ciyml)
- [..\.pre-commit-config.yaml](#-pre-commit-configyaml)
- [..\__init__.py](#-__init__py)
- [..\cli_CodeMate.bat](#-cli_CodeMatebat)
- [..\create_init_to_all_directories.py](#-create_init_to_all_directoriespy)
- [..\docker-compose.dev.yml](#-docker-composedevyml)
- [..\docker-compose.yml](#-docker-composeyml)
- [..\install_CodeMate.bat](#-install_CodeMatebat)
- [..\Makefile](#-Makefile)
- [..\open_CodeMate.bat](#-open_CodeMatebat)
- [..\pyproject.toml](#-pyprojecttoml)
- [..\pytest.ini](#-pytestini)
- [..\README copy.md](#-README-copymd)
- [..\README.md](#-READMEmd)
- [..\remove-pycache-script.ps1](#-remove-pycache-scriptps1)
- [..\run_CodeMate.bat](#-run_CodeMatebat)
- [..\setup.cfg](#-setupcfg)
- [..\tox.ini](#-toxini)


# ..\..\.dockerignore
## File: ..\..\.dockerignore

```
# ..\..\.dockerignore
# .dockerignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.venv
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.pytest_cache/
.mypy_cache/
.hypothesis/
.gitignore
.git/
docs/
tests/
*.md
Dockerfile
docker-compose.yml
```

---

# ..\..\.editorconfig
## File: ..\..\.editorconfig

```
# ..\..\.editorconfig
# .editorconfig
# EditorConfig is awesome: https://EditorConfig.org

# top-most EditorConfig file
root = true

[*]
end_of_line = lf
insert_final_newline = true
charset = utf-8
trim_trailing_whitespace = true

[*.{py,ini,yaml,yml,json}]
indent_style = space
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab

```

---

# File: ..\..\.env.development

**Binary file cannot be displayed.**

---

# ..\..\.env.example
## File: ..\..\.env.example

```example
# ..\..\.env.example
# ==============================================
# LLM Configuration
# ==============================================
LLM_PROVIDER=lm_studio
CONTEXT_WINDOW=60000
TEMPERATURE=0.7
LM_STUDIO_BASE_URL=http://localhost:1234/v1
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# ==============================================
# Workspace & System Configuration
# ==============================================
WORKSPACE_PATH=./workspace
MAX_FILES_PER_SCAN=10

# ==============================================
# Development Settings
# ==============================================
DEBUG=false
LOG_LEVEL=INFO

# ==============================================
# Agent Settings
# ==============================================
AUTO_TEST=true

```

---

# File: ..\..\.env.production

**Binary file cannot be displayed.**

---

# ..\..\.gitignore
## File: ..\..\.gitignore

```
# ..\..\.gitignore
# .gitignore

# ---------------------------
# 🐍 Python & Virtual Environments
# ---------------------------
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment (common names)
venv/
.venv/
env/
ENV/
.env

# ---------------------------
# 🛠 IDE / Editor Config Files
# ---------------------------
.idea/
.vscode/
*.swp
*.swo
*.swn
.DS_Store

# ---------------------------
# 🔧 Project-specific Files
# ---------------------------
logs/
logs/*.log  # Ignore all log files
temp/
output/     # Ignore all generated output files
workspace/*
!workspace/.gitkeep  # Keep workspace folder but ignore contents

# ---------------------------
# ✅ Testing & Coverage Reports
# ---------------------------
.coverage
coverage.xml
htmlcov/
.pytest_cache/
pytest_debug.log

# ---------------------------
# 🚀 Node.js / Frontend (if applicable)
# ---------------------------
node_modules/
package-lock.json
yarn.lock

# ---------------------------
# 🔍 Miscellaneous
# ---------------------------
*.bak  # Backup files
*.tmp  # Temporary files
*.swp  # Swap files from editors
*.log  # Any log files
*.out  # Output binary files

```

---

# ..\..\.gitlab-ci.yml
## File: ..\..\.gitlab-ci.yml

```yml
# ..\..\.gitlab-ci.yml
# .gitlab-ci.yml
image: python:3.10

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

cache:
  paths:
    - .pip-cache/
    - venv/

stages:
  - test
  - build
  - deploy

before_script:
  - python -V
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements/dev.txt

test:
  stage: test
  script:
    - flake8 src tests
    - black --check src tests
    - isort --check-only src tests
    - mypy src tests
    - pytest tests/ -v --cov=src --cov-report=term-missing
  coverage: '/TOTAL.+ ([0-9]{1,3}%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  script:
    - python -m build
  artifacts:
    paths:
      - dist/
  only:
    - main

deploy:
  stage: deploy
  script:
    - pip install twine
    - TWINE_USERNAME=${PYPI_USERNAME} TWINE_PASSWORD=${PYPI_PASSWORD} twine upload dist/*
  only:
    - main
  when: manual
```

---

# ..\..\.pre-commit-config.yaml
## File: ..\..\.pre-commit-config.yaml

```yaml
# ..\..\.pre-commit-config.yaml
# .pre-commit-config.yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
    -   id: debug-statements
    -   id: check-ast

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-docstrings]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-all]

```

---

# ..\..\__init__.py
## File: ..\..\__init__.py

```py
# ..\..\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\cli_CodeMate.bat
## File: ..\..\cli_CodeMate.bat

```bat
# ..\..\cli_CodeMate.bat
@echo off
cd /d "C:\Users\Tobia\CodeMate"
"C:\Users\Tobia\AppData\Local\Programs\Python\Python310\python.exe" -m src.core.main
pause

```

---

# File: ..\..\create_init_to_all_directories.py

**Binary file cannot be displayed.**

---

# ..\..\docker-compose.dev.yml
## File: ..\..\docker-compose.dev.yml

```yml
# ..\..\docker-compose.dev.yml
# docker-compose.dev.yml
version: '3.8'

services:
  agent:
    build:
      context: .
      dockerfile: docker/Dockerfile.dev
    volumes:
      - .:/app
      - ./workspace:/app/workspace
    environment:
      - PYTHONPATH=/app
      - DEBUG=true
    ports:
      - "8000:8000"
    depends_on:
      - lm-studio
    networks:
      - agent_network

  lm-studio:
    image: lmstudio/lmstudio:latest
    ports:
      - "1234:1234"
    volumes:
      - ./models:/models
    environment:
      - MODEL_PATH=/models
    networks:
      - agent_network

networks:
  agent_network:
    driver: bridge

# docker-compose.prod.yml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - agent
    networks:
      - agent_network

  agent:
    build:
      context: .
      dockerfile: docker/Dockerfile.prod
    expose:
      - "8000"
    environment:
      - PYTHONPATH=/app
    volumes:
      - workspace_data:/app/workspace
    depends_on:
      - lm-studio
    networks:
      - agent_network

  lm-studio:
    image: lmstudio/lmstudio:latest
    expose:
      - "1234"
    volumes:
      - model_data:/models
    environment:
      - MODEL_PATH=/models
    networks:
      - agent_network

volumes:
  workspace_data:
  model_data:

networks:
  agent_network:
    driver: bridge
```

---

# ..\..\docker-compose.yml
## File: ..\..\docker-compose.yml

```yml
# ..\..\docker-compose.yml
# docker-compose.yml
version: '3.8'

services:
  agent:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./workspace:/app/workspace
      - ./logs:/app/logs
      - ./config:/app/config
    environment:
      - PYTHONPATH=/app
      - WORKSPACE_PATH=/app/workspace
    ports:
      - "8000:8000"  # If needed for API
    networks:
      - agent_network

  lm-studio:  # Optional local LLM service
    image: lmstudio/lmstudio:latest
    ports:
      - "1234:1234"
    volumes:
      - ./models:/models
    environment:
      - MODEL_PATH=/models
    networks:
      - agent_network

networks:
  agent_network:
    driver: bridge



```

---

# ..\..\install_CodeMate.bat
## File: ..\..\install_CodeMate.bat

```bat
# ..\..\install_CodeMate.bat
@echo off
cd /d "C:\Users\Tobia\CodeMate"
"C:\Users\Tobia\AppData\Local\Programs\Python\Python310\python.exe" -m pip install -r requirements.txt
pause

```

---

# ..\..\Makefile
## File: ..\..\Makefile

```
# ..\..\Makefile
# Makefile
.PHONY: install test lint format clean docs

install:
	pip install -r requirements/dev.txt
	pre-commit install

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	flake8 src tests
	mypy src tests
	black --check src tests
	isort --check-only src tests

format:
	black src tests
	isort src tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +

docs:
	sphinx-build -b html docs/source docs/build/html

```

---

# ..\..\open_CodeMate.bat
## File: ..\..\open_CodeMate.bat

```bat
# ..\..\open_CodeMate.bat
@echo off
cd /d "C:\Users\Tobia\CodeMate"
code .

```

---

# ..\..\pyproject.toml
## File: ..\..\pyproject.toml

```toml
# ..\..\pyproject.toml
# pyproject.toml

[build-system]
requires = [
    "setuptools>=42",
    "wheel"
]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 88
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | _build
  | buck-out
  | build
  | dist
)/'''

[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
line_length = 88

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q"
testpaths = [
    "tests",
]
python_files = ["test_*.py"]
python_classes = ["Test"]
python_functions = ["test_"]

[tool.mypy]
python_version = "3.10"  # Ensuring Python 3.10 compatibility
warn_return_any = true
warn_unused_configs = true
ignore_missing_imports = true

[tool.setuptools]
package-dir = { "" = "src" }
packages = "find:"

```

---

# ..\..\pytest.ini
## File: ..\..\pytest.ini

```ini
# ..\..\pytest.ini
# pytest.ini
[pytest]
minversion = 6.0
addopts = -ra -q --cov=src --cov-report=term-missing
testpaths =
    tests
python_files =
    test_*.py
    *_test.py
python_classes =
    Test
    *Tests
python_functions =
    test_*
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests

```

---

# File: ..\..\README copy.md

**Binary file cannot be displayed.**

---

# ..\..\README.md
## File: ..\..\README.md

```md
# ..\..\README.md
# **Roadmap for CodeMate 🚀**

## Overview

CodeMate aims to deliver a **robust, scalable, and efficient** platform with a focus on:

### **Core Components:**
- **AgentCoordinator**
- **WorkflowManager**
- **StateManager**
- **MemoryManager**

### **Missing Modules (To Be Built from Scratch):**
- **LLM Integration Module**
- **Code Generation Module**
- **Project Analysis Module**
- **Code Analysis API**
- **Validation Strategies & Dynamic Rule Generation**
- **Context Priority & Persistence System**

### **Critical Integrations:**
- **Event System Integration** (including persistence, filtering & routing)
- **Memory System Integration**
- **Validation System Integration**
- **Central Integration Layer**

### **Additional Features & Optimizations:**
- **Request Validation** (with rate limiting & prioritization)
- **Memory Optimization & Indexing**
- **Template Management System**
- **Task Orchestration, ResourceMonitor, DependencyGraph, MilestoneTracker, and TaskEventBus**

---

## **Priority Order**

- 🔴 **High Priority:** Critical features that must be implemented first.
- 🟡 **Medium Priority:** Enhancements for integration, performance, and robustness.
- 🔵 **Low Priority:** Advanced features and optimizations that can be developed later.

---

## **Phase 1 – Core Functionality (High Priority) 🔴**

### **AgentCoordinator**
- Implement the **LLM Integration Module** for AI-assisted operations.
- Improve error handling with **Error Recovery** strategies.
- Introduce **Task Orchestration** to coordinate complex tasks.

### **WorkflowManager**
- Complete implementation of workflow stages:
  - File Analysis
  - Planning
  - Implementation
  - Testing
  - Validation
  - User Interaction
- Introduce **workflow templates** & **checkpointing**.

### **StateManager**
- Enforce strict **state transition validation** to prevent invalid transitions.
- Implement rollback functionality and **state persistence** (with history cleanup).

### **Event System**
- Connect event handling across all core components.
- Implement **Event Persistence** with basic filtering and routing.

### **Request Validation**
- Implement a robust **Request Validation System** (structure, content, rate limiting, and prioritization).

---

## **Phase 2 – Extended Integration (Medium Priority) 🟡**

### **Missing Modules**
- **Code Generation Module:** Automatic code generation with syntax validation and style formatting.
- **Project Analysis Module:** Analyze project structure with **dependency graphs, code metrics, and pattern detection**.
- **Code Analysis API:** Deeper code analysis, metric calculation, and issue detection.

### **Memory & Context**
- **Memory System Integration:** Connect MemoryManager with ContextManager and WorkflowManager for long-term persistence and optimization.
- **Context Priority & Persistence:** Introduce priority logic and storage for relevant context data.

### **Validation**
- Develop a **Validation Coordinator** with a **Rule Engine**.
- Introduce basic **Validation Strategies** (e.g., for Python and JavaScript) along with **dynamic rule generation**.

### **Testing Infrastructure**
- Build a **comprehensive testing environment** with unit, integration, and performance tests.

### **Extended Error Handling**
- Improve recovery strategies and **centralized error handling**.

### **Event System (Enhancements)**
- Improve filtering, routing, and prioritization (including **TaskEventBus**).

---

## **Phase 3 – Advanced Features (Low Priority) 🔵**

### **External Integration**
- Connect to external tools such as **Git, CI/CD systems, and IDE integrations**.

### **Task Management & Orchestration**
- Advanced process group management, including:
  - **ResourceMonitor** for ProcessManager
  - **DependencyGraph** for TaskPrioritizer
  - **MilestoneTracker** for ProgressTracker
  - Extended **Task Orchestration** via **TaskEventBus**

### **Performance Optimizations**
- Implement **Memory Optimization & Indexing** strategies.
- Introduce **caching** (result cache & memory cache), **batch processing**, and **asynchronous operations**.

### **Template & Integration Layer**
- Develop a **Template Management System** for response templates.
- Build a **central Integration Layer** to coordinate system components.

### **Comprehensive Monitoring**
- Implement a **system monitoring solution** to collect performance and integration metrics.

---

## **Detailed Task List by Component**

### **AgentCoordinator**
- 🔴 Implement **LLM Integration Module**.
- 🔴 Improve **error recovery** and expand audit trail.
- 🔴 Implement **Task Orchestration**.

### **WorkflowManager**
- 🔴 Complete implementation of **all workflow stages**.
- 🔴 Introduce **workflow templates** and **checkpointing**.
- 🟡 Enhance rollback functions and advanced error handling.

### **StateManager**
- 🔴 Enforce **state transition validation**.
- 🔴 Implement **rollback and state persistence**.
- 🟡 Improve **cleanup policies**.

### **File Services (FileAnalyzer & WorkspaceScanner)**
- 🟡 Finalize implementation for **JavaScript, HTML, CSS**.
- 🟡 Introduce **dependency graph generation**.
- 🟡 Optimize **file change detection** and **file categorization**.

### **Validation & Testing**
- 🔴 Implement **basic Validation Strategies**.
- 🔴 Connect a **Validation Coordinator** with a **Rule Engine**.
- 🟡 Introduce **cross-file validation** and **dynamic rule generation**.
- 🟡 Build a **robust testing infrastructure**.

### **Interfaces (CLIInterface & ResponseFormatter)**
- 🟡 Implement **command history, tab-completion, and interactive workflow visualization**.
- 🟡 Introduce **ANSI color support, custom templates, and pagination**.

### **Storage (CacheManager & PersistenceManager)**
- 🟡 Implement **cache compression** and **cache invalidation strategies**.
- 🟡 Support for multiple storage backends and **data migration systems**.
- 🔵 Backup verification.

### **Task Management (ChecklistManager, ProcessManager, etc.)**
- 🟡 Implement **checklist templates** and **recurring task support**.
- 🟡 Introduce **resource monitoring, process prioritization, and group handling**.
- 🟡 Implement **ResourceMonitor, DependencyGraph, and TaskEventBus**.
- 🔵 Advanced **process group management** and **task orchestration**.
- 🔵 Introduce **MilestoneTracker** for progress tracking.

### **Integrations & Additional Features**
- 🔴 Implement **Request Validation System** with **rate limiting and prioritization**.
- 🟡 **Memory System Integration** (connect MemoryManager with ContextManager & WorkflowManager).
- 🟡 Introduce **Context Priority & Persistence System**.
- 🟡 Develop **Code Generation Module** and **Project Analysis Module**.
- 🟡 Implement **Code Analysis API** and **Validation Coordinator** with a **Rule Engine**.
- 🟡 Improve **Event System Integration** (including persistence, filtering & routing).
- 🔵 External integration (**Git, CI/CD, IDE**).
- 🔵 Develop **Template Management System**.
- 🔵 Build a **central Integration Layer**.
- 🔵 Implement **comprehensive monitoring and metrics**.

---

# **CodeMate – Your AI-Powered Coding Assistant**  

### 🤖 _Let AI Build, Improve, and Test Code for You_  

**CodeMate** is a **semi-autonomous coding assistant** that helps you **develop new features step by step in a safe manner** while **automatically testing each implementation**. It analyzes the codebase, identifies relevant files, and ensures all modifications function correctly before being integrated into the system.

---

## 🔹 **How Does CodeMate Work?**  

1. **Understands Your Codebase**  
   - Scans all files in `./Workspace/` and creates a **project overview**.  
   - Automatically identifies **key files for frontend and backend**.

2. **Plans & Executes Tasks Step by Step**  
   - When you provide a prompt/instruction, CodeMate creates a **task plan** with clear steps.  
   - Uses an **interactive checklist** to track progress.

3. **Builds & Fixes Code Automatically**  
   - **Implements new features** based on your description.  
   - Analyzes existing code to determine **where and how to integrate** the new functionality.  
   - Ensures that frontend and backend work seamlessly together.

4. **Tests All Changes Automatically**  
   - Creates and runs tests to validate both **new features and bug fixes**.  
   - Adjusts the code if anything fails during tests.

5. **Tracks Project Progress**  
   - Stores data in a **temporary workspace**, so nothing is lost if a rollback is needed.  
   - **Works until the entire task is completed**, whether it’s adding a new feature or refining existing code.

6. **Stays Ready for Next Assignments**  
   - Once everything is done and tested, CodeMate reverts to **standby mode** and awaits your next instruction.

---

## **CLI Usage (Basic Examples)**

```bash
python src/main.py start  # Start CodeMate in interactive mode
python src/main.py process "your request here"  # Process a single request
python src/main.py --help  # Show all available commands and options
```

---

# **CLI Commands in Table Format**

| **Command**      | **Description**                                 | **Example Usage**                                   |
|------------------|-------------------------------------------------|-----------------------------------------------------|
| `start`          | Start the agent (interactive or non-interactive)| `python src/main.py start`<br>`python src/main.py start --interactive=False` |
| `process`        | Process a single request                        | `python src/main.py process "Analyze all files"`   |
| `status`         | Check agent status                              | `python src/main.py status`                        |
| `--help`         | Display usage instructions and help             | `python src/main.py --help`                        |
| **Below commands appear inside the interactive CLI** |  |  |
| `analyze`        | Analyze a file or directory                     | `analyze ./Workspace/`                             |
| `execute`        | Execute a workflow                              | `execute build_pipeline`                           |
| `status` (CLI)   | Display current agent status                    | `status`                                           |
| `config`         | View current configuration                      | `config`                                           |
| `update`         | Dynamically update configuration                | `update debug_mode True`                           |
| `visualize`      | Visualize the active workflow                   | `visualize`                                        |
| `refresh`        | Refresh the LLM context                         | `refresh`                                          |
| `generate`       | Generate code from a given prompt               | `generate "Create a new user registration form"`   |
| `git`            | Simulate Git integration                        | `git`                                              |
| `diagnostics`    | Run system diagnostics                          | `diagnostics`                                      |
| `audit`          | Show recent audit log entries                   | `audit`                                            |
| `error`          | Show error history                              | `error`                                            |
| `history`        | Show CLI command history                        | `history`                                          |
| `debug`          | Display detailed system info & internal state   | `debug`                                            |
| `clear`          | Clear the screen                                | `clear`                                            |
| `exit`           | Exit the CLI                                    | `exit`                                             |


### **Command Examples** (CLI Mode)

<details>
<summary><strong>Example 1: Analyzing a Directory</strong></summary>

```bash
# Within the interactive CLI
agent> analyze ./Workspace/
```

**Output**:
```
Analyze Request Result:
[Detailed analysis results...]
```
</details>

<details>
<summary><strong>Example 2: Updating Configuration</strong></summary>

```bash
agent> update debug_mode True
```

**Output**:
```
Configuration updated: debug_mode set to True
```
</details>

<details>
<summary><strong>Example 3: Generating Code</strong></summary>

```bash
agent> generate "Create a simple login page"
```

**Output**:
```
Generated Code:
[Rendered HTML/JS code here...]
```
</details>


---

# **Installation and Usage**

## **1. Install the Package**

1. **Navigate to your project root** (where the `setup.py` and `pyproject.toml` reside).
2. **Install** using `pip install .` (or `pip install -e .` for development mode).

```bash
# Standard installation
pip install .

# or if you want an editable install
pip install -e .
```

This will install the `rewnozom-codemate` package and register the `cmate` CLI entry point on your system (if the environment’s `bin` or `Scripts` folder is on PATH).

## **2. Use the `cmate` Command**

After installing, you can invoke CodeMate via the `cmate` command instead of `python src/main.py`:

```bash
cmate start
cmate start --interactive=False
cmate process "Analyze all files and create a test plan"
cmate status
cmate --help
```

**Example**:
```bash
# Start CodeMate in interactive mode:
cmate start
```

**Non-interactive mode**:
```bash
cmate start --interactive=False
```

**Process a single request**:
```bash
cmate process "Analyze the data pipeline"
```

## **3. (Optional) Environment Setup**

If you need to set up a development environment (install dev dependencies, create logs/temp directories, etc.):

```bash
python scripts/setup.py setupenv
```

This will:
- Install development dependencies from `requirements/dev.txt`
- Create directories: `logs/`, `temp/`, `workspace/`, etc.

```

---

# File: ..\..\remove-pycache-script.ps1

**Binary file cannot be displayed.**

---

# File: ..\..\run_CodeMate.bat

**Binary file cannot be displayed.**

---

# ..\..\setup.cfg
## File: ..\..\setup.cfg

```cfg
# ..\..\setup.cfg
[metadata]
name = rewnozom-codemate
version = 0.0.03
author = Tobias Raanaes
author_email = contact@rewnozom.com  ; Use a generic email here if desired.
description = CodeMate – Your AI-driven code assistant for building, improving, and testing code.
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/rewnozom/CodeMate
project_urls =
    Bug Tracker = https://github.com/rewnozom/CodeMate/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.10
install_requires =
    pyside6>=6.0.0
    anthropic>=0.3.0
    openai>=1.0.0
    python-dotenv>=0.19.0
    rich>=10.0.0
    typer>=0.4.0
    pyyaml>=6.0.0

[options.packages.find]
where = src

[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,build,dist,*.egg

[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
ignore_missing_imports = True

[coverage:run]
source = src
omit = tests/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    raise NotImplementedError
    if __name__ == '__main__':
    pass
    raise ImportError

```

---

# ..\..\tox.ini
## File: ..\..\tox.ini

```ini
# ..\..\tox.ini
# tox.ini
[tox]
envlist = py39, py310, lint
isolated_build = True

[testenv]
deps =
    -r{toxinidir}/requirements/dev.txt
commands =
    pytest tests/ -v --cov=src

[testenv:lint]
deps =
    flake8
    black
    isort
    mypy
commands =
    flake8 src tests
    black --check src tests
    isort --check-only src tests
    mypy src tests
```

---

