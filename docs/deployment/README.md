# docs/deployment/README.md
# Deployment Guide

## Requirements
- Python 3.9+
- Docker (optional)
- Required packages

## Installation Methods

### Standard Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements/prod.txt
```

### Docker Installation
```bash
docker-compose up --build
```

## Configuration
1. Environment setup
2. LLM configuration
3. Workspace setup
4. Logging setup

[More deployment details...](./deployment.md)
