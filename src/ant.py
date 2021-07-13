import pygame
import math
from random import choices, random
from colors import *


def random_move(pos):
    return pos + choices([-1, 0, 1])[0]


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

    def non_busy_location(self, world):
        walk = lambda x: min(max(random_move(x), 0), world.size - 1)
        candidate_x, candidate_y = walk(self.x), walk(self.y)
        while (
            world.grid[candidate_x][candidate_y]["busy"] != 0
            and candidate_x != 0 != candidate_y
        ):
            candidate_x, candidate_y = walk(candidate_x), walk(candidate_y)
        return candidate_x, candidate_y

    def walk(self, world):
        world.grid[self.x][self.y]["busy"] = 0
        self.x, self.y = self.non_busy_location(world)
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
