from collections import namedtuple
from typing import List, NamedTuple
import pygame
import pygame_gui
from map import Map
from colors import *
from colony import Colony
from pathlib import Path
from datatypes import InformationData


class Game:
    epoch = 0
    running = True
    pause = False
    step = False
    stop_render = False

    def __init__(
        self,
        width: int,
        height: int,
        map_size: int = 50,
        colony_size: int = 50,
        max_epoch: int = None,
    ):
        self.window = [width, height]
        self.init_pygame()
        self.read_input("../base_sintetica_4_g.in")
        self.map = Map(map_size, 5, self.screen, self.database)
        self.colony = Colony(self.screen, self.map, colony_size, 2, max_epoch)
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0
        self.simulation_pace = 10
        self.max_epoch = max_epoch

    def read_input(self, path: str):
        self.database: List[InformationData] = []
        path = Path(__file__).parent / path
        fix_float = lambda x: float(x.replace(",", "."))

        with open(Path(__file__).parent / path, "r") as file:
            for line in file:
                line = line.strip()
                line = line.split(" ")
                data = InformationData(
                    fix_float(line[0]), fix_float(line[1]), int(line[2])
                )
                self.database.append(data)

    def init_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode(self.window)
        self.gui = pygame_gui.UIManager(self.window)

        pygame.display.set_caption("Ant Clusterring")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Impact", 60)

    def run(self):
        self.time_delta = self.clock.tick(60) / 1000.0

        while self.running:
            self.clock.tick()
            events = pygame.event.get()
            self.handle_keyboard(events)

            if self.step:
                self.simulation_calculus()
                self.simulation_render(1)
                self.step = not self.step

            if not self.pause:
                self.simulation_calculus()
            self.simulation_render(self.simulation_pace)

            pace = 1000
            if self.epoch % pace == 0 or not self.stop_render:
                pygame.display.flip()

    def handle_keyboard(self, events):
        for event in events:
            map_mov = 5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.step = True
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
                if event.key == pygame.K_r:
                    self.stop_render = not self.stop_render
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

            self.gui.process_events(event)

    def simulation_calculus(self):
        continue_update = self.colony.update_ants_position(self.epoch)
        if continue_update:
            self.epoch += 1
        else:
            self.pause = True

    def simulation_render(self, pace):
        pace = pace if not self.stop_render else 1000
        if self.epoch % pace == 0 or self.pause:
            self.screen.fill(GRAY)
            if not self.stop_render:
                self.colony.draw()
            textsurface = self.font.render(f"Época: {self.epoch}", False, (0, 0, 0))
            self.screen.blit(textsurface, (0, 0))


if __name__ == "__main__":
    game = Game(width=800, height=800, map_size=50, colony_size=50, max_epoch=50000)
    game.run()
