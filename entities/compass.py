import pygame
from pygame.event import EventType
from main.constants import Constant
from math import atan2, pi


class Compass(object):
    def __init__(self, destination, player):
        self.destination = destination
        self.player = player
        self.compass_image = pygame.image.load('./resources/png/compass.png')
        self.compass_image = pygame.transform.scale(self.compass_image, (50, 50))

    def draw(self, screen: pygame.Surface):
        player_pos = self.player.get_grid_position(False)
        angle = atan2(player_pos[0] - self.destination.destination[0], player_pos[1] - self.destination.destination[1])
        rotated = pygame.transform.rotate(self.compass_image, angle * (180.0/pi))
        screen.blit(rotated, (Constant.SCREEN_WIDTH - 100, 50))
