import pygame
import pygame_gui
import math
from random import random, randint
from Ant import Ant

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (220, 220, 220)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)




class Map:
    def __init__(self, width: int, height: int, block_size: int, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.pos = [0, 0]
        self._zoom = 0
        self.drag = False
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

        self.block_size = block_size
        self.colony = [
            Ant(6, 2, (randint(0, 133), randint(0, 133)), self.screen)
            for _ in range(100)
        ]

        self.margin = math.ceil(self.block_size * 0.2)
        self.random_generator(0.3)

    def random_generator(self, fill_percentage):
        for y in range(self.width):
            for x in range(self.height):
                if random() <= fill_percentage:
                    r = randint(0, 1)
                    self.grid[y][x] = r

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        self._zoom = min(max(value, 0), 90)

    def draw(self):
        zoom_p = self._zoom/100
        screen_size = self.screen.get_size()
        x = min(max(self.pos[0], -screen_size[0]), screen_size[0])
        y = min(max(self.pos[1], -screen_size[1]), screen_size[1])
        
        size = math.ceil(800 / (self.width - math.ceil((self.width)* zoom_p )))
        for row in range(self.width):
            for column in range(self.height):
                color = LIGHT_GRAY
                if self.grid[row][column] == 1:
                    color = BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect([
                        (size) * column,
                        (size) * row,
                        size,
                        size,
                    ]).move(x, y)
                    ,
                )

        for ant in self.colony:
            ant.draw(size, (x, y))



