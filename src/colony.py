from random import randint, sample
import math

import pygame

from ant import Ant
from colors import *


def get_view(grid, x, y, n):
    h = len(grid) - 1
    v = len(grid[0]) - 1
    u = y - n
    d = y + n
    l = x - n
    r = x + n

    res = []
    for i in range(u, d + 1):
        if i < 0:
            i = h + i + 1
        elif i > h:
            i = 0 + i - 1

        line = []
        for j in range(l, r + 1):
            if j < 0:
                j = v + j + 1
            elif j > v:
                j = 0 + j - 1

            line.append(grid[i][j])
        res.append(line)

    return res


class Colony:
    def __init__(self, screen, map_grid, population_size, ant_view_range):
        self.map = map_grid
        self.screen = screen
        self.population_size = population_size
        self.ants = []
        self.ANT_VIEW_RANGE = ant_view_range
        self.generate_ants()
        self.pos = (0, 0)

    def generate_ants(self):
        indices = [(m, n) for m in range(self.map.size) for n in range(self.map.size)]
        candidates = sample(indices, self.population_size)

        for x, y in candidates:
            ant = Ant((x, y), self.ANT_VIEW_RANGE, self.map)
            self.map.grid[x][y]["busy"] = 1
            self.ants.append(ant)

    def update_ants_position(self):
        for ant in self.ants:
            view_field = get_view(self.map.grid, ant.x, ant.y, self.ANT_VIEW_RANGE)
            ant.action(self.map, view_field)

    def draw(self):
        zoom_p = self.map._zoom / 100
        screen_size = self.screen.get_size()
        x = min(max(self.map.pos_x, -screen_size[0]), screen_size[0])
        y = min(max(self.map.pos_y, -screen_size[1]), screen_size[1])

        size = math.ceil(
            screen_size[0] / (self.map.size - math.ceil((self.map.size) * zoom_p))
        )
        for row in range(self.map.size):
            for column in range(self.map.size):
                color = LIGHT_GRAY
                if self.map.grid[row][column]["busy"] == 2:
                    color = RED
                elif self.map.grid[row][column]["busy"] == 1:
                    color = GREEN
                elif self.map.grid[row][column]["value"] > 0:
                    color = BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        [
                            (size) * column,
                            (size) * row,
                            size,
                            size,
                        ]
                    ).move(x, y),
                )
