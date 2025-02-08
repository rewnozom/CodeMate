# docs/storage/README.md
# Storage Services Documentation

## Overview
Storage services handle data persistence and caching.

### Components
- temporary_storage.py
- persistence_manager.py
- cache_manager.py

## Usage Examples

### CacheManager
```python
from storage.cache_manager import CacheManager

cache = CacheManager()
cache.set("key", "value", ttl=3600)
value = cache.get("key")
```

### PersistenceManager
```python
from storage.persistence_manager import PersistenceManager

storage = PersistenceManager()
await storage.store("key", {"data": "value"})
```

[More storage details...](./storage.md)
