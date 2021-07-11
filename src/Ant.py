import pygame
import math
from random import randint
from colors import *

class Ant:
    def __init__(self, block_size: int, range: int, position, screen):
        self.x = position[0]
        self.y = position[1]
        self.screen = screen
        self.range = range

        self.block_size = block_size

        self.margin = math.ceil(self.block_size * 0.1)

    def walk(self):
        self.x += randint(-1, 1)
        self.y += randint(-1, 1)

    def draw(self, size, desloc):
        color = RED

        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect([
                (size) * (self.x),
                (size) * (self.y),
                size,
                size,
            ]).move(desloc[0], desloc[1])
        )