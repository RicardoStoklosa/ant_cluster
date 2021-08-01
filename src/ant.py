from map import CELL_STATE, Map
from datatypes import InformationData, Position
from typing import List, Optional
import math
from random import choices, random
from colors import *


def sigmoid(c, x):
    return (1 - math.exp(-(c * x))) / (1 + math.exp(-(c * x)))


def euclidian_distance(a: InformationData, b: InformationData):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

c = 10
class Ant:
    def __init__(self, position: Position, field_range):
        self.x = position.x
        self.y = position.y
        self.field_range = field_range
        self.field_size = (1 + 2 * field_range) ** 2 - 1
        self.data_carrying: Optional[InformationData] = None

        self._block_size = 1
        self._margin = math.ceil(self._block_size * 0.1)

    def _torus_movement(self, axis, size, movement=1):
        if axis < 0:
            axis = size - movement
        elif axis >= size:
            axis = movement - 1

        return axis

    def _get_valid_movement(self, world: Map):
        valid_movements = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i != 0 or j != 0:
                    x = self.x + i
                    y = self.y + j

                    x = self._torus_movement(x, world.size)
                    y = self._torus_movement(y, world.size)

                    if world.grid[x][y].busy is CELL_STATE.EMPTY:
                        valid_movements.append((x, y))

        return valid_movements

    def _avg_similarity(
        self, world, current, view_field: List[List[Optional[InformationData]]]
    ):
        s = 0
        for row in view_field:
            for item in row:
                ret = 0
                if item.value:
                    dist = euclidian_distance(current, item.value)
                    ret = 1 - dist / world.alpha
                    s += ret

        fi = s / (self.field_size ** 2)
        return max(0, fi)

    def _walk(self, world: Map):
        valid_movements = self._get_valid_movement(world)
        if valid_movements:
            world.grid[self.x][self.y].busy = CELL_STATE.EMPTY
            self.x, self.y = choices(valid_movements)[0]
            world.grid[self.x][self.y].busy = (
                CELL_STATE.CARRYING if self.data_carrying else CELL_STATE.OCCUPIED
            )

    def _pick_body(self, world):
        if not self.data_carrying:
            self.data_carrying = world.grid[self.x][self.y].value
            world.grid[self.x][self.y].value = None

    def _drop_body(self, world):
        if self.data_carrying:
            world.grid[self.x][self.y].value = self.data_carrying
            self.data_carrying = None

    def action(self, world: Map, view_field: int):
        if self.data_carrying:
            if world.grid[self.x][self.y].value is None:
                f = self._avg_similarity(world, self.data_carrying, view_field)
                p = sigmoid(self.field_range * c, f)
                if p >= random():
                    self._drop_body(world)
        else:
            if world.grid[self.x][self.y].value:
                f = self._avg_similarity(
                    world, world.grid[self.x][self.y].value, view_field
                )
                p = 1 - sigmoid(self.field_range * c, f)
                if p >= random():
                    self._pick_body(world)
        self._walk(world)
