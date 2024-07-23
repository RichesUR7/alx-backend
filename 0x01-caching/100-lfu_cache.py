#!/usr/bin/env python3
""" LFUCache module """

from collections import defaultdict
from typing import Any, Optional

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache defines:
        - caching system using LFU algorithm.
    """

    def __init__(self) -> None:
        """Initialize LFU algorithm."""
        super().__init__()
        # A defaultdict to keep track of the usage count of items
        self.usage_count = defaultdict(int)
        # A list to keep track of the order of items
        self.key_order = []

    def put(self, key: str, item: Any) -> None:
        """Add an item in the cache using LFU algorithm."""
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.cache_data[key] = item
            self.usage_count[key] += 1
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the least frequently used item(s)
                min_cnt = min(self.usage_count.values())
                least_frequent_keys = [
                    k for k in self.key_order if self.usage_count[k] == min_cnt
                ]

                discard_key = least_frequent_keys[0]

                # - Remove the item from the cache
                # - Remove the item from the usage count
                # - Remove the item from the key order
                self.cache_data.pop(discard_key)
                self.usage_count.pop(discard_key)
                self.key_order.remove(discard_key)
                print(f"DISCARD: {discard_key}")

            # - Add the new item to the cache
            # - Increment the usage count of the new item
            # - Add the new key to the key order
            self.cache_data[key] = item
            self.usage_count[key] += 1
            self.key_order.append(key)

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key."""
        if key in self.cache_data:
            self.usage_count[key] += 1
            return self.cache_data[key]
        return None
