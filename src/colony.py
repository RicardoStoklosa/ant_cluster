from random import choices, randint
import math

import pygame

from ant import Ant
from colors import *


def random_move(pos):
    return pos + choices([-1, 0, 1])[0]


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
        for _ in range(self.population_size):
            x = randint(0, self.map.size-1)
            y = randint(0, self.map.size-1)
            ant = Ant((x, y), self.ANT_VIEW_RANGE, self.map)
            self.map.grid[x][y]["busy"] = True

            self.ants.append(ant)

    def update_ants_position(self):
        for ant in self.ants:
            ant.action()

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
                if self.map.grid[row][column]["busy"]:
                    color = RED
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

        # for ant in self.ants:
        #     color = RED if ant.carrying else GREEN

        #     pygame.draw.rect(
        #         self.screen,
        #         color,
        #         pygame.Rect(
        #             [
        #                 (size) * (ant.x),
        #                 (size) * (ant.y),
        #                 size,
        #                 size,
        #             ]
        #         ).move(x, y),
        #     )
