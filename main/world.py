from pygame.surface import Surface

from main.camera import Camera
from main.generate import CellType, Cell, Grid
from entities.player import Player

class World(object):
    def __init__(self, amount_tiles_x, amount_tiles_y):
        self.amount_tiles_x = amount_tiles_x
        self.amount_tiles_y = amount_tiles_y
        self.player = Player(400, 400)
        self.grid = Grid(self.amount_tiles_x, self.amount_tiles_y)


    def handle_input(self, event):
        self.player.handle_input(event)

    def step(self):
        self.player.step()

    def draw(self, screen: Surface, camera: Camera):
        self.grid.draw(screen, camera)
        self.player.draw(screen, camera)