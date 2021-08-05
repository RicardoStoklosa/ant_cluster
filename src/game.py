from collections import namedtuple
from typing import List, NamedTuple
import pygame
import pygame_gui
from map import Map
from colors import *
from colony import Colony
from pathlib import Path
from datatypes import InformationData
import os
import time

out_dir = Path(__file__).parents[1] / "out"


class Game:
    epoch = 0
    running = True
    pause = False
    step = False
    stop_render = False

    def __init__(self, **kwargs):
        self.window = [kwargs["width"], kwargs["height"]]
        self.init_pygame()
        self.read_input(kwargs["file"])
        self.map = Map(kwargs["map_size"], 5, self.screen, self.database)
        self.colony = Colony(
            self.screen,
            self.map,
            kwargs["colony_size"],
            kwargs["ant_range"],
            kwargs["max_epoch"],
        )
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0
        self.simulation_pace = 10
        self.max_epoch = kwargs["max_epoch"]
        self.id = int(time.time())

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

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

            if self.epoch == 0:
                self.screenshot("start")

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
            self.stop_render = False
            self.pause = True
            self.screenshot("end")

    def simulation_render(self, pace):
        pace = pace if not self.stop_render else 1000

        if self.epoch % pace == 0 or self.pause:
            self.render(not self.stop_render)

    def render(self, render_map=True):
        self.screen.fill(GRAY)
        if render_map:
            self.colony.draw()
        textsurface = self.font.render(f"Época: {self.epoch}", False, WHITE)
        self.screen.blit(textsurface, (0, 0))

    def screenshot(self, name):
        self.render()
        pygame.image.save(self.screen, f"{out_dir}/{self.id}_{name}.jpg")


class SimulationConfig:
    def __init__(
        self,
        file: str,
        width: int = 800,
        height: int = 800,
        map_size: int = 50,
        colony_size: int = 50,
        ant_range: int = 1,
        max_epoch: int = None,
    ):
        self.file = file
        self.width = width
        self.height = height
        self.map_size = map_size
        self.colony_size = colony_size
        self.ant_range = ant_range
        self.max_epoch = max_epoch


if __name__ == "__main__":
    simulation = SimulationConfig(file=input())

    simulation.map_size = int(input())
    simulation.colony_size = int(input())
    simulation.ant_range = int(input())
    simulation.max_epoch = int(input())

    labels_4 = "../base_sintetica_4_g.in"
    labels_15 = "../base_sintetica_15_g.in"
    game = Game(**simulation.__dict__)
    game.run()
