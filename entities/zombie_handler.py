from pygame.surface import Surface

from entities.zombie import Zombie
from main.camera import Camera


class ZombieHandler(object):
    def __init__(self):
        self.zombies = []

        # TODO: Temporary spawn code
        self.add_zombie(Zombie(500, 500))

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
