# docs/utils/README.md
# Utilities Documentation

## Overview
Utility modules provide common functionality across the system.

### Components
- logger.py
- error_handler.py
- config.py
- token_counter.py
- prompt_templates.py
- system_metrics.py

## Usage Examples

### Logger
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Processing started")
```

### ErrorHandler
```python
from utils.error_handler import ErrorHandler

handler = ErrorHandler()
handler.handle_error(exception, severity="error")
```

[More utility details...](./utils.md)
