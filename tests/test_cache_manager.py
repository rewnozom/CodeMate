import unittest
from cmate.storage.cache_manager import CacheManager

class TestCacheManager(unittest.TestCase):
    def setUp(self):
        self.cache = CacheManager(cache_dir="temp/test_cache", default_ttl=2)
    
    def test_set_get_delete(self):
        self.cache.set("test_key", "test_data")
        data = self.cache.get("test_key")
        self.assertEqual(data, "test_data")
        deleted = self.cache.delete("test_key")
        self.assertTrue(deleted)
        data_after = self.cache.get("test_key")
        self.assertIsNone(data_after)
    
    def test_cleanup_expired(self):
        self.cache.set("temp_key", "temp", ttl=1)
        import time; time.sleep(2)
        removed = self.cache.cleanup_expired()
        self.assertGreaterEqual(removed, 1)

if __name__ == '__main__':
    unittest.main()
