# Cache API (`parsikit.cache`)

High-performance, thread-safe caching infrastructure for expensive mathematical, linguistic, and calendar computations.

---

## Overview

The `parsikit.cache` module provides in-memory thread-safe LRU-like caching mechanisms utilized internally by compute-intensive functions such as `parsikit.number.number_to_words`.

> **Note on API Stability**: While `ThreadSafeLRUCache` and `@memoize` are fully functional and tested, `parsikit.cache` serves primarily as an internal infrastructure module for ParsiKit. Its public surface is stable for standard caching tasks, but future major versions may introduce specialized cache backends.

---

## Classes

### `ThreadSafeLRUCache`

```python
class ThreadSafeLRUCache:
    def __init__(self, maxsize: int = 1024) -> None
```

A lightweight in-memory LRU cache guarded by `threading.RLock` to provide safe concurrent access and re-entrant recursion without deadlocks.

#### Capacity Rules
- `maxsize` must be an integer (`int`). Non-integer types raise `TypeError`.
- `maxsize >= 0`. Negative integers raise `ValueError`.
- `maxsize == 0`: Operates in **no-storage mode** where entries are not stored and lookups return the default value.

#### Methods & Properties

- **`get(key: Any, default: Any = None) -> Any`**:
  Retrieves a value from the cache. If found, refreshes the key's position to mark it as most recently used (MRU) and increments hits. Returns `default` on cache miss.
- **`set(key: Any, value: Any) -> None`**:
  Inserts or updates a value. If the key exists, updates its value and marks it as MRU without eviction. When capacity is exceeded, evicts the least recently used (LRU) entry.
- **`clear() -> None`**:
  Evicts all entries and resets hit and miss counters.
- **`pop(key: Any, default: Any = ...) -> Any`**:
  Removes and returns an entry from the cache. Raises `KeyError` if key is not found and no default is provided.
- **`keys_order`**:
  Property returning a snapshot list of cached keys ordered from oldest (LRU) to newest (MRU).
- **`__len__()` & `__contains__(key)`**:
  Provides standard dictionary-like container inspection under lock.

---

## Decorators

### `@memoize`

```python
def memoize(maxsize: int = 1024) -> Callable[[Callable[..., _T]], Callable[..., _T]]
```

Decorator that caches function return values using a dedicated `ThreadSafeLRUCache` instance.

#### Features
- **Dynamic Configuration Toggle**: Respects `parsikit.config.enable_cache`. When set to `False`, the wrapper bypasses the cache entirely and calls the underlying function directly.
- **Thread Safety & Reentrancy**: Protected by `threading.RLock`, ensuring safe multi-threaded operation and recursion without deadlocks.
- **Sentinel-Based Cache Misses**: Uses an internal sentinel to distinguish missing entries from cached values of `None`, `False`, `0`, or empty containers.
- **Unhashable Argument Graceful Fallback**: When unhashable arguments (such as `list`, `dict`, `set`, or nested unhashable structures) are supplied, caching is gracefully bypassed and the target function executes normally without raising `TypeError`.
- **Object Identity**: Returns cached objects by reference (`res1 is res2`). Callers requiring isolated mutable results should copy them explicitly.
- **Inspection & Control**: The wrapped function exposes:
  - `func.cache`: Direct reference to the underlying `ThreadSafeLRUCache`.
  - `func.cache_clear()`: Clears cached entries and resets statistics.
  - `func.cache_info()`: Returns a `CacheInfo(hits, misses, maxsize, currsize)` tuple.

#### Usage Example

```python
import parsikit
from parsikit.cache import memoize

@memoize(maxsize=512)
def compute_complex_tax(base_amount: int, tier: str = "standard") -> int:
    # Expensive financial calculation
    return base_amount * 2

# First call calculates and stores in cache
res1 = compute_complex_tax(1000000, tier="A")

# Subsequent calls with identical arguments hit the cache immediately
res2 = compute_complex_tax(1000000, tier="A")
assert res1 == res2

# Introspect cache statistics
info = compute_complex_tax.cache_info()
print(f"Hits: {info.hits}, Misses: {info.misses}, Size: {info.currsize}")

# Clear cache when needed
compute_complex_tax.cache_clear()

# Disable cache dynamically if needed
parsikit.config.enable_cache = False
res3 = compute_complex_tax(1000000, tier="A")  # executes underlying function
parsikit.config.reset_defaults()
```

---

## Edge Cases & Limitations

1. **Unhashable Arguments**: Functions called with unhashable arguments will execute normally without raising `TypeError`, bypassing the cache for that specific invocation.
2. **Mutable Return Values**: Because objects are cached by reference, mutating a returned mutable object (e.g. `list.append()`) alters the cached instance.
3. **Process Isolation**: The cache is purely in-memory within the Python process. Multi-process architectures (e.g. `gunicorn -w 4`) maintain independent caches per worker process.
