from map import CELL_STATE, Map
from data import Data
from typing import List, Optional
import math
from random import choices, random
from colors import *


def p_pick(k, f):
    return (k / (k + f)) ** 2


def p_drop(k, f):
    return 2 * f if f < k else 1


class Ant:
    def __init__(self, position, range):
        self.x = position[0]
        self.y = position[1]
        self.vision_range = range
        self.field_size = (1 + 2 * range) ** 2 - 1
        self.carrying: Optional[Data] = None
        self.block_size = 1
        self.k_pick = 0.5
        self.k_drop = 0.4

        self.margin = math.ceil(self.block_size * 0.1)

    # 0 - vazio
    # 1 - ocupado
    # 2 - ocupado e carregando

    def pacman_move(self, axis, size, movement=1):
        if axis < 0:
            axis = size - movement
        elif axis >= size:
            axis = movement - 1

        return axis

    def get_valid_movement(self, world: Map):
        valid_movements = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i != 0 or j != 0:
                    x = self.x + i
                    y = self.y + j

                    x = self.pacman_move(x, world.size)
                    y = self.pacman_move(y, world.size)

                    if world.grid[x][y].busy is CELL_STATE.EMPTY:
                        valid_movements.append((x, y))

        return valid_movements

    def walk(self, world: Map):
        candidates = self.get_valid_movement(world)
        if candidates:
            world.grid[self.x][self.y].busy = CELL_STATE.EMPTY
            self.x, self.y = choices(candidates)[0]
            world.grid[self.x][self.y].busy = CELL_STATE.CARRYING if self.carrying else CELL_STATE.OCCUPIED


    def pick_body(self, world):
        if not self.carrying:
            self.carrying = world.grid[self.x][self.y].value
            world.grid[self.x][self.y].value = None

    def drop_body(self, world):
        if self.carrying:
            world.grid[self.x][self.y].value = self.carrying
            self.carrying = None

    def look_and_count(self, view_field: List[List[Optional[Data]]]):
        n_local = -1  # discounting himself

        for row in view_field:
            for col in row:
                if col.value:
                    n_local += 1
        return n_local

    def action(self, world: Map, view_field: int):
        if self.carrying is not None:
            if world.grid[self.x][self.y].value:
                self.walk(world)
            else:
                f = self.look_and_count(view_field) / self.field_size
                p = p_drop(self.k_drop, f)
                if p > random():
                    self.drop_body(world)
                    self.walk(world)
                else:
                    self.walk(world)
        else:
            if world.grid[self.x][self.y].value:
                f = self.look_and_count(view_field) / self.field_size
                p = p_pick(self.k_pick, f)
                if p > random():
                    self.pick_body(world)
                    self.walk(world)
                else:
                    self.walk(world)
            else:
                self.walk(world)
