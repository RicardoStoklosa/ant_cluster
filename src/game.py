import pygame
import pygame_gui
from map import Map
from colors import *
from colony import Colony
import math


class Game:
    running = True
    pause = False
    fps = "0"

    def __init__(self, width: int, height: int):
        self.window = [width, height]
        self.init_pygame()
        self.map = Map(133, 4, self.screen)
        self.colony = Colony(self.screen, self.map, 100, 2)
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0

    def init_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode(self.window)
        self.gui = pygame_gui.UIManager(self.window)
        self.ui()

        pygame.display.set_caption("Ant Clusterring")

        self.clock = pygame.time.Clock()

    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0

        while self.running:
            self.clock.tick(60)
            events = pygame.event.get()
            self.handle_keyboard(events)
            if not self.pause:
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
                    self.map.pos_x += map_mov
                if event.key == pygame.K_RIGHT:
                    self.map.pos_x -= map_mov
                if event.key == pygame.K_UP:
                    self.map.pos_y += map_mov
                if event.key == pygame.K_DOWN:
                    self.map.pos_y -= map_mov
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
                    self.mouse_offset_x = self.map.pos_x - mouse_x
                    self.mouse_offset_y = self.map.pos_y - mouse_y

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.map.drag = False

            if event.type == pygame.MOUSEMOTION:
                if self.map.drag:
                    mouse_x, mouse_y = event.pos
                    self.map.pos_x = mouse_x + self.mouse_offset_x
                    self.map.pos_y = mouse_y + self.mouse_offset_y

            # print(self.map.pos)
            self.gui.process_events(event)

    def game_loop(self, render=True):
        self.screen.fill(GRAY)
        pygame_gui.elements.UILabel(
            pygame.Rect((0, 0), (100, 50)), str(math.ceil(self.clock.get_fps())), self.gui
        )
        print(str(math.ceil(self.clock.get_fps())))
        # self.gui.update(self.time_delta)
        self.colony.update_ants_position()
        self.colony.draw()

        # self.gui.draw_ui(self.screen)


Game(1200, 1200).run()
