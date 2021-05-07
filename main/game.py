"""
    This class will hold game entities and will call the draw and step methods of these entities
"""
from pygame.surface import Surface

from entities.player import Player


class Game(object):
    def __init__(self):
        self.player = Player(400, 400)

    def handle_input(self, event):
        self.player.handle_input(event)

    def step(self):
        self.player.step()

    def draw(self, screen: Surface):
        self.player.draw(screen)

