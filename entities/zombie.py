import random
from math import pi, atan2, cos, sin

import pygame
from pygame.surface import Surface

from audio.audio import SoundEmitter
from main.camera import Camera
from main.util import distance

zombie_texture = pygame.image.load("./resources/png/zombie_standing.png")


class Zombie(object):
    VISION_RANGE = 20.0
    SPEED = 2.0
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
            self.angle = atan2(self.y - self.target_pos[1], self.x - self.target_pos[0])
            self.speed = self.SPEED

        self.x += cos(self.angle) * self.SPEED
        self.y += sin(self.angle) * self.speed

    def draw(self, screen: Surface, camera: Camera):
        rotated = pygame.transform.rotate(zombie_texture, self.angle * (180.0/pi))
        camera.blit_surface_to_screen(screen, rotated, self.x, self.y)

    def hear(self, emitter: SoundEmitter):
        # TODO: Make this depend on loudness :)
        if distance((emitter.x, emitter.y), (self.x, self.y)) < 200:
            self.target_pos = (emitter.x, emitter.y)

