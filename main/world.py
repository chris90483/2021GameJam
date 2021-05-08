from pygame.surface import Surface

from main.camera import Camera
from main.grid import CellType, Cell, Grid
from entities.player import Player
from entities.compass import Compass
from main.camera import Camera
from main.grid import Grid
from main.constants import Constant
from main.destination import Destination


class World(object):
    def __init__(self, amount_tiles_x, amount_tiles_y):
        self.amount_tiles_x = amount_tiles_x
        self.amount_tiles_y = amount_tiles_y
        self.grid = Grid(self.amount_tiles_x, self.amount_tiles_y)
        self.player = Player(Constant.TILE_SIZE * self.grid.doominos_location[0], Constant.TILE_SIZE * self.grid.doominos_location[1])
        self.destination = Destination(self.grid, self.player)
        self.compass = Compass(self.destination, self.player)

    def handle_input(self, event):
        self.player.handle_input(event)

    def step(self):
        self.player.step()
        self.destination.step()

    def draw(self, screen: Surface, camera: Camera):
        self.grid.draw(screen, camera)
        self.player.draw(screen, camera)
        self.compass.draw(screen)