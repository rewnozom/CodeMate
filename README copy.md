# README.md
# CodeMate

A Python-based semi-autonomous agent system designed to assist with code analysis, modifications, and testing within a defined workspace.

## Features

- Automated code analysis and modification
- Test generation and execution
- PySide6 UI integration
- Multi-model LLM support (local and cloud)
- Workflow management and tracking
- Extensive validation system
- Configurable prompts and templates

## Requirements

- Python 3.9+
- PySide6
- Required Python packages listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rewnozom/CodeMate.git
cd CodeMate
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Run setup script:
```bash
python scripts/setup.py
```

## Configuration

1. Copy the example configuration:
```bash
cp config/default.yaml config/local.yaml
```

2. Edit `config/local.yaml` to match your requirements.

## Usage

### Command Line Interface

Start the agent in interactive mode:
```bash
python src/main.py start
```

Process a single request:
```bash
python src/main.py process "your request here"
```

Check agent status:
```bash
python src/main.py status
```

### As a Library

```python
from src.core.agent_coordinator import AgentCoordinator

# Initialize agent
agent = AgentCoordinator()

# Process request
result = await agent.process_request({
    "type": "analyze",
    "data": {"path": "some/file/path"}
})
```

## Development

### Running Tests

```bash
./scripts/run_tests.sh
```

### Code Style

This project follows PEP 8 guidelines. Run linting:
```bash
flake8 src tests
```

## Docker Support

Build and run using Docker:
```bash
docker-compose up --build
```

## Project Structure

```
CodeMate/
├── src/               # Source code
├── tests/            # Test files
├── config/           # Configuration files
├── docs/             # Documentation
├── scripts/          # Utility scripts
├── workspace/        # Agent workspace
├── logs/             # Log files
└── temp/             # Temporary files
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
