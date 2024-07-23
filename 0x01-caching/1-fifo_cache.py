#!/usr/bin/env python3
""" FIFOCache module. """

from collections import deque
from typing import Any, Optional

from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """
    FIFOCache defines:
        - caching system using FIFO algorithm.
    """

    def __init__(self) -> None:
        """Initialization the cache and queue."""
        super().__init__()
        # A deque to keep track of the order of items
        self.queue = deque()

    def put(self, key: str, item: Any) -> None:
        """Add an item in the cache using FIFO algorithm."""
        if key and item:
            self.cache_data[key] = item
            self.queue.append(key)
            # If the cache is full
            if len(self.queue) > BaseCaching.MAX_ITEMS:
                # Remove the oldest item from the cache (FIFO)
                discarded_key = self.queue.popleft()
                del self.cache_data[discarded_key]
                print(f"DISCARD: {discarded_key}")

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key."""
        return self.cache_data.get(key) if key else None
