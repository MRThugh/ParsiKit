"""
parsikit.cache
~~~~~~~~~~~~~~
Thread-safe, high-performance caching infrastructure for expensive computations.
"""

from __future__ import annotations
import threading
from collections import OrderedDict
from functools import wraps
from typing import Callable, Any, TypeVar, NamedTuple

_T = TypeVar("_T")

# Internal sentinel to distinguish a missing cache entry from a cached None/False/etc.
_MISSING = object()


class CacheInfo(NamedTuple):
    """Snapshot of cache performance statistics and capacity."""
    hits: int
    misses: int
    maxsize: int
    currsize: int


class ThreadSafeLRUCache:
    """A lightweight, thread-safe LRU (Least Recently Used) cache.
    
    Guarded by a re-entrant lock (threading.RLock) to provide thread-safety
    and prevent deadlocks during re-entrant or recursive calls.
    
    Attributes:
        maxsize: Maximum number of entries the cache will retain.
        hits: Number of successful cache hits.
        misses: Number of cache lookups that missed.
    """
    def __init__(self, maxsize: int = 1024) -> None:
        if not isinstance(maxsize, int) or isinstance(maxsize, bool):
            raise TypeError(f"maxsize must be an integer, got {type(maxsize).__name__}")
        if maxsize < 0:
            raise ValueError(f"maxsize must be non-negative (>= 0), got {maxsize}")

        self.maxsize = maxsize
        self.cache: OrderedDict[Any, Any] = OrderedDict()
        self.lock = threading.RLock()
        self.hits: int = 0
        self.misses: int = 0

    @property
    def keys_order(self) -> list[Any]:
        """List of keys in order from oldest (LRU) to newest (MRU)."""
        with self.lock:
            return list(self.cache.keys())

    def get(self, key: Any, default: Any = None) -> Any:
        """Retrieve a value from the cache.
        
        If found, marks the key as most recently used and increments hits.
        If not found, increments misses and returns the default value.
        """
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
                self.hits += 1
                return self.cache[key]
            self.misses += 1
            return default

    def set(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair in the cache.
        
        If maxsize is 0, operates in no-storage mode (no entry is retained).
        If the key already exists, updates its value and marks it as MRU without eviction.
        If capacity is reached, evicts the oldest entry (LRU) before insertion.
        """
        with self.lock:
            if self.maxsize == 0:
                return
            if key in self.cache:
                self.cache.move_to_end(key)
            else:
                while len(self.cache) >= self.maxsize:
                    self.cache.popitem(last=False)
            self.cache[key] = value

    def clear(self) -> None:
        """Evict all entries and reset hit/miss statistics."""
        with self.lock:
            self.cache.clear()
            self.hits = 0
            self.misses = 0

    def pop(self, key: Any, default: Any = _MISSING) -> Any:
        """Remove and return an item from the cache.
        
        If key is not found, default is returned if given, otherwise KeyError is raised.
        """
        with self.lock:
            if key in self.cache:
                return self.cache.pop(key)
            if default is not _MISSING:
                return default
            raise KeyError(key)

    def __contains__(self, key: Any) -> bool:
        """Check whether a key exists in the cache."""
        with self.lock:
            return key in self.cache

    def __len__(self) -> int:
        """Return the current number of cached items."""
        with self.lock:
            return len(self.cache)


def _make_cache_key(args: tuple[Any, ...], kwargs: dict[str, Any]) -> tuple[Any, ...] | None:
    """Build a deterministic cache key from positional and keyword arguments.
    
    Keyword arguments are sorted by parameter name to ensure consistent keys
    regardless of call-site argument order.
    
    Returns None if any argument is unhashable or cannot be safely hashed.
    """
    try:
        kw_items = tuple(sorted(kwargs.items(), key=lambda item: item[0]))
        key = (args, kw_items)
        hash(key)
        return key
    except TypeError:
        return None


def memoize(maxsize: int = 1024) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
    """Decorator to cache function results in a thread-safe manner.
    
    Features:
        - Thread safety: Protected by internal re-entrant locking (threading.RLock).
        - Dynamic config: Bypasses cache when `parsikit.config.enable_cache` is False.
        - Zero capacity: Operates in transparent pass-through mode when maxsize=0.
        - Unhashable fallback: Gracefully executes without caching if arguments are unhashable.
        - Sentinel hit check: Accurately caches and returns None and falsey results.
        - Object identity: Returns cached objects by reference without unintended deep copies.
        - Introspection: Exposes `.cache`, `.cache_clear()`, and `.cache_info()` on the wrapper.
    """
    if not isinstance(maxsize, int) or isinstance(maxsize, bool):
        raise TypeError(f"maxsize must be an integer, got {type(maxsize).__name__}")
    if maxsize < 0:
        raise ValueError(f"maxsize must be non-negative (>= 0), got {maxsize}")

    cache_instance = ThreadSafeLRUCache(maxsize=maxsize)
    
    def decorator(func: Callable[..., _T]) -> Callable[..., _T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> _T:
            from parsikit.config import config
            if not config.enable_cache or maxsize == 0:
                return func(*args, **kwargs)
                
            key = _make_cache_key(args, kwargs)
            if key is None:
                # Unhashable argument fallback: bypass cache and execute directly
                return func(*args, **kwargs)
                
            cached_val = cache_instance.get(key, default=_MISSING)
            if cached_val is not _MISSING:
                return cached_val
                
            result = func(*args, **kwargs)
            cache_instance.set(key, result)
            return result

        wrapper.cache = cache_instance  # type: ignore
        wrapper.cache_clear = cache_instance.clear  # type: ignore
        wrapper.cache_info = lambda: CacheInfo(  # type: ignore
            hits=cache_instance.hits,
            misses=cache_instance.misses,
            maxsize=cache_instance.maxsize,
            currsize=len(cache_instance),
        )
        return wrapper  # type: ignore
    return decorator


__all__ = ["ThreadSafeLRUCache", "memoize", "CacheInfo"]