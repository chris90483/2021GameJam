import random
from math import pi, atan2, cos, sin

import pygame
from pygame.surface import Surface

from audio.audio import SoundEmitter
from main.camera import Camera
from main.util import distance

zombie_texture = pygame.image.load("./resources/png/zombie_standing.png")
zombie_texture = pygame.transform.scale(zombie_texture, (50, 50))
zombie_texture = pygame.transform.rotate(zombie_texture, -90)


class Zombie(object):
    VISION_RANGE = 100.0
    SPEED = 0.8

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.random() * 2 * pi
        self.speed = 0.0
        self.target_pos = None

    def step(self):
        if self.target_pos is None:
            return

        if distance((self.x, self.y), self.target_pos) < self.VISION_RANGE:
            self.angle += random.random() * 0.1 - 0.05
            self.speed = 0
        else:
            self.angle = atan2(self.target_pos[1] - self.y, self.target_pos[0] - self.x) + ((random.random()-0.5) * 0.05)
            self.speed = self.SPEED * (1.0 + random.random() * 0.1)

        self.x += cos(self.angle) * self.speed
        self.y += sin(self.angle) * self.speed

    def draw(self, screen: Surface, camera: Camera):
        rotated = pygame.transform.rotate(zombie_texture, -self.angle * (180.0/pi))
        camera.blit_surface_to_screen(screen, rotated, self.x, self.y)

    def hear(self, emitter: SoundEmitter):
        # TODO: Make this depend on loudness :)
        if distance((emitter.x, emitter.y), (self.x, self.y)) < 2000:
            self.target_pos = (emitter.x, emitter.y)

