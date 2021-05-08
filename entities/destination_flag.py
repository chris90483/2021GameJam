import pygame
from main.camera import Camera
from main.destination import Destination
from main.constants import Constant

class DestinationFlag(object):
    def __init__(self, destination, player):
        self.destination = destination
        self.player = player
        self.compass_image = pygame.image.load('./resources/png/compass.png')
        self.compass_image = pygame.transform.scale(self.compass_image, (50, 50))
        self.animation_counter = 0
        self.keyframes = []
        for x in range(1, 9):
            self.keyframes.append(pygame.transform.scale(pygame.image.load(
                "./resources/png/animations/destination/destination_" + str(x) + ".png"), (225, 225)))

    def draw(self, screen: pygame.Surface, camera: Camera):
        camera.blit_surface_to_screen(screen, self.keyframes[self.animation_counter // 10],
                                      self.destination.destination[0] * Constant.TILE_SIZE,
                                      self.destination.destination[1] * Constant.TILE_SIZE + Constant.TILE_SIZE * 0.25,
                                      centered=False)
        self.animation_counter = (self.animation_counter + 1) % (10 * len(self.keyframes))
