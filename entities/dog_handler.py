from pygame.surface import Surface

from entities.dog import Dog
from main.camera import Camera
from main.constants import Constant


class DogHandler(object):
    def __init__(self, world):
        self.player = world.player
        self.world = world
        self.dogs = set()
        self.to_delete = set()

    def get_dogs(self):
        return self.dogs[:]

    def add_dog(self, dog: Dog):
        self.dogs.add(dog)

    def step(self):
        for dog in self.dogs:
            dog.step()

        if len(self.to_delete) > 0:
            self.dogs -= self.to_delete
            self.to_delete.clear()

    def draw(self, screen: Surface, camera: Camera):
        for dog in self.dogs:
            dog.draw(screen, camera)

    def delete_dog(self, dog: Dog):
        self.to_delete.add(dog)
