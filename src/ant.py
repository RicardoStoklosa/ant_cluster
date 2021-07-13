import pygame
import math
from random import choices, random
from colors import *


def random_move(pos):
    return pos + choices([-1, 1])[0]


class Ant:
    def __init__(self, position, range, map):
        self.x = position[0]
        self.y = position[1]
        self.vision_range = range
        self.field_size = (1 + 2 * range) ** 2 - 1
        self.carrying = 0
        self.block_size = 1
        self.alpha = 3

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

    def get_valid_movement(self, world):
        valid_movements = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i != 0 or j != 0:
                    x = self.x + i
                    y = self.y + j

                    x = self.pacman_move(x, world.size)
                    y = self.pacman_move(y, world.size)

                    if world.grid[x][y]["busy"] == 0:
                        valid_movements.append((x, y))

        return valid_movements

    def walk(self, world):
        candidates = self.get_valid_movement(world)
        if len(candidates):
            world.grid[self.x][self.y]["busy"] = 0
            self.x, self.y = choices(candidates)[0]
            world.grid[self.x][self.y]["busy"] = 2 if self.carrying > 0 else 1

    def pick_body(self, world):
        if self.carrying == 0:
            self.carrying = world.grid[self.x][self.y]["value"]
            world.grid[self.x][self.y]["value"] = 0

    def drop_body(self, world):
        if self.carrying > 0:
            world.grid[self.x][self.y]["value"] = self.carrying
            self.carrying = 0

    def look_and_count(self, view_field):
        n_local = -1  # discounting himself

        for row in view_field:
            for col in row:
                if col["value"] > 0:
                    n_local += 1
        return n_local + 0.1

    def action(self, world, view_field):
        if self.carrying:
            if world.grid[self.x][self.y]["value"] > 0:
                self.walk(world)
            else:
                p = (self.look_and_count(view_field) / self.field_size) ** 2
                if p * self.alpha > random():
                    self.drop_body(world)
                    self.walk(world)
                else:
                    self.walk(world)
        else:
            if world.grid[self.x][self.y]["value"] > 0:
                p = (self.look_and_count(view_field) / self.field_size) ** 2
                if p < random():
                    self.pick_body(world)
                    self.walk(world)
                else:
                    self.walk(world)
            else:
                self.walk(world)
