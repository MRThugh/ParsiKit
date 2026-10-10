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

A lightweight in-memory LRU-like cache guarded by a `threading.Lock`.

#### Methods

- **`get(key: tuple[Any, ...]) -> Any | None`**:
  Retrieves a value from the cache. If found, refreshes the key's position to mark it as most recently used. Returns `None` on cache miss.
- **`set(key: tuple[Any, ...], value: Any) -> None`**:
  Inserts or updates a value. When cache size exceeds `maxsize`, evicts the oldest unused key.
- **`clear() -> None`**:
  Evicts all entries and resets the key ordering list.

---

## Decorators

### `@memoize`

```python
def memoize(maxsize: int = 1024) -> Callable[[Callable[..., _T]], Callable[..., _T]]
```

Decorator that caches function return values using a dedicated `ThreadSafeLRUCache` instance.

#### Features
- **Dynamic Configuration Toggle**: Respects `parsikit.config.enable_cache`. When set to `False`, the wrapper bypasses the cache entirely and calls the underlying function directly.
- **Thread Safety**: Safe for concurrent threads (e.g. FastAPI / Flask / Django worker threads).
- **Composite Key Generation**: Builds cache keys from positional arguments and sorted keyword argument tuples.

#### Usage Example

```python
import parsikit
from parsikit.cache import memoize

@memoize(maxsize=512)
def compute_complex_tax(base_amount: int, tier: str) -> int:
    # Expensive financial calculation
    return base_amount * 2

# First call calculates and stores in cache
res1 = compute_complex_tax(1000000, tier="A")

# Subsequent calls with identical arguments hit the cache immediately
res2 = compute_complex_tax(1000000, tier="A")

# Disable cache dynamically if needed
parsikit.config.enable_cache = False
res3 = compute_complex_tax(1000000, tier="A")  # executes underlying function
parsikit.config.reset_defaults()
```

---

## Edge Cases & Limitations

1. **Hashable Arguments**: Arguments to `@memoize` decorated functions must be hashable. Dictionaries or mutable lists passed as arguments will raise `TypeError` when constructing cache keys.
2. **Process Isolation**: The cache is purely in-memory within the Python process. Multi-process architectures (e.g. `gunicorn -w 4`) maintain independent caches per worker process.
