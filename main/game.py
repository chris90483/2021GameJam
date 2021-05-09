"""
    This class will hold the world and all other game features
"""
from pygame.surface import Surface

from main.camera import Camera
from main.inventory import Inventory
from main.world import World
from main.score import Score


class Game(object):
    def __init__(self, amount_tiles_x, amount_tiles_y, audio_manager):
        self.audio_manager = audio_manager
        self.score = Score()
        self.world = World(amount_tiles_x, amount_tiles_y, audio_manager, self.score)
        self.camera = Camera(self.world.player)

    def handle_input(self, event):
        self.world.handle_input(event)

    def step(self):
        self.world.step()

    def draw(self, screen: Surface):
        self.world.draw(screen, self.camera)

