import pygame
from math import pi

class Flamethrower(object):

    def __init__(self, player):
        self.player = player
        self.fuel_left = 1000
        self.activated = False
        self.empty = False
        self.keyframes_fire_spitting_counter = 0
        self.keyframes_fire_spitting = []
        for x in range(1, 2):
            self.keyframes_fire_spitting.append(pygame.image.load("./resources/png/animations/flamethrower/fire_spitting_" + str(x) + ".png"))

        self.keyframes_empty_counter = 0
        self.keyframes_empty = []
        for x in range(1, 2):
            self.keyframes_empty.append(pygame.image.load("./resources/png/animations/flamethrower/empty_" + str(x) + ".png"))

    def toggle(self):
        self.activated = not self.activated

    def step(self):
        if self.activated and not self.empty:
            self.fuel_left -= 1
            if self.fuel_left < 1:
                self.empty = True

    def draw(self, screen: pygame.Surface, camera, angle):
        if self.activated:
            print("player.x: " + str(self.player.x) + " player.y: " + str(self.player.y))
            print("fuel left: " + str(self.fuel_left))