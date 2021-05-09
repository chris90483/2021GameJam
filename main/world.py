from pygame.surface import Surface

from audio.emitter_handler import EmitterHandler
from entities.compass import Compass
from entities.delivery_status import DeliveryStatus
from entities.destination_flag import DestinationFlag
from entities.player import Player
from entities.zombie_handler import ZombieHandler
from entities.dog_handler import DogHandler
from main.camera import Camera
from main.constants import Constant
from main.destination import Destination
from main.grid import Grid
from main.inventory import Inventory
from entities.health_bar import HealthBar
from main.util import convert_world_to_grid_position


class World(object):
    def __init__(self, amount_tiles_x, amount_tiles_y, audio_manager, score):
        self.audio_manager = audio_manager
        self.amount_tiles_x = amount_tiles_x
        self.amount_tiles_y = amount_tiles_y
        self.grid = Grid(self.amount_tiles_x, self.amount_tiles_y)
        self.player = Player(self, audio_manager)
        self.zombie_handler = ZombieHandler(self)
        self.dog_handler = DogHandler(self)
        self.emitter_handler = EmitterHandler(self.zombie_handler)
        self.destination = Destination(self, score)
        self.destination_flag = DestinationFlag(self)
        self.compass = Compass(self)
        self.delivery_status = DeliveryStatus(self, score)
        self.inventory = Inventory(self)
        self.health_bar = HealthBar(self.player)

        self.pizza = None
        self.populated_tiles = [[False for _ in range(Constant.GRID_HEIGHT)] for _ in range(Constant.GRID_WIDTH)]

    def handle_input(self, event):
        self.player.handle_input(event)

    def step(self):
        self.emitter_handler.step()
        player_grid_location_before = convert_world_to_grid_position(self.player.x, self.player.y)
        self.player.step()
        player_grid_location_after = convert_world_to_grid_position(self.player.x, self.player.y)
        if player_grid_location_after != player_grid_location_before:
            self._update_spawn_regions(player_grid_location_after)
        self.destination.step()
        self.zombie_handler.step()
        self.dog_handler.step()

        if self.pizza:
            self.pizza.step()

    def draw(self, screen: Surface, camera: Camera):
        # Grid
        self.grid.draw(screen, camera)
        self.destination_flag.draw(screen, camera)

        # Sound circle
        self.emitter_handler.draw(screen, camera)

        if self.pizza:
            self.pizza.draw(screen, camera)

        # Moving entites
        self.player.draw(screen, camera)
        self.zombie_handler.draw(screen, camera)
        self.dog_handler.draw(screen, camera)

        # UI
        self.compass.draw(screen, camera)
        self.delivery_status.draw(screen)
        self.inventory.draw(screen, camera)
        self.health_bar.draw(screen)

    def _update_spawn_regions(self, pos):
        x, y = pos
        new_regions = set()
        for dx in range(-Constant.GRID_SPAWN_RANGE, Constant.GRID_SPAWN_RANGE + 1):
            for dy in range(-Constant.GRID_SPAWN_RANGE, Constant.GRID_SPAWN_RANGE + 1):
                if self.grid.is_in_grid(x + dx, y + dy) and not self.populated_tiles[x + dx][y + dy]:
                    new_regions.add((x + dx, y + dy))

        for region in new_regions:
            self._spawn_in_tile(region)

    def _spawn_in_tile(self, region):
        pass




