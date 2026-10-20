"""
Regression tests for all verified defects fixed in parsikit.cache during Phase 01.
Each test verifies a specific bug reproduction and resolution.
"""
import unittest
from typing import Any
import parsikit
from parsikit.cache import ThreadSafeLRUCache, memoize


class TestCachePhase01Regressions(unittest.TestCase):
    def setUp(self) -> None:
        parsikit.config.reset_defaults()

    def tearDown(self) -> None:
        parsikit.config.reset_defaults()

    def test_regression_maxsize_zero_index_error(self):
        """
        Bug: In the original implementation, ThreadSafeLRUCache(maxsize=0) raised:
             IndexError: pop from empty list
             because 'len(self.cache) >= self.maxsize' evaluated to True (0 >= 0)
             when self.keys_order was empty.
        Fix: maxsize=0 is validated and treated as a documented no-storage mode.
        """
        cache = ThreadSafeLRUCache(maxsize=0)
        # Should not raise IndexError
        cache.set(("alpha",), "value1")
        self.assertEqual(len(cache), 0)
        self.assertIsNone(cache.get(("alpha",)))

        # Also verify @memoize(maxsize=0) executes without error
        invocations = 0

        @memoize(maxsize=0)
        def compute_sq(x: int) -> int:
            nonlocal invocations
            invocations += 1
            return x * x

        self.assertEqual(compute_sq(4), 16)
        self.assertEqual(invocations, 1)
        self.assertEqual(compute_sq(4), 16)
        self.assertEqual(invocations, 2)  # Passthrough mode, no storage

    def test_regression_unhashable_argument_type_error(self):
        """
        Bug: In the original implementation, calling a memoized function with unhashable
             arguments (e.g. lists, dicts, sets, nested containers) raised:
             TypeError: unhashable type: 'list' / 'dict' / 'set'
             when attempting to construct or hash the cache key tuple.
        Fix: Bypasses caching for unhashable arguments and executes the original function
             normally without crashing.
        """
        call_count = 0

        @memoize(maxsize=32)
        def aggregate(items: list[int], options: dict[str, Any] | None = None) -> int:
            nonlocal call_count
            call_count += 1
            base = sum(items)
            if options and options.get("bonus"):
                base += options["bonus"]
            return base

        # Positional list: should not raise TypeError
        res1 = aggregate([10, 20, 30])
        self.assertEqual(res1, 60)
        self.assertEqual(call_count, 1)

        # Subsequent call with unhashable arg executes normally
        res2 = aggregate([10, 20, 30])
        self.assertEqual(res2, 60)
        self.assertEqual(call_count, 2)

        # Keyword dict: should not raise TypeError
        res3 = aggregate([1, 2], options={"bonus": 10})
        self.assertEqual(res3, 13)
        self.assertEqual(call_count, 3)

    def test_regression_cached_none_distinction(self):
        """
        Bug: In the original implementation, the cache lookup checked:
             'if cached_val is not None:'
             Because cache misses returned None, any function legitimately returning
             None was treated as a cache miss on every subsequent call, re-executing
             expensive computations every time.
        Fix: Uses an internal sentinel (_MISSING) to distinguish cache misses from cached
             None/False/0 values, guaranteeing cache hit on repeated calls.
        """
        invocations = 0

        @memoize(maxsize=16)
        def resolve_optional(key: str) -> None:
            nonlocal invocations
            invocations += 1
            return None

        # First call: executes function and caches None
        val1 = resolve_optional("missing_record")
        self.assertIsNone(val1)
        self.assertEqual(invocations, 1)

        # Second call: must hit cache and NOT re-execute
        val2 = resolve_optional("missing_record")
        self.assertIsNone(val2)
        self.assertEqual(invocations, 1)

    def test_regression_invalid_capacity_types_and_negative(self):
        """
        Bug: In original implementation, negative capacity raised IndexError on first set(),
             and non-integer maxsize raised TypeError only at set() time instead of validating
             at initialization.
        Fix: ThreadSafeLRUCache and @memoize validate maxsize at initialization:
             - Negative capacity raises ValueError
             - Non-integer or boolean capacity raises TypeError
        """
        with self.assertRaises(ValueError):
            ThreadSafeLRUCache(maxsize=-5)

        with self.assertRaises(ValueError):
            memoize(maxsize=-1)

        for invalid_val in ["500", 2.5, None, True, False]:
            with self.assertRaises(TypeError):
                ThreadSafeLRUCache(maxsize=invalid_val)  # type: ignore
            with self.assertRaises(TypeError):
                memoize(maxsize=invalid_val)  # type: ignore

    def test_regression_rlock_reentrancy(self):
        """
        Bug: The original implementation used threading.Lock instead of threading.RLock,
             risking self-deadlock when a memoized function called itself or triggered
             another cache access on the same thread.
        Fix: threading.RLock allows safe re-entrant cache access.
        """
        call_count = 0

        @memoize(maxsize=64)
        def factorial(n: int) -> int:
            nonlocal call_count
            call_count += 1
            if n <= 1:
                return 1
            return n * factorial(n - 1)

        result = factorial(5)
        self.assertEqual(result, 120)
        self.assertEqual(call_count, 5)

        # Subsequent top-level call is an immediate single cache hit
        result2 = factorial(5)
        self.assertEqual(result2, 120)
        self.assertEqual(call_count, 5)


if __name__ == "__main__":
    unittest.main()
