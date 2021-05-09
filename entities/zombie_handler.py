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
