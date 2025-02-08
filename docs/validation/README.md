# docs/validation/README.md
# Validation Services Documentation

## Overview
Validation services ensure code quality and correctness.

### Components
- test_manager.py
- implementation_validator.py
- frontend_validator.py
- backend_validator.py
- validation_rules.py

## Validation Examples

### TestManager
```python
from validation.test_manager import TestManager

test_manager = TestManager()
result = await test_manager.run_test("test_example.py")
```

### ImplementationValidator
```python
from validation.implementation_validator import ImplementationValidator

validator = ImplementationValidator()
result = await validator.validate_implementation(
    code="def example(): pass",
    language="python"
)
```

[More validation details...](./validation.md)
