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


class Game:
    running = True
    pause=False
    fps = 0

    def __init__(self, width: int, height: int):
        self.window = [width, height]
        self.init_pygame()
        self.map = Map(133, 133, 4, self.screen)
        self.offset_x = 0
        self.offset_y = 0

    

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
            map_mov = 5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.map.pos[1] += map_mov
                if event.key == pygame.K_RIGHT:
                    self.map.pos[1] -= map_mov
                if event.key == pygame.K_UP:
                    self.map.pos[0] += map_mov
                if event.key == pygame.K_DOWN:
                    self.map.pos[0] -= map_mov
                if event.key == 61:
                    print("+")
                    self.map.block_size += 5
                if event.key == pygame.K_MINUS:
                    self.map.block_size -= 5
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                if event.type == pygame.QUIT:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.map.zoom += map_mov
                elif event.button == 5:
                    self.map.zoom -= map_mov

                if event.button == 1:           
                    self.map.drag = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.map.pos[0] - mouse_x
                    self.offset_y = self.map.pos[1] - mouse_y

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    self.map.drag = False

            if event.type == pygame.MOUSEMOTION:
                if self.map.drag:
                    mouse_x, mouse_y = event.pos
                    self.map.pos[0] = mouse_x + self.offset_x
                    self.map.pos[1] = mouse_y + self.offset_y

            # print(self.map.pos)
            # self.gui.process_events(event)

    def game_loop(self, render = True):
        self.screen.fill(GRAY)
        pygame_gui.elements.UILabel(pygame.Rect((0, 0), (100, 50)), str(self.fps), self.gui)
        self.gui.update(self.time_delta)
        self.map.draw()
        for ant in self.map.colony:
            walk = lambda x, y: min(max(x + randint(-1, 1), 1), y-1)
            ant.x = walk(ant.x, self.map.width)
            ant.y = walk(ant.y, self.map.height)
                # ant.draw(self.map.block_size)

        # self.gui.draw_ui(self.screen)

Game(1200, 1200).run()
