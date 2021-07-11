import pygame
import math
from random import choices
from colors import *


def random_move(pos):
    return pos + choices([-1, 0, 1])[0]


class Ant:
    def __init__(self, position, range, map):
        self.x = position[0]
        self.y = position[1]
        self.range = range
        self.carrying = False
        self.map = map

        self.block_size = 1

        self.margin = math.ceil(self.block_size * 0.1)

    def walk(self):
        walk = lambda x: min(max(random_move(x), 0), self.map.size - 1)
        self.x = walk(self.x)
        self.y = walk(self.y)
        self.map.grid[self.x][self.y] = self

    def look(self):
        

    def action(self):
        if "algo":
            self.walk()

# classe Ant
# posicao
# estado

# classe Mapa
# grid
# 0, 1, 2

# ant se desloca apanas para chao
# se ant encontra dead_ant, decide se pega ou desvia
#  se ant pega, dead_ant some e fica so ant com estado = carrying
# se ant encontra 

