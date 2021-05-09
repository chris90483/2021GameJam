from pygame.surface import Surface

from entities.dog import Dog
from main.camera import Camera
from main.constants import Constant


class DogHandler(object):
    def __init__(self, world):
        self.player = world.player
        self.world = world
        self.dogs = []

        # TODO: Temporary spawn code
        self.add_dog(Dog(Constant.GRID_HEIGHT*Constant.TILE_SIZE/2, Constant.GRID_HEIGHT*Constant.TILE_SIZE/2,
                         self.player, self.world))

    def get_dogs(self):
        return self.dogs[:]

    def add_dog(self, dog: Dog):
        self.dogs.append(dog)

    def step(self):
        for dog in self.dogs:
            dog.step()

    def draw(self, screen: Surface, camera: Camera):
        for dog in self.dogs:
            dog.draw(screen, camera)
