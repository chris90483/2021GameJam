from pygame.surface import Surface

from audio.emitter_handler import EmitterHandler
from entities.zombie_handler import ZombieHandler
from entities.destination_flag import DestinationFlag
from main.camera import Camera
from main.grid import CellType, Cell, Grid
from entities.player import Player
from entities.compass import Compass
from entities.delivery_status import DeliveryStatus
from main.camera import Camera
from main.grid import Grid
from main.constants import Constant
from main.destination import Destination


class World(object):
    def __init__(self, amount_tiles_x, amount_tiles_y, audio_manager):
        self.audio_manager = audio_manager
        self.amount_tiles_x = amount_tiles_x
        self.amount_tiles_y = amount_tiles_y
        self.grid = Grid(self.amount_tiles_x, self.amount_tiles_y)
        self.player = Player(Constant.TILE_SIZE * self.grid.doominos_location[0],
                             Constant.TILE_SIZE * self.grid.doominos_location[1], self, audio_manager)
        self.zombie_handler = ZombieHandler()
        self.emitter_handler = EmitterHandler(self.zombie_handler)
        self.destination = Destination(self.grid, self.player)
        self.destination_flag = DestinationFlag(self.destination, self.player)
        self.compass = Compass(self.destination, self.player)
        self.delivery_status = DeliveryStatus(self.destination)

    def handle_input(self, event):
        self.player.handle_input(event)

    def step(self):
        self.emitter_handler.step()
        self.player.step()
        self.destination.step()
        self.zombie_handler.step()
        self.destination_flag.step(self.destination)

    def draw(self, screen: Surface, camera: Camera):
        self.grid.draw(screen, camera)
        self.emitter_handler.draw(screen, camera)
        self.player.draw(screen, camera)
        self.destination_flag.draw(screen, camera)
        self.compass.draw(screen)
        self.delivery_status.draw(screen)

        self.zombie_handler.draw(screen, camera)