"""Unit tests for parsikit.cache module."""
import unittest
from parsikit.cache import ThreadSafeLRUCache, memoize
import parsikit


class TestCacheModule(unittest.TestCase):
    def test_lru_cache_operations(self):
        cache = ThreadSafeLRUCache(maxsize=3)
        cache.set(("a",), 1)
        cache.set(("b",), 2)
        cache.set(("c",), 3)

        self.assertEqual(cache.get(("a",)), 1)
        self.assertEqual(cache.get(("b",)), 2)

        # Adding 4th element should evict oldest (c)
        cache.set(("d",), 4)
        self.assertIsNone(cache.get(("c",)))
        self.assertEqual(cache.get(("d",)), 4)

        cache.clear()
        self.assertIsNone(cache.get(("a",)))

    def test_memoize_decorator(self):
        call_count = 0

        @memoize(maxsize=10)
        def expensive(n: int) -> int:
            nonlocal call_count
            call_count += 1
            return n * 2

        self.assertEqual(expensive(5), 10)
        self.assertEqual(call_count, 1)

        # Cached call
        self.assertEqual(expensive(5), 10)
        self.assertEqual(call_count, 1)

        # Different argument
        self.assertEqual(expensive(6), 12)
        self.assertEqual(call_count, 2)


if __name__ == "__main__":
    unittest.main()
