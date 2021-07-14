import pygame
import pygame_gui
from map import Map
from colors import *
from colony import Colony


class Game:
    epoch = 0
    running = True
    pause = False
    step = False

    def __init__(self, width: int, height: int):
        self.window = [width, height]
        self.init_pygame()
        self.map = Map(50, 5, 0.5, self.screen)
        self.colony = Colony(self.screen, self.map, 200, 1)
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0
        self.simulation_pace = 10

    def init_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode(self.window)
        self.gui = pygame_gui.UIManager(self.window)

        pygame.display.set_caption("Ant Clusterring")

        self.clock = pygame.time.Clock()

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

            pygame.display.flip()

    def handle_keyboard(self, events):
        for event in events:
            map_mov = 5
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.step = True
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause
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
        self.colony.update_ants_position()
        self.epoch += 1

    def simulation_render(self, pace):
        if self.epoch % pace == 0 or self.pause:
            self.screen.fill(GRAY)
            self.colony.draw()
            if not self.pause or self.step:
                print(f"Época: {self.epoch}")


if __name__ == "__main__":
    game = Game(1200, 1200)
    game.run()
