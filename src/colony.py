from map import CELL_STATE, Map
from random import randint, sample
import math

import pygame

from ant import Ant
from colors import *


def get_view(grid, x, y, n):
    h = len(grid)
    v = len(grid[0])
    left_upper_x = (x - n + h) % h
    left_upper_y = (y - n + v) % v
    res = []
    for i in range(0, 2 * n + 1):
        line = []
        pos_x = (left_upper_x + i + h) % h
        for j in range(0, 2 * n + 1):
            pos_y = (left_upper_y + j + v) % v
            line.append(grid[pos_x][pos_y])
        res.append(line)
    return res


class Colony:
    def __init__(self, screen, map_grid: Map, population_size, ant_view_range):
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
            ant = Ant((x, y), self.ANT_VIEW_RANGE)
            self.map.grid[x][y].busy = CELL_STATE.OCCUPIED
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
                if self.map.grid[row][column].busy == CELL_STATE.CARRYING:
                    color = RED
                elif self.map.grid[row][column].busy == CELL_STATE.OCCUPIED:
                    color = GREEN
                elif self.map.grid[row][column].value:
                    color = GRADIENT_4[self.map.grid[row][column].value.label - 1]
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
