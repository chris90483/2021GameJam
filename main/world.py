from pygame.surface import Surface

from audio.emitter_handler import EmitterHandler
from entities.compass import Compass
from entities.delivery_status import DeliveryStatus
from entities.destination_flag import DestinationFlag
from entities.player import Player
from entities.zombie_handler import ZombieHandler
from entities.dog_handler import DogHandler
from main.camera import Camera
from main.destination import Destination
from main.grid import Grid
from main.inventory import Inventory
from entities.health_bar import HealthBar


class World(object):
    def __init__(self, amount_tiles_x, amount_tiles_y, audio_manager, score):
        self.audio_manager = audio_manager
        self.amount_tiles_x = amount_tiles_x
        self.amount_tiles_y = amount_tiles_y
        self.grid = Grid(self.amount_tiles_x, self.amount_tiles_y)
        self.player = Player(self.grid, self, audio_manager)
        self.zombie_handler = ZombieHandler(self)
        self.dog_handler = DogHandler(self.player, self)
        self.emitter_handler = EmitterHandler(self.zombie_handler)
        self.destination = Destination(self.grid, self.player, score, self)
        self.destination_flag = DestinationFlag(self.destination, self.player)
        self.compass = Compass(self.destination, self.player, self.destination_flag)
        self.delivery_status = DeliveryStatus(self.destination, score)
        self.inventory = Inventory(self)
        self.health_bar = HealthBar(self.player)

    def handle_input(self, event):
        self.player.handle_input(event)

    def step(self):
        self.emitter_handler.step()
        self.player.step()
        self.destination.step()
        self.zombie_handler.step()
        self.dog_handler.step()

    def draw(self, screen: Surface, camera: Camera):
        self.grid.draw(screen, camera)
        self.emitter_handler.draw(screen, camera)
        self.player.draw(screen, camera)
        self.destination_flag.draw(screen, camera)
        self.compass.draw(screen, camera)
        self.delivery_status.draw(screen)

        self.zombie_handler.draw(screen, camera)
        self.dog_handler.draw(screen, camera)

        self.inventory.draw(screen, camera)
        self.health_bar.draw(screen)
