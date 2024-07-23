#!/usr/bin/env python3

"""BasicCache module."""

from typing import Any, Optional

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    BasicCache defines:
        - caching system without limit
    """

    def put(self, key: str, item: Any) -> None:
        """Add an item in the cache."""
        if key and item:
            self.cache_data[key] = item

    def get(self, key: str) -> Optional[Any]:
        """Get an item by key."""
        return self.cache_data.get(key) if key else None
