import random
from math import pi, atan2, cos, sin

import pygame
from pygame.surface import Surface

from audio.audio import SoundEmitter, SFX
from audio.sound_emitter import DogBark
from main.camera import Camera
from main.constants import Constant
from main.util import distance, can_move_to, convert_world_to_grid_position

dog_texture = pygame.image.load("./resources/png/dog.png")
dog_texture = pygame.transform.scale(dog_texture, (50, 50))
dog_texture = pygame.transform.rotate(dog_texture, -90)

dog_keyframes = [pygame.image.load("./resources/png/animations/dog/dog_" + str(x) + ".png") for x in range(1, 7)]


class Dog(object):

    PIZZA_VISION_RANGE = 1000.0
    PIZZA_EATING_RANGE = 5.0
    VISION_RANGE = 500.0
    FOLLOW_RANGE = 250.0
    GROWL_RANGE = 2000.0

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
        self.following_pizza = False

        self.pizza_health = 100

        self.keyframes_counter = 0
        self.bark_delay_counter = 0
        self.growl_delay_counter = 0
        self.current_bark_delay = random.randint(200, 300)
        self.current_growl_delay = random.randint(200, 300)

    def step(self):
        # print(self.world.pizza)
        # print("Follow player ", self.following_player)
        # print("Follow pizza ", self.following_pizza)
        # print("Eating pizza ", self.eating_pizza)
        if not self.eating_pizza and not self.following_pizza:
            self.target_pos = (self.player.x, self.player.y)

        if self.world.pizza:
            if distance((self.x, self.y), (self.world.pizza.x, self.world.pizza.y)) < self.PIZZA_VISION_RANGE:
                self.target_pos = (self.world.pizza.x, self.world.pizza.y)
                self.following_pizza = True
                self.following_player = False

        if not self.following_player and distance((self.x, self.y), (self.player.x, self.player.y)) < self.GROWL_RANGE:
            self.growl_delay_counter += 1
            if self.growl_delay_counter % self.current_growl_delay == 0:
                player_distance = distance((self.x, self.y), (self.player.x, self.player.y))
                magic_number = 1000
                sound_factor = magic_number/player_distance
                if sound_factor > 2:
                    sound_factor = 2
                self.world.audio_manager.play_sfx(SFX.DOG_GROWL, sound_factor=sound_factor)
                self.current_growl_delay = random.randint(200, 300)
                self.growl_delay_counter = 0

        # De-spawn the dog when out of range
        gx, gy = convert_world_to_grid_position(self.x, self.y)
        pgx, pgy = convert_world_to_grid_position(self.player.x, self.player.y)
        if abs(gx - pgx) > Constant.GRID_SPAWN_RANGE or abs(gy - pgy) > Constant.GRID_SPAWN_RANGE:
            self.world.dog_handler.delete_dog(self)

        dx = 0
        dy = 0
        # TODO: Bark every 2-6 seconds?
        if self.following_player:
            self.bark_delay_counter += 1
            if self.bark_delay_counter % self.current_bark_delay == 0:
                # TODO: Play bark sound
                self.world.audio_manager.play_sfx(SFX.DOG_BARK)
                self.world.emitter_handler.add_emitter(DogBark(self.x, self.y))
                self.current_bark_delay = random.randint(200, 300)

        if not self.following_pizza and distance((self.x, self.y), self.target_pos) < self.FOLLOW_RANGE:
            self.speed = 0.0
            return

        if self.following_pizza and distance((self.x, self.y), self.target_pos) < self.PIZZA_EATING_RANGE:
            self.eating_pizza = True

        if self.eating_pizza:
            self.pizza_health -= 1
            if self.pizza_health < 0:
                self.world.pizza = None
                self.eating_pizza = False
                self.following_pizza = False
                self.pizza_health = 20
                self.target_pos = (self.player.x, self.player.y)
            else:
                return

        # print(not self.following_pizza, not self.eating_pizza, distance((self.x, self.y), self.target_pos) < self.VISION_RANGE)

        if not self.following_pizza and not self.eating_pizza and distance((self.x, self.y), self.target_pos) < self.VISION_RANGE:
            self.following_player = True
            self.angle = atan2(self.target_pos[1] - self.y, self.target_pos[0] - self.x) + (
                    (random.random() - 0.5) * 0.05)
            self.speed = self.SPEED * (1.0 + random.random() * 0.1)

            dx = cos(self.angle) * self.speed
            dy = sin(self.angle) * self.speed

            # print("moving", dx, dy)

        if self.following_pizza and self.world.pizza:
            self.angle = atan2(self.world.pizza.y - self.y, self.world.pizza.x - self.x) + (
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
        scaled = pygame.transform.scale(dog_keyframes[self.keyframes_counter // 5], (100, 100))
        rotated = pygame.transform.rotate(scaled, -self.angle * (180.0 / pi) + 90)
        self.keyframes_counter = (self.keyframes_counter + 1) % (5 * len(dog_keyframes))
        camera.blit_surface_to_screen(screen, rotated, self.x, self.y)

    def hear(self, emitter: SoundEmitter):
        # TODO: Make this depend on loudness :)
        if distance((emitter.x, emitter.y), (self.x, self.y)) < 2000:
            self.target_pos = (emitter.x, emitter.y)
