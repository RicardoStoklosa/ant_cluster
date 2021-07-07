import pygame
import pygame_gui
import math
from random import random, randint

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (220, 220, 220)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Ant:
    def __init__(self, block_size: int, range: int, position, screen):
        self.x = position[0]
        self.y = position[1]
        self.screen = screen

        self.block_size = block_size

        self.margin = math.ceil(self.block_size * 0.1)

    def walk(self):
        self.x += randint(-1, 1)
        self.y += randint(-1, 1)

    def draw(self):
        color = GREEN

        pygame.draw.rect(
            self.screen,
            color,
            [
                (self.block_size) * self.x,
                (self.block_size) * self.y,
                self.block_size,
                self.block_size,
            ],
        )


class Map:
    def __init__(self, width: int, height: int, block_size: int, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

        self.block_size = block_size

        self.margin = math.ceil(self.block_size * 0.2)
        self.random_generator(0.3)

    def random_generator(self, fill_percentage):
        for y in range(self.width):
            for x in range(self.height):
                if random() <= fill_percentage:
                    r = randint(0, 1)
                    self.grid[y][x] = r

    def draw(self):
        for row in range(self.width):
            for column in range(self.width):
                color = LIGHT_GRAY
                if self.grid[row][column] == 1:
                    color = BLACK
                pygame.draw.rect(
                    self.screen,
                    color,
                    [
                        (self.block_size) * column,
                        (self.block_size) * row,
                        self.block_size,
                        self.block_size,
                    ],
                )


class Game:
    running = True
    pause=False
    fps = 0

    def __init__(self, width: int, height: int):
        self.window = [width, height]
        self.init_pygame()
        self.map = Map(133, 133, 6, self.screen)
        self.colony = [
            Ant(6, 2, (randint(0, 133), randint(0, 133)), self.screen)
            for _ in range(100)
        ]
        for ant in self.colony:
            print(ant.x, ant.y)

    def init_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode(self.window)
        self.gui = pygame_gui.UIManager(self.window)
        self.ui()

        pygame.display.set_caption("Ant Clusterring")

        self.clock = pygame.time.Clock()

    def run(self):
        self.time_delta = self.clock.tick(60)/1000.0
        while self.running:
            events = pygame.event.get()
            self.handle_keyboard(events)
            if(not self.pause):
                for _ in range(self.fps):
                    self.game_loop(render=False)
                self.game_loop()
            pygame.display.flip()

    def ui(self):
        pass
        # hello_button = pygame_gui.elements.UILabel(pygame.Rect((0, 0), (100, 50)), str(self.fps), self.gui)


    def handle_keyboard(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.map.block_size -= 1
                if event.key == pygame.K_RIGHT:
                    self.map.block_size += 1
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                if event.type == pygame.QUIT:
                    self.running = False
            self.gui.process_events(event)

    def game_loop(self, render = True):
        self.screen.fill(GRAY)
        print(self.clock.get_fps())
        pygame_gui.elements.UILabel(pygame.Rect((0, 0), (100, 50)), str(self.fps), self.gui)
        self.gui.update(self.time_delta)
        self.map.draw()
        for ant in self.colony:
            walk = lambda x, y: min(max(x + randint(-1, 1), 0), y)
            ant.x = walk(ant.x, self.map.width)
            ant.y = walk(ant.y, self.map.height)
            if render:
                ant.walk()
                ant.draw()

        self.gui.draw_ui(self.screen)

Game(800, 800).run()
