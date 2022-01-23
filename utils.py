from enum import Enum
import math


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


