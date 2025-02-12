import unittest
from cmate.core.memory_manager import MemoryManager, MemoryType
from uuid import UUID

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.memory_manager = MemoryManager()
    
    def test_store_and_retrieve(self):
        key = "test_item"
        content = "This is a test."
        memory_id = self.memory_manager.store(content, MemoryType.SHORT_TERM)
        self.assertIsInstance(memory_id, UUID)
        retrieved = self.memory_manager.retrieve(memory_id)
        self.assertEqual(retrieved, content)
    
    def test_cleanup_expired(self):
        key = "cleanup_test"
        memory_id = self.memory_manager.store("temporary", MemoryType.SHORT_TERM, ttl=1)
        import time; time.sleep(2)
        count = self.memory_manager.cleanup()
        self.assertGreaterEqual(count, 1)

if __name__ == '__main__':
    unittest.main()
