import random
from math import pi, atan2, cos, sin

import pygame
from pygame.surface import Surface

from audio.audio import SoundEmitter
from audio.sound_emitter import DogBark
from main.camera import Camera
from main.util import distance, can_move_to

dog_texture = pygame.image.load("./resources/png/dog.png")
dog_texture = pygame.transform.scale(dog_texture, (50, 50))
dog_texture = pygame.transform.rotate(dog_texture, -90)

dog_keyframes = [pygame.image.load("./resources/png/animations/dog/dog_" + str(x) + ".png") for x in range(1, 3)]

class Dog(object):
    VISION_RANGE = 500.0
    FOLLOW_RANGE = 250.0
    SPEED = 7.5

    def __init__(self, x, y, player, world):
        self.player = player
        self.world = world
        self.x = x
        self.y = y
        self.angle = random.random() * 2 * pi
        self.speed = 0.0
        self.target_pos = (self.player.x, self.player.y)
        self.following_player = False
        self.eating_pizza = False

        self.keyframes_counter = 0
        self.bark_delay_counter = 0
        self.current_bark_delay = random.randint(200, 300)

    def step(self):
        self.target_pos = (self.player.x, self.player.y)

        dx = 0
        dy = 0
        # TODO: Bark every 2-6 seconds?
        if self.following_player:
            self.bark_delay_counter += 1
            if self.bark_delay_counter % self.current_bark_delay == 0:
                self.world.emitter_handler.add_emitter(DogBark(self.x, self.y))
                self.current_bark_delay = random.randint(200, 300)

        if distance((self.x, self.y), self.target_pos) < self.FOLLOW_RANGE:
            return

        if distance((self.x, self.y), self.target_pos) < self.VISION_RANGE:
            self.following_player = True
            self.angle = atan2(self.target_pos[1] - self.y, self.target_pos[0] - self.x) + (
                    (random.random() - 0.5) * 0.05)
            self.speed = self.SPEED * (1.0 + random.random() * 0.1)

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

    def draw(self, screen: Surface, camera: Camera):
        if self.speed > 0.0:

            rotated = pygame.transform.rotate(dog_keyframes[self.keyframes_counter // 5], -self.angle * (180.0 / pi))
            self.keyframes_counter = (self.keyframes_counter + 1) % (5 * len(dog_keyframes))
            camera.blit_surface_to_screen(screen, rotated, self.x, self.y)
        else:
            rotated = pygame.transform.rotate(dog_texture, -self.angle * (180.0 / pi))
            camera.blit_surface_to_screen(screen, rotated, self.x, self.y)

    def hear(self, emitter: SoundEmitter):
        # TODO: Make this depend on loudness :)
        if distance((emitter.x, emitter.y), (self.x, self.y)) < 2000:
            self.target_pos = (emitter.x, emitter.y)
