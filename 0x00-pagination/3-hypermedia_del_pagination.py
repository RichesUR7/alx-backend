#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import Dict, List


class Server:
    """Server class to paginate a database of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE, encoding="utf-8") as f:
                reader = csv.reader(f)
                dataset = list(reader)
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i: dataset[i]
                                      for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Returns paginated data starting from the given index.

        Args:
            index (int): Starting index for pagination.
            page_size (int): Number of items per page.

        Returns:
            dict: Paginated data and related information.
        """
        assert isinstance(index, int) and index >= 0
        assert isinstance(page_size, int) and page_size > 0

        indexed_data = self.indexed_dataset()
        dataset_size = len(indexed_data)

        if index is None or index >= dataset_size:
            index = 0

        data = []
        current_index = index
        items_added = 0

        while items_added < page_size and current_index < dataset_size:
            item = indexed_data.get(current_index)
            if item:
                if items_added == 0:
                    start_index = current_index

                data.append(item)
                items_added += 1
            current_index += 1

        next_index = current_index if current_index < dataset_size else None

        return {
            "index": start_index,
            "data": data,
            "page_size": page_size,
            "next_index": next_index,
        }
