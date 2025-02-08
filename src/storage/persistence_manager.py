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
