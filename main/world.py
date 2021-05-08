from pygame.surface import Surface

from entities.player import Player
from main.camera import Camera
from main.generate import Grid
from main.constants import Constant


class World(object):
    def __init__(self, amount_tiles_x, amount_tiles_y):
        self.amount_tiles_x = amount_tiles_x
        self.amount_tiles_y = amount_tiles_y
        self.grid = Grid(self.amount_tiles_x, self.amount_tiles_y)
        self.player = Player(Constant.TILE_SIZE * self.grid.doominos_location[0], Constant.TILE_SIZE * self.grid.doominos_location[1])

    def handle_input(self, event):
        self.player.handle_input(event)

    def step(self):
        self.player.step()

    def draw(self, screen: Surface, camera: Camera):
        self.grid.draw(screen, camera)
        self.player.draw(screen, camera)