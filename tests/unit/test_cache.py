"""Unit tests for parsikit.cache module."""
import threading
import unittest
from typing import Any
import parsikit
from parsikit.cache import ThreadSafeLRUCache, memoize, CacheInfo


class TestCacheModule(unittest.TestCase):
    def setUp(self) -> None:
        parsikit.config.reset_defaults()

    def tearDown(self) -> None:
        parsikit.config.reset_defaults()

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

    def test_cache_none_and_falsey_values(self):
        """Verify that None and all falsey values are properly cached on subsequent calls."""
        none_calls = 0
        false_calls = 0
        zero_calls = 0
        empty_str_calls = 0
        empty_list_calls = 0

        @memoize(maxsize=16)
        def return_none(x: int) -> None:
            nonlocal none_calls
            none_calls += 1
            return None

        @memoize(maxsize=16)
        def return_false(x: int) -> bool:
            nonlocal false_calls
            false_calls += 1
            return False

        @memoize(maxsize=16)
        def return_zero(x: int) -> int:
            nonlocal zero_calls
            zero_calls += 1
            return 0

        @memoize(maxsize=16)
        def return_empty_str(x: int) -> str:
            nonlocal empty_str_calls
            empty_str_calls += 1
            return ""

        @memoize(maxsize=16)
        def return_empty_list(x: int) -> list:
            nonlocal empty_list_calls
            empty_list_calls += 1
            return []

        # First calls (misses)
        self.assertIsNone(return_none(1))
        self.assertEqual(none_calls, 1)
        self.assertFalse(return_false(1))
        self.assertEqual(false_calls, 1)
        self.assertEqual(return_zero(1), 0)
        self.assertEqual(zero_calls, 1)
        self.assertEqual(return_empty_str(1), "")
        self.assertEqual(empty_str_calls, 1)
        self.assertEqual(return_empty_list(1), [])
        self.assertEqual(empty_list_calls, 1)

        # Subsequent calls must hit the cache and NOT increment invocation counts
        self.assertIsNone(return_none(1))
        self.assertEqual(none_calls, 1)

        self.assertFalse(return_false(1))
        self.assertEqual(false_calls, 1)

        self.assertEqual(return_zero(1), 0)
        self.assertEqual(zero_calls, 1)

        self.assertEqual(return_empty_str(1), "")
        self.assertEqual(empty_str_calls, 1)

        self.assertEqual(return_empty_list(1), [])
        self.assertEqual(empty_list_calls, 1)

        # ThreadSafeLRUCache direct sentinel distinguishing test
        cache = ThreadSafeLRUCache(maxsize=5)
        sentinel = object()
        cache.set(("key_with_none",), None)
        self.assertIsNone(cache.get(("key_with_none",), default=sentinel))
        self.assertIs(cache.get(("non_existent_key",), default=sentinel), sentinel)
        self.assertIn(("key_with_none",), cache)
        self.assertNotIn(("non_existent_key",), cache)

    def test_unhashable_arguments_fallback(self):
        """Verify unhashable positional/keyword arguments cleanly bypass caching without TypeError."""
        call_count = 0

        @memoize(maxsize=16)
        def process_data(data: Any, flag: bool = True, extra: Any = None) -> int:
            nonlocal call_count
            call_count += 1
            if isinstance(data, (list, dict, set)):
                return len(data)
            return 1

        # Unhashable positional argument (list)
        result1 = process_data([1, 2, 3])
        self.assertEqual(result1, 3)
        self.assertEqual(call_count, 1)
        # Second call executes normally without crashing
        result2 = process_data([1, 2, 3])
        self.assertEqual(result2, 3)
        self.assertEqual(call_count, 2)  # Bypassed cache, executed directly

        # Unhashable keyword argument (dict)
        result3 = process_data(10, extra={"a": 1, "b": 2})
        self.assertEqual(result3, 1)
        self.assertEqual(call_count, 3)

        # Unhashable positional set
        result4 = process_data({1, 2, 3, 4})
        self.assertEqual(result4, 4)
        self.assertEqual(call_count, 4)

        # Deeply nested unhashable container
        result5 = process_data([[1, 2], {"inner": [3, 4]}])
        self.assertEqual(result5, 2)
        self.assertEqual(call_count, 5)

        # Hashable argument still caches normally
        call_count_hashable = 0

        @memoize(maxsize=16)
        def hashable_func(x: tuple[int, ...]) -> int:
            nonlocal call_count_hashable
            call_count_hashable += 1
            return sum(x)

        self.assertEqual(hashable_func((1, 2, 3)), 6)
        self.assertEqual(call_count_hashable, 1)
        self.assertEqual(hashable_func((1, 2, 3)), 6)
        self.assertEqual(call_count_hashable, 1)  # Hit cache

    def test_keyword_argument_ordering(self):
        """Verify that keyword arguments are order-independent for cache hits."""
        call_count = 0

        @memoize(maxsize=16)
        def compute(a: int, b: int, c: str) -> str:
            nonlocal call_count
            call_count += 1
            return f"{a}-{b}-{c}"

        res1 = compute(a=1, b=2, c="test")
        self.assertEqual(res1, "1-2-test")
        self.assertEqual(call_count, 1)

        # Different kwarg order at call-site must be a cache hit
        res2 = compute(c="test", a=1, b=2)
        self.assertEqual(res2, "1-2-test")
        self.assertEqual(call_count, 1)

        res3 = compute(b=2, c="test", a=1)
        self.assertEqual(res3, "1-2-test")
        self.assertEqual(call_count, 1)

    def test_capacity_validation(self):
        """Verify strict capacity validation on initialization for both cache and decorator."""
        # Negative capacity must raise ValueError
        with self.assertRaises(ValueError):
            ThreadSafeLRUCache(maxsize=-1)
        with self.assertRaises(ValueError):
            memoize(maxsize=-1)
        with self.assertRaises(ValueError):
            ThreadSafeLRUCache(maxsize=-100)

        # Non-integer capacity must raise TypeError
        for invalid in ["10", 3.14, None, True, False, [10]]:
            with self.assertRaises(TypeError):
                ThreadSafeLRUCache(maxsize=invalid)  # type: ignore
            with self.assertRaises(TypeError):
                memoize(maxsize=invalid)  # type: ignore

    def test_zero_capacity_no_storage_mode(self):
        """Verify maxsize=0 acts as a documented no-storage mode without index errors."""
        cache = ThreadSafeLRUCache(maxsize=0)
        self.assertEqual(len(cache), 0)
        self.assertEqual(cache.maxsize, 0)

        # Insertion must succeed gracefully without raising IndexError
        cache.set(("a",), 1)
        self.assertEqual(len(cache), 0)
        self.assertIsNone(cache.get(("a",)))
        self.assertEqual(cache.keys_order, [])

        # Memoize with maxsize=0 must pass-through transparently
        calls = 0

        @memoize(maxsize=0)
        def passthrough(n: int) -> int:
            nonlocal calls
            calls += 1
            return n * 10

        self.assertEqual(passthrough(5), 50)
        self.assertEqual(calls, 1)
        self.assertEqual(passthrough(5), 50)
        self.assertEqual(calls, 2)
        self.assertEqual(len(passthrough.cache), 0)

    def test_capacity_enforcement_and_eviction_order(self):
        """Verify strict LRU eviction ordering and capacity enforcement."""
        cache = ThreadSafeLRUCache(maxsize=3)
        cache.set(("k1",), 10)
        cache.set(("k2",), 20)
        cache.set(("k3",), 30)
        self.assertEqual(len(cache), 3)
        self.assertEqual(cache.keys_order, [("k1",), ("k2",), ("k3",)])

        # Access k1: moves k1 to most recently used (end)
        self.assertEqual(cache.get(("k1",)), 10)
        self.assertEqual(cache.keys_order, [("k2",), ("k3",), ("k1",)])

        # Insert k4: should evict k2 (oldest LRU entry)
        cache.set(("k4",), 40)
        self.assertEqual(len(cache), 3)
        self.assertNotIn(("k2",), cache)
        self.assertIn(("k3",), cache)
        self.assertIn(("k1",), cache)
        self.assertIn(("k4",), cache)
        self.assertEqual(cache.keys_order, [("k3",), ("k1",), ("k4",)])

        # Updating existing k3 must update value and move to MRU without evicting
        cache.set(("k3",), 99)
        self.assertEqual(len(cache), 3)
        self.assertEqual(cache.get(("k3",)), 99)
        self.assertEqual(cache.keys_order, [("k1",), ("k4",), ("k3",)])

    def test_mutable_cached_results_and_identity_contract(self):
        """Document and verify that memoized calls return the exact cached object reference."""
        call_count = 0

        @memoize(maxsize=5)
        def generate_list(tag: str) -> list[str]:
            nonlocal call_count
            call_count += 1
            return [tag, "initial"]

        res1 = generate_list("item")
        res2 = generate_list("item")
        self.assertEqual(call_count, 1)
        self.assertIs(res1, res2)

        # Mutating the returned object modifies the cached instance
        res1.append("mutated")
        res3 = generate_list("item")
        self.assertEqual(res3, ["item", "initial", "mutated"])
        self.assertIs(res1, res3)

    def test_exceptions_not_cached(self):
        """Verify that exceptions raised by the wrapped function are not cached."""
        call_count = 0
        should_fail = True

        @memoize(maxsize=5)
        def flaky(x: int) -> int:
            nonlocal call_count
            call_count += 1
            if should_fail:
                raise ValueError("Calculation failed")
            return x * 10

        # First call raises
        with self.assertRaises(ValueError):
            flaky(5)
        self.assertEqual(call_count, 1)

        # Second call also raises if should_fail is still True
        with self.assertRaises(ValueError):
            flaky(5)
        self.assertEqual(call_count, 2)

        # Third call succeeds once condition resolves; result is now cached
        should_fail = False
        self.assertEqual(flaky(5), 50)
        self.assertEqual(call_count, 3)

        # Fourth call hits cache
        self.assertEqual(flaky(5), 50)
        self.assertEqual(call_count, 3)

    def test_decorator_metadata_and_introspection(self):
        """Verify wraps metadata, .cache, .cache_clear(), and .cache_info()."""
        @memoize(maxsize=64)
        def sample_function(x: int, y: int = 1) -> int:
            """Sample docstring for testing."""
            return x + y

        self.assertEqual(sample_function.__name__, "sample_function")
        self.assertEqual(sample_function.__doc__, "Sample docstring for testing.")
        self.assertTrue(hasattr(sample_function, "__wrapped__"))

        # Test cache_info and cache_clear
        info0 = sample_function.cache_info()
        self.assertEqual(info0, CacheInfo(hits=0, misses=0, maxsize=64, currsize=0))

        sample_function(10, y=2)
        info1 = sample_function.cache_info()
        self.assertEqual(info1.hits, 0)
        self.assertEqual(info1.misses, 1)
        self.assertEqual(info1.currsize, 1)

        sample_function(10, y=2)
        info2 = sample_function.cache_info()
        self.assertEqual(info2.hits, 1)
        self.assertEqual(info2.misses, 1)
        self.assertEqual(info2.currsize, 1)

        sample_function.cache_clear()
        info3 = sample_function.cache_info()
        self.assertEqual(info3.hits, 0)
        self.assertEqual(info3.misses, 0)
        self.assertEqual(info3.currsize, 0)

    def test_recursive_function_and_reentrancy(self):
        """Verify re-entrant calls with threading.RLock compute correctly without deadlock."""
        eval_counts = 0

        @memoize(maxsize=128)
        def fib(n: int) -> int:
            nonlocal eval_counts
            eval_counts += 1
            if n <= 1:
                return n
            return fib(n - 1) + fib(n - 2)

        result = fib(10)
        self.assertEqual(result, 55)
        # With memoization, fib(10) evaluates exactly 11 states (0 through 10)
        self.assertEqual(eval_counts, 11)

    def test_dynamic_enable_cache_toggle(self):
        """Verify parsikit.config.enable_cache toggle dynamically disables/enables caching."""
        calls = 0

        @memoize(maxsize=10)
        def calc(val: int) -> int:
            nonlocal calls
            calls += 1
            return val * 3

        self.assertEqual(calc(5), 15)
        self.assertEqual(calls, 1)
        self.assertEqual(calc(5), 15)
        self.assertEqual(calls, 1)

        # Disable cache via global config
        parsikit.config.enable_cache = False
        self.assertEqual(calc(5), 15)
        self.assertEqual(calls, 2)  # Cache bypassed

        # Re-enable cache
        parsikit.config.enable_cache = True
        self.assertEqual(calc(5), 15)
        self.assertEqual(calls, 2)  # Hit cache again

    def test_multithreaded_concurrent_access(self):
        """Verify thread-safety and capacity invariants under heavy concurrent access."""
        cache = ThreadSafeLRUCache(maxsize=20)
        num_threads = 10
        iterations_per_thread = 100
        barrier = threading.Barrier(num_threads)
        errors: list[Exception] = []

        def worker(thread_id: int) -> None:
            try:
                barrier.wait()
                for i in range(iterations_per_thread):
                    key = (f"key_{i % 50}",)
                    cache.set(key, i)
                    val = cache.get(key)
                    if i % 10 == 0:
                        _ = cache.keys_order
                    if i % 30 == 0:
                        _ = len(cache)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(errors, [])
        self.assertLessEqual(len(cache), 20)

    def test_thread_safe_lru_cache_pop_and_protocol(self):
        """Verify pop, __contains__, __len__, and clear methods on ThreadSafeLRUCache."""
        cache = ThreadSafeLRUCache(maxsize=5)
        cache.set(("x",), 100)
        cache.set(("y",), 200)

        self.assertEqual(len(cache), 2)
        self.assertTrue(("x",) in cache)
        self.assertFalse(("z",) in cache)

        # Pop existing
        val = cache.pop(("x",))
        self.assertEqual(val, 100)
        self.assertEqual(len(cache), 1)
        self.assertFalse(("x",) in cache)

        # Pop non-existent with default
        val_default = cache.pop(("missing",), default=999)
        self.assertEqual(val_default, 999)

        # Pop non-existent without default raises KeyError
        with self.assertRaises(KeyError):
            cache.pop(("missing",))


if __name__ == "__main__":
    unittest.main()
