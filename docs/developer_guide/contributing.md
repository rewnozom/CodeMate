# docs/developer_guide/contributing.md
# Contributing Guide

## Development Setup

1. Fork and clone the repository
2. Install development dependencies:
```bash
pip install -r requirements/dev.txt
```
3. Install pre-commit hooks:
```bash
pre-commit install
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public methods
- Include tests for new features

## Testing

Run tests:
```bash
pytest tests/
```

Check coverage:
```bash
pytest --cov=src tests/
```

[More contribution guidelines...](./guidelines.md)
