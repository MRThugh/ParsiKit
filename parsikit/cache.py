"""
parsikit.cache
~~~~~~~~~~~~~~
Thread-safe, high-performance caching infrastructure for expensive computations.
"""

from __future__ import annotations
import threading
from functools import wraps
from typing import Callable, Any, TypeVar

_T = TypeVar("_T")


class ThreadSafeLRUCache:
    """A simple, lightweight thread-safe LRU-like cache."""
    def __init__(self, maxsize: int = 1024) -> None:
        self.maxsize = maxsize
        self.cache: dict[tuple[Any, ...], Any] = {}
        self.lock = threading.Lock()
        self.keys_order: list[tuple[Any, ...]] = []

    def get(self, key: tuple[Any, ...]) -> Any | None:
        with self.lock:
            if key in self.cache:
                self.keys_order.remove(key)
                self.keys_order.append(key)
                return self.cache[key]
            return None

    def set(self, key: tuple[Any, ...], value: Any) -> None:
        with self.lock:
            if key in self.cache:
                self.keys_order.remove(key)
            elif len(self.cache) >= self.maxsize:
                oldest = self.keys_order.pop(0)
                self.cache.pop(oldest, None)
            self.cache[key] = value
            self.keys_order.append(key)

    def clear(self) -> None:
        with self.lock:
            self.cache.clear()
            self.keys_order.clear()


def memoize(maxsize: int = 1024) -> Callable[[Callable[..., _T]], Callable[..., _T]]:
    """Decorator to cache function results in a thread-safe manner."""
    cache_instance = ThreadSafeLRUCache(maxsize=maxsize)
    
    def decorator(func: Callable[..., _T]) -> Callable[..., _T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> _T:
            from parsikit.config import config
            if not config.enable_cache:
                return func(*args, **kwargs)
                
            key = (args, tuple(sorted(kwargs.items())))
            cached_val = cache_instance.get(key)
            if cached_val is not None:
                return cached_val
                
            result = func(*args, **kwargs)
            cache_instance.set(key, result)
            return result
        return wrapper  # type: ignore
    return decorator