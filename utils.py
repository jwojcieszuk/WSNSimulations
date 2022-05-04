import logging
from enum import Enum
import math
from functools import lru_cache


class Colors:
    BLACK = "black"
    GREEN = "green"
    RED = "red"
    PURPLE = "purple"
    PINK = "pink"
    BlUE = "blue"
    colors_list = [BLACK, GREEN, RED, PURPLE, PINK, BlUE]


def euclidean_distance(node1, node2):
    return math.sqrt((node1.pos_x - node2.pos_x)**2 + (node1.pos_y - node2.pos_y) ** 2)


class DuplicateFilter:
    """
    Filters away duplicate log messages.
    Modified version of: https://stackoverflow.com/a/31953563/965332
    """

    def __init__(self, logger):
        self.msgs = set()
        self.logger = logger

    def filter(self, record):
        msg = str(record.msg)
        is_duplicate = msg in self.msgs
        if not is_duplicate:
            self.msgs.add(msg)
        return not is_duplicate

    def __enter__(self):
        self.logger.addFilter(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.removeFilter(self)