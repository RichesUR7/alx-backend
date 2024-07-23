#!/usr/bin/env python3
""" LRUCache module. """

from collections import OrderedDict
from typing import Any, Optional

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """
    LRUCache defines:
        - caching system using LRU algorithm.
    """

    def __init__(self) -> None:
        """Initialize LRU algorithm."""
        super().__init__()
        # OrderedDict to keep track of the order of items
        self.cache_data = OrderedDict()

    def put(self, key: str, item: Any) -> None:
        """Add an item in the cache using LRU algorithm."""
        if key and item:
            self.cache_data[key] = item
            # Move the key to the end of the OrderedDict (most recently used)
            self.cache_data.move_to_end(key)
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                # Remove the least recently used item from the cache
                discarded_key = next(iter(self.cache_data))
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key"""
        if key in self.cache_data:
            self.cache_data.move_to_end(key)
            return self.cache_data.get(key)
        return None
