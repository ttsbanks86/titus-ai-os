# knowledge_engine/cache.py
# Phase E: Hot Context Cache — context caching for sessions

from __future__ import annotations

import time
import threading
from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any, Optional

from .config import KnowledgeEngineConfig
from .models import CacheEntry


class HotContextCache:
    """
    LRU cache with TTL expiration for hot context.

    Features:
    - Bounded size (configurable max entries)
    - TTL expiration
    - LRU eviction
    - Deterministic refresh
    - Thread-safe operations
    - Hit/miss statistics
    """

    def __init__(self, config: Optional[KnowledgeEngineConfig] = None):
        self.config = config or KnowledgeEngineConfig()
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0
        self._evictions = 0

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.

        Returns None if not found or expired.
        """
        with self._lock:
            entry = self._cache.get(key)
            if entry is None:
                self._misses += 1
                return None

            if entry.is_expired:
                del self._cache[key]
                self._misses += 1
                return None

            # Move to end (most recently used)
            self._cache.move_to_end(key)
            entry.hit_count += 1
            self._hits += 1
            return entry.data

    def set(
        self,
        key: str,
        data: Any,
        ttl_seconds: Optional[int] = None,
    ) -> None:
        """Set a value in the cache."""
        with self._lock:
            # Remove existing entry if present
            if key in self._cache:
                del self._cache[key]

            # Evict if at capacity
            while len(self._cache) >= self.config.cache_max_entries:
                self._cache.popitem(last=False)
                self._evictions += 1

            expires_at = None
            if ttl_seconds is not None:
                expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
            elif self.config.cache_default_ttl_seconds > 0:
                expires_at = datetime.now() + timedelta(
                    seconds=self.config.cache_default_ttl_seconds
                )

            self._cache[key] = CacheEntry(
                key=key,
                data=data,
                created_at=datetime.now(),
                expires_at=expires_at,
            )

    def invalidate(self, key: str) -> bool:
        """Remove a specific key from the cache. Returns True if found."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def invalidate_prefix(self, prefix: str) -> int:
        """Remove all keys starting with prefix. Returns count removed."""
        with self._lock:
            keys_to_remove = [k for k in self._cache if k.startswith(prefix)]
            for key in keys_to_remove:
                del self._cache[key]
            return len(keys_to_remove)

    def clear(self) -> int:
        """Clear the entire cache. Returns count removed."""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count

    def cleanup_expired(self) -> int:
        """Remove all expired entries. Returns count removed."""
        with self._lock:
            now = datetime.now()
            keys_to_remove = [
                k for k, v in self._cache.items()
                if v.expires_at and now > v.expires_at
            ]
            for key in keys_to_remove:
                del self._cache[key]
            return len(keys_to_remove)

    def refresh(self, key: str, data: Any, ttl_seconds: Optional[int] = None) -> None:
        """Force-refresh a cache entry (invalidate + set)."""
        self.invalidate(key)
        self.set(key, data, ttl_seconds)

    @property
    def size(self) -> int:
        """Current number of entries in cache."""
        return len(self._cache)

    @property
    def stats(self) -> dict:
        """Cache statistics."""
        total_requests = self._hits + self._misses
        hit_rate = self._hits / total_requests if total_requests > 0 else 0.0
        return {
            "size": len(self._cache),
            "max_size": self.config.cache_max_entries,
            "hits": self._hits,
            "misses": self._misses,
            "evictions": self._evictions,
            "hit_rate": round(hit_rate, 3),
            "total_requests": total_requests,
        }

    def keys(self) -> list[str]:
        """List all cache keys."""
        with self._lock:
            return list(self._cache.keys())

    def peek(self, key: str) -> Optional[Any]:
        """Get a value without affecting LRU order or hit count."""
        with self._lock:
            entry = self._cache.get(key)
            if entry is None or entry.is_expired:
                return None
            return entry.data
