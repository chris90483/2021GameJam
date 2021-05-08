"""
    Defines all code for the player object
"""
from collections import defaultdict
from math import atan2, pi
from main.constants import Constant
import pygame
from pygame.event import EventType


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.held_keys = defaultdict(lambda: False)
        self.keyframes_walking = []
        self.keyframes_walking_animation_counter = 0
        for x in range(1, 6):
            self.keyframes_walking.append(
                pygame.image.load('./resources/png/animations/player/player_walking_' + str(x) + '.png'))

    def gen_texture(self):
        player_sprite = None
        if self.held_keys[pygame.K_w] or self.held_keys[pygame.K_s] or self.held_keys[pygame.K_a] or self.held_keys[pygame.K_d]:
            player_sprite = self.keyframes_walking[self.keyframes_walking_animation_counter // 5]
            self.keyframes_walking_animation_counter = \
                (self.keyframes_walking_animation_counter + 1) % (5 * len(self.keyframes_walking))
        else:
            player_sprite = pygame.image.load('./resources/png/player_standing.png')

        player_sprite = pygame.transform.rotate(player_sprite, 90)
        player_sprite = pygame.transform.scale(player_sprite, (50, 50))
        return player_sprite
        # texture = pygame.Surface((40, 40))
        # texture.fill((246, 1, 1), rect=(10, 10, 20, 20))
        # return texture

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
        self.angle = atan2(- (Constant.SCREEN_HEIGHT//2 - mouse_y), Constant.SCREEN_WIDTH//2 - mouse_x)

        # Silly Python has no switch case statement >:-(
        if self.held_keys[pygame.K_w]:
            self.y -= 10
        if self.held_keys[pygame.K_s]:
            self.y += 10
        if self.held_keys[pygame.K_a]:
            self.x -= 10
        if self.held_keys[pygame.K_d]:
            self.x += 10

    def draw(self, screen: pygame.Surface, camera):
        rotated = pygame.transform.rotate(self.gen_texture(), self.angle * (180.0/pi))
        camera.blit_surface_to_screen(screen, rotated, self.x, self.y)
