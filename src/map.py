from typing import List, NamedTuple, Optional, TypedDict
import math
from random import random, randint, sample
from datatypes import InformationData
from enum import Enum
from dataclasses import dataclass


def euclidian_distance(a: InformationData, b: InformationData):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


class CELL_STATE(Enum):
    EMPTY = 0
    OCCUPIED = 1
    CARRYING = 2


@dataclass
class Cell:
    value: Optional[InformationData] = None
    busy: CELL_STATE = CELL_STATE.EMPTY


class Map:
    def __init__(self, size, block_size: int, screen, database: List[InformationData]):
        self.width = size
        self.height = size
        self.size = size
        self.screen = screen
        self.pos_x = 0
        self.pos_y = 0
        self._zoom = 0
        self.drag = False
        self.grid: List[List[Cell]] = [
            [Cell() for _ in range(size)] for _ in range(size)
        ]
        self.block_size = block_size
        self.margin = math.ceil(self.block_size * 0.2)
        self.database = database
        self.alpha = self._calc_alpha()
        self.data_distribution()

    def data_distribution(self):
        positions = [(m, n) for m in range(self.size) for n in range(self.size)]
        candidates = sample(positions, len(self.database))

        for (i, (x, y)) in enumerate(candidates):
            self.grid[x][y].value = self.database[i]

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = min(max(value, 0), 90)

    def _calc_alpha(self):
        s = 0
        for a in self.database:
            for b in self.database:
                s += euclidian_distance(a, b)
        return s / (len(self.database) ** 2)
