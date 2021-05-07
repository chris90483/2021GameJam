"""
    Defines all code for the player object
"""
from collections import defaultdict
from math import atan2, pi

import pygame
from pygame.event import EventType


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.held_keys = defaultdict(lambda: False)
        self.texture = self.gen_texture()

    def gen_texture(self):
        texture = pygame.Surface((40, 40))
        texture.fill((246, 1, 1), rect=(10, 10, 20, 20))
        return texture

    def handle_input(self, event: EventType):
        """
        Handles a single pygame event. Is used for detecting WASD input
        :param event: pygame event
        """
        if event.type == pygame.KEYDOWN:
            self.held_keys[event.key] = True

        elif event.type == pygame.KEYUP:
            self.held_keys[event.key] = False

    def step(self):
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = atan2(- (self.y - mouse_y), self.x - mouse_x)

        # Silly Python has no switch case statement >:-(
        if self.held_keys[pygame.K_w]:
            self.y -= 10
        if self.held_keys[pygame.K_s]:
            self.y += 10
        if self.held_keys[pygame.K_a]:
            self.x -= 10
        if self.held_keys[pygame.K_d]:
            self.x += 10

    def draw(self, screen: pygame.Surface):
        rotated = pygame.transform.rotate(self.texture, self.angle * (180.0/pi))
        surf_w, surf_h = rotated.get_size()
        screen.blit(rotated, (self.x - surf_w//2, self.y - surf_h//2))
