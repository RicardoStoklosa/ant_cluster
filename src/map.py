import pygame
import pygame_gui
import math
from random import random, randint


class Map:
    def __init__(self, size, block_size: int, density: float, screen):
        self.width = size
        self.height = size
        self.size = size
        self.screen = screen
        self.pos_x = 0
        self.pos_y = 0
        self._zoom = 0
        self.drag = False
        self.grid = [
            [{"value": 0, "busy": 0} for _ in range(size)] for _ in range(size)
        ]

        self.block_size = block_size

        self.margin = math.ceil(self.block_size * 0.2)
        self.random_generator(density)

    def random_generator(self, fill_percentage):
        for y in range(self.width):
            for x in range(self.height):
                if random() <= fill_percentage:
                    r = randint(0, 1)
                    self.grid[y][x]["value"] = r

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = min(max(value, 0), 90)
