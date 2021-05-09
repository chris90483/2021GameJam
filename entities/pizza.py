import pygame
from math import cos, sin, pi

from pygame import Surface

from main.util import distance

pizza_texture = pygame.image.load("./resources/png/pizza_inventory_icon.png")
pizza_texture = pygame.transform.scale(pizza_texture, (50, 50))
pizza_texture = pygame.transform.rotate(pizza_texture, -90)


class Pizza:

    def __init__(self, x, y, dist_to_mouse, angle, world):
        self.x = x
        self.y = y
        self.dist_to_mouse = dist_to_mouse
        # DOnt ASK QUESTIONS about the ANGLE or the SPEED
        self.angle = -angle
        self.speed = -10
        self.world = world

    def step(self):
        if self.dist_to_mouse < 0:
            return

        dx = cos(self.angle) * self.speed
        dy = sin(self.angle) * self.speed

        self.x += dx
        self.y += dy

        self.dist_to_mouse -= distance((0, 0), (dx, dy))

        # # Check whether we can move anywhere
        # if can_move_to(self.x + dx, self.y + dy, self.world.grid):
        #     self.x += dx
        #     self.y += dy
        # elif can_move_to(self.x + dx, self.y, self.world.grid):
        #     self.x += dx
        # elif can_move_to(self.x, self.y + dy, self.world.grid):
        #     self.y += dy

    def draw(self, screen: Surface, camera):
        rotated = pygame.transform.rotate(pizza_texture, -self.angle * (180.0 / pi))
        camera.blit_surface_to_screen(screen, rotated, self.x, self.y)

