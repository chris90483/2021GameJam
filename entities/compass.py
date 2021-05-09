import pygame
from pygame.event import EventType
from main.constants import Constant
from main.camera import Camera
from math import atan2, pi


class Compass(object):
    def __init__(self, world):
        self.destination = world.destination
        self.destination_flag = world.destination_flag
        self.player = world.player
        self.compass_image = pygame.image.load('./resources/png/compass.png')
        self.compass_image = pygame.transform.scale(self.compass_image, (50, 50))

    def draw(self, screen: pygame.Surface, camera: Camera):
        player_pos = self.player.get_grid_position(False)
        angle = atan2(player_pos[0] - self.destination.destination[0], player_pos[1] - self.destination.destination[1])
        rotated = pygame.transform.rotate(self.compass_image, angle * (180.0/pi))
        if not camera.is_in_screen(self.destination_flag.keyframes[0],
                               self.destination.destination[0] * Constant.TILE_SIZE,
                               self.destination.destination[1] * Constant.TILE_SIZE)[0]:
            destination_screen_x, destination_screen_y = camera.compute_screen_position(
                self.destination.destination[0] * Constant.TILE_SIZE, self.destination.destination[1] * Constant.TILE_SIZE)
            compass_x = min(Constant.SCREEN_WIDTH - 100, max(50, destination_screen_x))
            compass_y = min(Constant.SCREEN_HEIGHT - 100, max(50, destination_screen_y))
            screen.blit(rotated, (compass_x, compass_y))
