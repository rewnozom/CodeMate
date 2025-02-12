import unittest
import asyncio
from cmate.storage.persistence_manager import PersistenceManager
from pathlib import Path

class TestPersistenceManager(unittest.TestCase):
    def setUp(self):
        self.storage_path = "temp/test_storage"
        self.pm = PersistenceManager(storage_path=self.storage_path, compression=False)
    
    def test_store_and_retrieve(self):
        async def run_test():
            key = "persistent_test"
            data = {"value": 123}
            item_id = await self.pm.store(key, data)
            self.assertIsNotNone(item_id)
            retrieved = await self.pm.retrieve(key)
            self.assertEqual(retrieved, data)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()
