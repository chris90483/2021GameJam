import random

from pygame.surface import Surface

from entities.zombie import Zombie
from main.camera import Camera
from main.constants import Constant
from main.grid import CellType


class ZombieHandler(object):

    CHANCE_FOR_SUPER_ZOMBIE = 0.1

    def __init__(self, world):
        self.zombies = set()
        self.world = world
        self.to_delete = set()

        for grid_x in range(Constant.GRID_WIDTH):
            for grid_y in range(Constant.GRID_HEIGHT):
                if world.grid.grid[grid_x][grid_y].type == CellType.NATURE:
                    for _ in range(1):
                        world_x, world_y = grid_x * Constant.TILE_SIZE, grid_y * Constant.TILE_SIZE
                        world_x += int(random.random() * Constant.TILE_SIZE)
                        world_y += int(random.random() * Constant.TILE_SIZE)
                        if random.random() < self.CHANCE_FOR_SUPER_ZOMBIE:
                            self.add_zombie(Zombie(world_x, world_y, world, is_super_zombie=True))
                        else:
                            self.add_zombie(Zombie(world_x, world_y, world, is_super_zombie=False))

        print("N zombies: ", len(self.zombies))

    def get_zombies(self):
        return self.zombies.copy()

    def add_zombie(self, zombie: Zombie):
        self.zombies.add(zombie)

    def step(self):
        for zombie in self.zombies:
            zombie.step()

        if len(self.to_delete) > 0:
            self.zombies -= self.to_delete
            self.to_delete.clear()

    def draw(self, screen: Surface, camera: Camera):
        for zombie in self.zombies:
            zombie.draw(screen, camera)

    def delete_zombie(self, zombie: Zombie):
        self.to_delete.add(zombie)
