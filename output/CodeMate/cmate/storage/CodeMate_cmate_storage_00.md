# Project Details

# Table of Contents
- [..\CodeMate\cmate\storage\__init__.py](#-CodeMate-cmate-storage-__init__py)
- [..\CodeMate\cmate\storage\cache_manager.py](#-CodeMate-cmate-storage-cache_managerpy)
- [..\CodeMate\cmate\storage\persistence_manager.py](#-CodeMate-cmate-storage-persistence_managerpy)


# ..\..\CodeMate\cmate\storage\__init__.py
## File: ..\..\CodeMate\cmate\storage\__init__.py

```py
# ..\..\CodeMate\cmate\storage\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\cmate\storage\cache_manager.py
## File: ..\..\CodeMate\cmate\storage\cache_manager.py

```py
# ..\..\CodeMate\cmate\storage\cache_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
from pathlib import Path
import pickle

@dataclass
class CacheItem:
    """Individual cache item"""
    key: str
    data: Any
    created_at: datetime
    expires_at: Optional[datetime]
    metadata: Dict[str, Any] = field(default_factory=dict)
    access_count: int = 0

class CacheManager:
    """
    Manages temporary data caching.
    
    If a cache directory is provided, items are stored persistently using pickle.
    """
    
    def __init__(self, cache_dir: Optional[str] = None, max_size: int = 1000, default_ttl: Optional[int] = None):
        self.cache_dir = Path(cache_dir) if cache_dir else Path("temp/cache")
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache: Dict[str, CacheItem] = {}
        self.persistent: bool = cache_dir is not None
        self._initialize_cache()

    def _initialize_cache(self) -> None:
        """Initialize the cache system and load persistent items if needed"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if self.persistent:
            self._load_persistent_cache()

    def _load_persistent_cache(self) -> None:
        """Load persistent cache items from disk"""
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                with open(cache_file, 'rb') as f:
                    item = pickle.load(f)
                    if not self._is_expired(item):
                        self.cache[item.key] = item
            except Exception as e:
                print(f"Error loading cache item {cache_file}: {str(e)}")

    def _is_expired(self, item: CacheItem) -> bool:
        """Check if a cache item is expired"""
        return item.expires_at is not None and datetime.now() > item.expires_at

    def get(self, key: str, default: Any = None) -> Any:
        """Get an item from the cache"""
        item = self.cache.get(key)
        if not item:
            return default
        if self._is_expired(item):
            self.delete(key)
            return default
        item.access_count += 1
        if self.persistent:
            self._save_item(item)
        return item.data

    def set(self, key: str, data: Any, ttl: Optional[int] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Set a cache item"""
        if len(self.cache) >= self.max_size:
            self._cleanup()
        ttl_value = ttl if ttl is not None else self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl_value) if ttl_value else None
        item = CacheItem(
            key=key,
            data=data,
            created_at=datetime.now(),
            expires_at=expires_at,
            metadata=metadata or {}
        )
        self.cache[key] = item
        if self.persistent:
            self._save_item(item)

    def delete(self, key: str) -> bool:
        """Delete a cache item"""
        if key in self.cache:
            del self.cache[key]
            cache_file = self.cache_dir / f"{key}.cache"
            if cache_file.exists():
                cache_file.unlink()
            return True
        return False

    def clear(self) -> None:
        """Clear all cache items"""
        self.cache.clear()
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()

    def _cleanup(self) -> None:
        """Clean up expired and least-used items"""
        # Remove expired items first
        expired_keys = [key for key, item in self.cache.items() if self._is_expired(item)]
        for key in expired_keys:
            self.delete(key)
        # If still over limit, remove least-accessed items
        while len(self.cache) >= self.max_size:
            sorted_items = sorted(self.cache.items(), key=lambda x: (x[1].access_count, -x[1].created_at.timestamp()))
            if not sorted_items:
                break
            key_to_remove, _ = sorted_items[0]
            self.delete(key_to_remove)

    def _save_item(self, item: CacheItem) -> None:
        """Save a cache item to disk"""
        try:
            cache_file = self.cache_dir / f"{item.key}.cache"
            with open(cache_file, 'wb') as f:
                pickle.dump(item, f)
        except Exception as e:
            print(f"Error saving cache item {item.key}: {str(e)}")

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the cache"""
        total_items = len(self.cache)
        expired_items = len([item for item in self.cache.values() if self._is_expired(item)])
        total_access = sum(item.access_count for item in self.cache.values())
        average_access = total_access / total_items if total_items else 0
        memory_usage = sum(len(pickle.dumps(item)) for item in self.cache.values())
        hits_by_key = {key: item.access_count for key, item in self.cache.items()}
        return {
            "total_items": total_items,
            "expired_items": expired_items,
            "total_access_count": total_access,
            "average_access_count": average_access,
            "cached_keys": list(self.cache.keys()),
            "memory_usage": memory_usage,
            "hits_by_key": hits_by_key,
            "persistent": self.persistent,
            "cache_usage_percent": (total_items / self.max_size) * 100
        }

    def touch(self, key: str) -> bool:
        """Update the access time (via access count) for a cache item"""
        if key in self.cache:
            item = self.cache[key]
            item.access_count += 1
            if self.persistent:
                self._save_item(item)
            return True
        return False

    def get_metadata(self, key: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a cache item"""
        item = self.cache.get(key)
        return item.metadata if item else None

    def update_metadata(self, key: str, metadata: Dict[str, Any]) -> bool:
        """Update metadata for a cache item"""
        if key in self.cache:
            item = self.cache[key]
            item.metadata.update(metadata)
            if self.persistent:
                self._save_item(item)
            return True
        return False

    def get_expired_items(self) -> List[str]:
        """Get a list of keys that are expired"""
        return [key for key, item in self.cache.items() if self._is_expired(item)]

    def cleanup_expired(self) -> int:
        """Clean up expired items and return the count removed"""
        expired = self.get_expired_items()
        for key in expired:
            self.delete(key)
        return len(expired)

    def exists(self, key: str) -> bool:
        """Check if a key exists in the cache"""
        return key in self.cache

    def set_many(self, items: Dict[str, Any], ttl: Optional[int] = None) -> None:
        """Set multiple cache items at once"""
        for key, data in items.items():
            self.set(key, data, ttl)

    def get_many(self, keys: List[str], default: Any = None) -> Dict[str, Any]:
        """Get multiple cache items at once"""
        return {key: self.get(key, default) for key in keys}

```

---

# ..\..\CodeMate\cmate\storage\persistence_manager.py
## File: ..\..\CodeMate\cmate\storage\persistence_manager.py

```py
# ..\..\CodeMate\cmate\storage\persistence_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
import pickle
from pathlib import Path
import shutil
import zlib
from uuid import UUID, uuid4

@dataclass
class StorageConfig:
    """
    Configuration for persistent storage.
    For this merged version the default format is 'pickle'.
    """
    storage_path: Path
    format: str = "pickle"  # Currently only 'pickle' is supported.
    compression: bool = False
    backup_enabled: bool = True
    max_backups: int = 5

@dataclass
class StorageItem:
    """Individual storage item"""
    id: UUID
    key: str
    data: Any
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    compressed: bool = False

class PersistenceManager:
    """Manages persistent data storage with optional compression and backup"""
    
    def __init__(self, config: Optional[StorageConfig] = None, storage_path: Optional[str] = None, compression: bool = False):
        if config:
            self.config = config
        else:
            path = Path(storage_path) if storage_path else Path("storage")
            self.config = StorageConfig(storage_path=path, compression=compression)
        self.storage_path = self.config.storage_path
        self.compression = self.config.compression
        self.items: Dict[UUID, StorageItem] = {}
        self.indices: Dict[str, UUID] = {}
        self._initialize_storage()
        
    def _initialize_storage(self) -> None:
        """Initialize the storage system and load existing data"""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._load_existing_data()
        
    def _load_existing_data(self) -> None:
        """Load existing data and indices from storage"""
        index_file = self.storage_path / "index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r') as f:
                    index_data = json.load(f)
                    self.indices = {k: UUID(v) for k, v in index_data.items()}
            except Exception as e:
                print(f"Error loading index file: {str(e)}")
        for item_file in self.storage_path.glob("item_*.dat"):
            try:
                with open(item_file, 'rb') as f:
                    item = pickle.load(f)
                    if isinstance(item, StorageItem):
                        self.items[item.id] = item
            except Exception as e:
                print(f"Error loading item {item_file}: {str(e)}")
                
    async def store(self, key: str, data: Any, metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """
        Store data persistently under the given key.
        If the key already exists, the data is updated.
        """
        if key in self.indices:
            return await self.update(key, data, metadata)
        item_id = uuid4()
        now = datetime.now()
        stored_data = self._compress_data(data) if self.compression else data
        item = StorageItem(
            id=item_id,
            key=key,
            data=stored_data,
            created_at=now,
            updated_at=now,
            metadata=metadata or {},
            compressed=self.compression
        )
        self.items[item_id] = item
        self.indices[key] = item_id
        await self._save_item(item)
        await self._save_index()
        if self.config.backup_enabled:
            self.create_backup()
        return item_id

    async def retrieve(self, key: str) -> Any:
        """Retrieve stored data by key"""
        item_id = self.indices.get(key)
        if not item_id:
            raise KeyError(f"Key not found: {key}")
        item = self.items[item_id]
        return self._decompress_data(item.data) if item.compressed else item.data

    async def update(self, key: str, data: Any, metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Update stored data for the given key"""
        item_id = self.indices.get(key)
        if not item_id:
            raise KeyError(f"Key not found: {key}")
        item = self.items[item_id]
        item.data = self._compress_data(data) if self.compression else data
        item.updated_at = datetime.now()
        if metadata:
            item.metadata.update(metadata)
        await self._save_item(item)
        return item_id

    async def delete(self, key: str) -> None:
        """Delete stored data by key"""
        item_id = self.indices.pop(key, None)
        if item_id:
            self.items.pop(item_id, None)
            item_file = self.storage_path / f"item_{item_id}.dat"
            if item_file.exists():
                item_file.unlink()
            await self._save_index()

    def _compress_data(self, data: Any) -> bytes:
        """Compress data using pickle and zlib"""
        pickled = pickle.dumps(data)
        return zlib.compress(pickled)

    def _decompress_data(self, data: bytes) -> Any:
        """Decompress data"""
        try:
            decompressed = zlib.decompress(data)
            return pickle.loads(decompressed)
        except Exception as e:
            print(f"Decompression error: {str(e)}")
            return data

    async def _save_item(self, item: StorageItem) -> None:
        """Save a storage item to disk"""
        item_file = self.storage_path / f"item_{item.id}.dat"
        try:
            with open(item_file, 'wb') as f:
                pickle.dump(item, f)
        except Exception as e:
            print(f"Error saving item {item.id}: {str(e)}")

    async def _save_index(self) -> None:
        """Save the index mapping to disk"""
        index_file = self.storage_path / "index.json"
        try:
            with open(index_file, 'w') as f:
                json.dump({k: str(v) for k, v in self.indices.items()}, f)
        except Exception as e:
            print(f"Error saving index: {str(e)}")

    def create_backup(self) -> Path:
        """Create a backup of the storage directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.storage_path.parent / f"storage_backup_{timestamp}"
        try:
            shutil.copytree(self.storage_path, backup_path)
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
        # Remove old backups if necessary
        backups = sorted(self.storage_path.parent.glob("storage_backup_*"))
        while len(backups) > self.config.max_backups:
            old_backup = backups.pop(0)
            shutil.rmtree(old_backup)
        return backup_path

    def restore_backup(self, backup_path: Union[str, Path]) -> None:
        """Restore storage from a backup"""
        backup_path = Path(backup_path)
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")
        # Clear current storage and copy backup
        if self.storage_path.exists():
            shutil.rmtree(self.storage_path)
        shutil.copytree(backup_path, self.storage_path)
        # Reload data into memory
        self.items.clear()
        self.indices.clear()
        self._load_existing_data()

class StorageError(Exception):
    """Custom exception for storage-related errors"""
    pass

```

---

