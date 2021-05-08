import random

from pygame.surface import Surface

from entities.zombie import Zombie
from main.camera import Camera
from main.grid import CellType


class ZombieHandler(object):
    def __init__(self, world):
        self.zombies = []
        self.world = world

        for grid_x in range(len(world.grid.grid)):
            for grid_y in range(len(world.grid.grid[0])):
                if world.grid.grid[grid_x][grid_y].type == CellType.NATURE:
                    for _ in range(1):
                        world_x, world_y = grid_x * 256, grid_y * 256
                        world_x += int(random.random() * 256)
                        world_y += int(random.random() * 256)
                        self.add_zombie(Zombie(world_x, world_y))

        print("N zombies: ", len(self.zombies))



    def get_zombies(self):
        return self.zombies[:]

    def add_zombie(self, zombie: Zombie):
        self.zombies.append(zombie)

    def step(self):
        for zombie in self.zombies:
            zombie.step()

    def draw(self, screen: Surface, camera: Camera):
        for zombie in self.zombies:
            zombie.draw(screen, camera)
