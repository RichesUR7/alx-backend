#!/usr/bin/env python3
"""
Module for pagination helper function
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculate start and end index for pagination.

    Parameters:
    page (int): Current page number
    page_size (int): Item per page

    Returns:
    Tuple[int, int]: Start and end index
    """

    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index
