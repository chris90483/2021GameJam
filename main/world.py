from pygame.surface import Surface

from entities.player import Player

class World(object):
    def __init__(self, amount_tiles_x, amount_tiles_y):
        self.amount_tiles_x = amount_tiles_x
        self.amount_tiles_y = amount_tiles_y
        self.player = Player(400, 400)

    def handle_input(self, event):
        self.player.handle_input(event)

    def step(self):
        self.player.step()

    def draw(self, screen: Surface):
        self.player.draw(screen)