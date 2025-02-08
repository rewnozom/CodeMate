# docs/user_guide/usage.md
# Detailed Usage Guide

## Request Types

### Analysis Request
```python
request = {
    "type": "analyze",
    "data": {
        "path": "path/to/file.py",
        "depth": "simple"  # or "detailed"
    }
}
```

### Modification Request
```python
request = {
    "type": "modify",
    "data": {
        "path": "path/to/file.py",
        "changes": "description of changes",
        "auto_test": True
    }
}
```

[More request types...](./requests.md)
