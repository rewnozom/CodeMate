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
# CodeMate Roadmap - Implementation Status

## Priority Levels:
- 🔴 High Priority: Critical features needed for core functionality
- 🟡 Medium Priority: Important features for enhanced operation
- 🔵 Low Priority: Nice-to-have features for future enhancement
## Core Components

### AgentCoordinator
✅ DONE:
- Full subsystem integration architecture
- Comprehensive error handling system
- Advanced event distribution system
- Audit logging and request tracking
- Dynamic configuration management
- System diagnostics infrastructure
- State-based model selection
- Multi-provider LLM integration

🔴 TODO (High Priority):
- Enhance recovery strategies with ML-based approaches
- Implement advanced workflow checkpointing
- Add dynamic resource management
- Implement auto-scaling capabilities

### WorkflowManager
✅ DONE:
- Async workflow execution engine
- Step-based workflow with dependencies
- Execution time tracking
- Persistent workflow state
- Basic error handling and recovery
- Basic workflow templates

🟡 TODO (Medium Priority):
- Advanced workflow templates
- Enhanced checkpoint/rollback system
- Multi-stage workflow validation
- Parallel workflow execution
- Workflow optimization algorithms

### StateManager
✅ DONE:
- State transitions with validation
- State persistence and history
- Observer pattern implementation
- Context window management
- Error tracking system
- State metadata handling

🟡 TODO (Medium Priority):
- Enhanced state prediction
- State optimization algorithms
- Advanced state recovery mechanisms
- Cross-state dependency tracking

### MemoryManager
✅ DONE:
- Multi-tier memory system
- Automatic cleanup
- Priority-based management
- Memory statistics
- Memory consolidation
- Token-based memory limits

🔵 TODO (Low Priority):
- Advanced memory indexing
- Memory optimization strategies
- Cross-reference memory items
- Enhanced memory persistence

## System Features

### Event System
✅ DONE:
- Event bus implementation
- Publisher/Subscriber pattern
- Event filtering
- Basic event persistence
- Event history tracking

🟡 TODO:
- Enhanced event routing
- Event prioritization
- Advanced event filtering
- Event analytics

### Request/Response Handling
✅ DONE:
- Request validation
- Response formatting
- Error handling
- Request queuing
- Basic rate limiting

🔴 TODO:
- Advanced rate limiting
- Request prioritization
- Response optimization
- Enhanced validation rules

### LLM Integration
✅ DONE:
- Multi-provider support
- State-based model selection
- Context management
- Response parsing
- Error handling

🟡 TODO:
- Enhanced prompt optimization
- Response caching
- Provider fallback system
- Context optimization

### File Services
✅ DONE:
- Basic file analysis
- Workspace scanning
- File change detection
- Basic dependency tracking

🟡 TODO:
- Enhanced dependency analysis
- Code structure visualization
- Advanced file categorization
- Pattern detection

### Validation System
✅ DONE:
- Basic validation strategies
- Frontend/Backend validation
- Implementation validation
- Test management

🔴 TODO:
- Dynamic rule generation
- Cross-file validation
- Enhanced test coverage
- Validation optimization

## Advanced Features

### Performance Optimization
✅ DONE:
- Basic metrics collection
- Resource monitoring
- Performance logging
- Basic caching

🔵 TODO:
- Advanced caching strategies
- Resource optimization
- Performance analytics
- Auto-scaling system

### Monitoring & Diagnostics
✅ DONE:
- Basic system metrics
- Error tracking
- Process monitoring
- Log analysis

🟡 TODO:
- Enhanced metrics collection
- Real-time monitoring
- Advanced diagnostics
- Performance predictions

### External Integration
✅ DONE:
- Basic Git integration
- Terminal management
- Process management

🔵 TODO:
- Enhanced Git integration
- CI/CD integration
- IDE integration
- External API integration

## Implementation Statistics:
- Core Components: ~75% Complete
- System Features: ~60% Complete
- Advanced Features: ~30% Complete
- Overall Project: ~60% Complete

## Next Steps:
1. Focus on high-priority error recovery enhancements
2. Implement advanced workflow templates
3. Enhance validation system with dynamic rules
4. Improve performance optimization
5. Develop advanced monitoring capabilities



---
---


# **CodeMate – Your AI-Powered Coding Assistant**

### 🤖 _Advanced AI Integration for Code Development, Analysis, and Testing_

**CodeMate** is a sophisticated **semi-autonomous coding assistant** that leverages multiple AI models to help you develop, analyze, and test code effectively. It uses state-based model selection to optimize AI responses for different tasks while ensuring all modifications are properly tested and integrated.

## 🔹 **Key Features**

### 1. **Advanced AI Integration**
- Multi-provider LLM support (Anthropic, OpenAI, Azure, Groq, LM Studio)
- State-based model selection for optimized responses
- Dynamic context management and token optimization
- Comprehensive error recovery and fallback systems

### 2. **Intelligent Codebase Analysis**
- Deep scanning of `./Workspace/` for project structure
- Automatic identification of frontend/backend components
- Dependency tracking and analysis
- File change monitoring and impact assessment

### 3. **Sophisticated Task Management**
- Automated task planning and workflow creation
- Interactive progress tracking with checklists
- Event-driven task orchestration
- Persistent state management with rollback capability

### 4. **Automated Code Operations**
- Context-aware code generation
- Intelligent code integration
- Style-preserving modifications
- Cross-component compatibility checks

### 5. **Comprehensive Testing**
- Automated test generation and execution
- Multi-level validation (frontend, backend, implementation)
- Test coverage analysis
- Failure recovery and code adjustment

### 6. **Advanced Monitoring**
- Detailed audit logging
- Performance metrics collection
- System diagnostics
- Error tracking and analysis

## 🔧 **System Requirements**

- Python 3.8+
- Storage: Minimum 1GB free space
- Memory: Minimum 4GB RAM recommended
- API Keys for desired LLM providers

## 📦 **Installation**

### 1. **Standard Installation**
```bash
# Navigate to project root
cd codemate

# Install package
pip install .
```

### 2. **Development Installation**
```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### 3. **Environment Setup**
```bash
# Set up development environment
python scripts/setup.py setupenv
```

This creates required directories (`logs/`, `temp/`, `workspace/`) and installs dependencies.

## ⚙️ **Configuration**

### 1. **Environment Variables**
Create a `.env` file with your configuration:
```env
# LLM Provider Settings
LLM_PROVIDER=lm_studio
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
AZURE_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# System Settings
CONTEXT_WINDOW=60000
TEMPERATURE=0.7
DEBUG=false
LOG_LEVEL=INFO
```

### 2. **Provider Selection**
CodeMate automatically selects the optimal model based on the current task:
- Code Generation: Uses specialized coding models
- Test Writing: Employs testing-focused models
- Analysis: Utilizes models optimized for comprehension

## 🖥️ **CLI Usage**

### Basic Commands
```bash
# Start interactive mode
cmate start

# Process a single request
cmate process "Analyze the project structure"

# Check system status
cmate status

# Display help
cmate --help
```

### Interactive CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `analyze` | Analyze code/directory | `analyze ./Workspace/` |
| `execute` | Run workflow | `execute build_pipeline` |
| `generate` | Generate code | `generate "Create login form"` |
| `visualize` | Show workflow | `visualize` |
| `config` | View/edit config | `config` |
| `diagnostics` | System diagnostics | `diagnostics` |
| `audit` | View audit logs | `audit` |

## 📊 **Advanced Usage Examples**

### 1. **Code Analysis**
```bash
agent> analyze ./Workspace/src
```
```output
Analysis Results:
- Project Structure
- Dependencies
- Code Metrics
- Potential Issues
```

### 2. **Code Generation**
```bash
agent> generate "Create a user authentication system"
```
```output
Generating:
6. User model
7. Authentication endpoints
8. Security middleware
9. Unit tests
```

### 3. **Configuration Updates**
```bash
agent> update debug_mode True
```
```output
Configuration updated:
- Debug mode enabled
- Enhanced logging activated
```

## 🔍 **Monitoring & Diagnostics**

### 1. **Audit Logs**
```bash
agent> audit
```
Shows recent operations, changes, and system events.

### 2. **Error Tracking**
```bash
agent> error
```
Displays error history with recovery attempts.

### 3. **System Diagnostics**
```bash
agent> diagnostics
```
Shows system health, resource usage, and performance metrics.

## 🛠️ **Error Handling**

CodeMate includes sophisticated error recovery:
10. Automatic error detection and classification
11. Recovery strategy selection
12. State preservation and rollback capability
13. Detailed error reporting and logging

## 📚 **Best Practices**

14. **Workspace Organization**
   - Keep workspace clean and organized
   - Use consistent file naming
   - Maintain clear directory structure

15. **Request Formulation**
   - Be specific in requests
   - Provide context when needed
   - Use proper command syntax

16. **Configuration Management**
   - Regularly update API keys
   - Monitor resource usage
   - Review audit logs

---

*CodeMate: Empowering Developers with AI-Driven Code Development*
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

