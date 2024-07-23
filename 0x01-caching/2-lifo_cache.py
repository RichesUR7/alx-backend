#!/usr/bin/env python3
""" LIFOCache module """

from typing import Any, Optional

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """
    LIFOCache defines:
        - caching system using LIFO algorithm.
    """

    def __init__(self) -> None:
        """Initialize LIFO algorithm"""
        super().__init__()
        # A list to keep track of the order of items
        self.keys = []

    def put(self, key: str, item: Any) -> None:
        """Add an item in the cache using LIFO algorithm."""
        if key and item:
            self.cache_data[key] = item
            if key in self.keys:
                self.keys.remove(key)
            self.keys.append(key)
            if len(self.keys) > BaseCaching.MAX_ITEMS:
                # Remove the most recently added item from the cache (LIFO)
                discarded_key = self.keys.pop(-2)
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key."""
        return self.cache_data.get(key) if key else None
