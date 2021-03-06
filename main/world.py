import random

from pygame.surface import Surface

from audio.emitter_handler import EmitterHandler
from entities.compass import Compass
from entities.delivery_status import DeliveryStatus
from entities.destination_flag import DestinationFlag
from entities.dog import Dog
from entities.player import Player
from entities.zombie import Zombie
from entities.zombie_handler import ZombieHandler
from entities.dog_handler import DogHandler
from main.camera import Camera
from main.constants import Constant
from main.destination import Destination
from main.grid import Grid, CellType
from main.inventory import Inventory
from entities.health_bar import HealthBar
from main.util import convert_world_to_grid_position, distance


class World(object):
    def __init__(self, amount_tiles_x, amount_tiles_y, audio_manager, score):
        self.audio_manager = audio_manager
        self.score = score
        self.amount_tiles_x = amount_tiles_x
        self.amount_tiles_y = amount_tiles_y
        self.grid = Grid(self.amount_tiles_x, self.amount_tiles_y, self)
        self.player = Player(self, audio_manager)
        self.zombie_handler = ZombieHandler(self)
        self.dog_handler = DogHandler(self)
        self.emitter_handler = EmitterHandler(self.zombie_handler)
        self.destination = Destination(self)
        self.destination_flag = DestinationFlag(self)
        self.compass = Compass(self)
        self.delivery_status = DeliveryStatus(self)
        self.inventory = Inventory(self)
        self.health_bar = HealthBar(self.player)

        self.pizza = None
        self.populated_tiles = [[False for _ in range(Constant.GRID_HEIGHT)] for _ in range(Constant.GRID_WIDTH)]
        self._update_spawn_regions(convert_world_to_grid_position(self.player.x, self.player.y))

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
        self.dog_handler.draw(screen, camera)
        self.player.draw(screen, camera)
        self.zombie_handler.draw(screen, camera)

        # UI
        self.compass.draw(screen, camera)
        self.delivery_status.draw(screen)
        self.inventory.draw(screen, camera)
        self.health_bar.draw(screen)

    def _update_spawn_regions(self, pos):
        x, y = pos
        new_grid = [[False for _ in range(Constant.GRID_HEIGHT)] for _ in range(Constant.GRID_WIDTH)]
        new_regions = set()
        for dx in range(-Constant.GRID_SPAWN_RANGE, Constant.GRID_SPAWN_RANGE + 1):
            for dy in range(-Constant.GRID_SPAWN_RANGE, Constant.GRID_SPAWN_RANGE + 1):
                if self.grid.is_in_grid(x + dx, y + dy):
                    new_grid[x + dx][y + dy] = True
                    if not self.populated_tiles[x + dx][y + dy]:
                        new_regions.add((x + dx, y + dy))

        for region in new_regions:
            self._spawn_in_tile(region)

        del self.populated_tiles
        self.populated_tiles = new_grid

    def _spawn_in_tile(self, region):
        dist_to_center = distance(region, (Constant.GRID_WIDTH//2, Constant.GRID_HEIGHT//2))
        world_x, world_y = region[0] * Constant.TILE_SIZE, region[1] * Constant.TILE_SIZE

        if self.grid.grid[region[0]][region[1]].type in {CellType.NATURE, CellType.ROAD} and dist_to_center > 4:
            zombies = 0
            if int(Constant.AVG_ZOMBIES_PER_TILE_DISTANCE_FROM_CENTER * dist_to_center) > 0:
                zombies = random.randint(0, int(Constant.AVG_ZOMBIES_PER_TILE_DISTANCE_FROM_CENTER * dist_to_center))
            blue_zombie = Constant.BLUE_ZOMBIE_PROB_INCREASE_PER_TILE_DISTANCE_FROM_CENTER * dist_to_center > random.random()
            dog = Constant.DOG_PROB_INCREASE_PER_TILE_DISTANCE_FROM_CENTER * dist_to_center > random.random()

            for _ in range(zombies):
                x, y = int(world_x + random.random() * Constant.TILE_SIZE), int(world_y + random.random() * Constant.TILE_SIZE)
                self.zombie_handler.add_zombie(Zombie(x, y, self))

            if blue_zombie:
                x, y = int(world_x + random.random() * Constant.TILE_SIZE), int(
                    world_y + random.random() * Constant.TILE_SIZE)
                self.zombie_handler.add_zombie(Zombie(x, y, self, is_super_zombie=True))

            if dog:
                x, y = int(world_x + random.random() * Constant.TILE_SIZE), int(
                    world_y + random.random() * Constant.TILE_SIZE)
                self.dog_handler.add_dog(Dog(x, y, self.player, self))





