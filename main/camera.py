from pygame.surface import Surface

from entities.player import Player
from main.constants import Constant


class Camera(object):
    def __init__(self, player: Player):
        self.player = player

    def compute_screen_position(self, x, y):
        """
        Computes screen position given a world position using player's position
        :param x: World x coordinate
        :param y: World y coordinate
        :return: (screen_x, screen_y) and lots of love <3 Thanks Gerben love you too
        """
        screen_left_x = self.player.x - Constant.SCREEN_WIDTH // 2
        screen_top_y = self.player.y - Constant.SCREEN_HEIGHT // 2

        return x - screen_left_x, y - screen_top_y

    def is_in_screen(self, surface: Surface, x, y, centered=True):
        screen_x, screen_y = self.compute_screen_position(x, y)
        if centered:
            left_x, right_x = screen_x - surface.get_size()[0]//2, screen_x + surface.get_size()[0]//2
            top_y, bottom_y = screen_y - surface.get_size()[1]//2, screen_y + surface.get_size()[1]//2
        else:
            left_x, right_x = screen_x, screen_x + surface.get_size()[0]
            top_y, bottom_y = screen_y, screen_y + surface.get_size()[1]

        return bottom_y > 0 and top_y < Constant.SCREEN_HEIGHT and right_x > 0 and left_x < Constant.SCREEN_WIDTH, left_x, top_y

    def blit_surface_to_screen(self, screen: Surface, surface: Surface, x, y, centered=True):
        """
        Blits (draws) surface to the screen (if visible).
            The surface will be drawn such that its world coordinates are at the center of the surface
        :param centered: Whether the Surface is centered on the x,y or whether x,y is the top left (used for tiles)
        :param screen: The screen Surface
        :param surface: The surface to draw
        :param x: world x coordinate
        :param y: world y coordinate
        """
        in_screen, left_x, top_y = self.is_in_screen(surface, x, y, centered)
        if in_screen:
            screen.blit(surface, (left_x, top_y))
