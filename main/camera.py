from pygame.surface import Surface

from entities.player import Player


class Camera(object):
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    def __init__(self, player: Player):
        self.player = player

    def compute_screen_position(self, x, y):
        """
        Computes screen position given a world position using player's position
        :param x: World x coordinate
        :param y: World y coordinate
        :return: (screen_x, screen_y) and lots of love <3
        """
        screen_left_x = self.player.x - self.SCREEN_WIDTH // 2
        screen_top_y = self.player.y - self.SCREEN_HEIGHT // 2

        return x - screen_left_x, y - screen_top_y

    def blit_surface_to_screen(self, screen: Surface, surface: Surface, x, y):
        """
        Blits (draws) surface to the screen (if visible).
            The surface will be drawn such that its world coordinates are at the center of the surface
        :param screen: The screen Surface
        :param surface: The surface to draw
        :param x: world x coordinate
        :param y: world y coordinate
        """
        screen_x, screen_y = self.compute_screen_position(x, y)
        left_x, right_x = screen_x - surface.get_size()[0], screen_x + surface.get_size()[0]
        top_y, bottom_y = screen_y - surface.get_size()[1], screen_y + surface.get_size()[1]

        # Check if it is visible and draw if it is
        if bottom_y > 0 and top_y < self.SCREEN_HEIGHT and right_x > 0 and left_x < self.SCREEN_WIDTH:
            screen.blit(surface, (left_x, top_y))
