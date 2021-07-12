import pygame
import math
from random import choices, random
from colors import *


def random_move(pos):
    return pos + choices([-1, 0, 1])[0]


def get_view(grid, x, y, n):
    h = len(grid)
    v = len(grid[0])
    u = max(0, y - n)
    d = min(h - 1, y + n)
    l = max(0, x - n)
    r = min(v - 1, x + n)

    res = []
    for i in range(u, d + 1):
        res.append(grid[i][l : r + 1])

    return res


class Ant:
    def __init__(self, position, range, map):
        self.x = position[0]
        self.y = position[1]
        self.vision_range = range
        self.field_size = (1 + 2 * range) ** 2
        self.carrying = 0
        self.map = map
        self.block_size = 1
        self.alpha = 3

        self.margin = math.ceil(self.block_size * 0.1)

    # 0 - vazio
    # 1 - ocupado
    # 2 - ocupado e carregando

    def walk(self):
        walk = lambda x: min(max(random_move(x), 0), self.map.size - 1)
        self.map.grid[self.x][self.y]["busy"] = 0
        self.x = walk(self.x)
        self.y = walk(self.y)
        self.map.grid[self.x][self.y]["busy"] = 2 if self.carrying > 0 else 1

    def pick_body(self):
        if self.carrying == 0:
            self.carrying = self.map.grid[self.x][self.y]["value"]
            self.map.grid[self.x][self.y]["value"] = 0

    def drop_body(self):
        if self.carrying > 0:
            self.map.grid[self.x][self.y]["value"] = self.carrying
            self.carrying = 0

    def look_and_count(self):
        view_field = get_view(self.map.grid, self.x, self.y, self.vision_range)

        n_local = 0

        for row in view_field:
            for col in row:
                if col["value"] > 0:
                    n_local += 1
        return n_local + 0.1

    def action(self):
        if self.carrying:
            if self.map.grid[self.x][self.y]["value"] > 0:
                self.walk()
            else:
                p = (self.look_and_count() / self.field_size) ** 2
                if p * self.alpha > random():
                    self.drop_body()
                    self.walk()
                else:
                    self.walk()
        else:
            if self.map.grid[self.x][self.y]["value"] > 0:
                p = (self.look_and_count() / self.field_size) ** 2
                if p / self.alpha < random():
                    self.pick_body()
                    self.walk()
                else:
                    self.walk()
            else:
                self.walk()
