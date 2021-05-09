import random
from math import pi, atan2, cos, sin

import pygame
from pygame.surface import Surface

from audio.audio import SoundEmitter
from audio.sound_emitter import Footstep
from entities import player
from main import constants
from main.camera import Camera
from main.constants import Constant
from main.util import distance, convert_world_to_grid_position, can_move_to

zombie_texture = pygame.image.load("./resources/png/zombie_standing.png")
zombie_texture = pygame.transform.scale(zombie_texture, (50, 50))
zombie_texture = pygame.transform.rotate(zombie_texture, -90)
pygame.font.init()
paused_font = pygame.font.SysFont("Arial", 50)
exclamation_mark = paused_font.render('!', True, (200, 200, 0))
is_collision = False


class Zombie(object):
    VISION_RANGE = 30.0

    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.angle = random.random() * 2 * pi
        self.speed = 0.0
        self.max_speed = random.random() * Constant.MAX_ZOMBIE_SPEED
        self.target = None
        self.angery = False
        self.world = world
        self.is_colliding = False

    def step(self):
        if self.target is None:
            return

        if distance((self.x, self.y), (self.target.x, self.target.y)) < self.VISION_RANGE:
            self.angle = atan2(self.target.y - self.y, self.target.x - self.x) + (
                    (random.random() - 0.5) * 0.05)
            self.speed = 0
            self.angery = False
            self.target = None
        else:
            self.angle = atan2(self.target.y - self.y, self.target.x - self.x) + (
                    (random.random() - 0.5) * 0.05)
            self.speed = self.max_speed * (1.0 + random.random() * 0.1)

        dx = cos(self.angle) * self.speed
        dy = sin(self.angle) * self.speed

        # Check whether we can move anywhere
        if can_move_to(self.x + dx, self.y + dy, self.world.grid):
            self.x += dx
            self.y += dy
        elif can_move_to(self.x + dx, self.y, self.world.grid):
            self.x += dx
        elif can_move_to(self.x, self.y + dy, self.world.grid):
            self.y += dy

        self.check_collision()

    def draw(self, screen: Surface, camera: Camera):
        rotated = pygame.transform.rotate(zombie_texture, -self.angle * (180.0 / pi))
        if self.is_colliding:
            rotated.fill((0, 0, 0))
        camera.blit_surface_to_screen(screen, rotated, self.x, self.y)
        if self.target is not None:
            camera.blit_surface_to_screen(screen, exclamation_mark, self.x, self.y - 30.0)

    def hear(self, emitter: SoundEmitter):
        if emitter.get_loudness_at_position(self.x, self.y) >= 1.0:
            if self.target is None or self.target.timestamp < emitter.timestamp or \
                    (isinstance(emitter, Footstep) and not isinstance(self.target, Footstep)):
                self.target = emitter
                self.angery = True

    def check_collision(self):
        self.is_colliding = distance((self.world.player.x, self.world.player.y), (self.x, self.y)) <= 50
        if self.is_colliding:
            self.world.player.take_damage(1)
