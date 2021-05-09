import random
from enum import Enum
from math import pi, atan2, cos, sin

import pygame
from pygame.surface import Surface

from audio.audio import SoundEmitter
from audio.sound_emitter import Footstep, PlayerSoundEmitter
from main import constants
from main.camera import Camera
from main.constants import Constant
from main.util import distance, convert_world_to_grid_position, can_move_to

zombie_texture = pygame.image.load("./resources/png/zombie_standing.png")
zombie_texture = pygame.transform.scale(zombie_texture, (50, 50))
zombie_texture = pygame.transform.rotate(zombie_texture, -90)

super_zombie_texture = pygame.image.load("./resources/png/blue_zombie_standing.png")
super_zombie_texture = pygame.transform.scale(super_zombie_texture, (50, 50))
super_zombie_texture = pygame.transform.rotate(super_zombie_texture, -90)

pygame.font.init()
state_indicator_font = pygame.font.SysFont("Arial", 35)
marker_yellow = state_indicator_font.render('?', True, (200, 200, 0))
marker_red = state_indicator_font.render('!', True, (200, 0, 0))


class LostPlayerEntity(object):
    """
    Used when the Zombie was directly engaging the player, but lost range
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


class ZombieState(Enum):
    IDLE = 0,  # Zombie walks around randomly, looking for brainzzzz
    REACTING_TO_NOISE = 1,  # Zombie has hear a noise that may indicate the presence of brains and walks towards it
    ATTACKING_PLAYER = 2  # Zombie is close enough to the player to attack and keep following


class Zombie(object):
    VISION_RANGE = 150.0

    def __init__(self, x, y, world, is_super_zombie=False):
        self.is_super_zombie = is_super_zombie

        self.x = x
        self.y = y
        self.angle = random.random() * 2 * pi
        self.speed = 0.0
        self.max_speed = 0.5 + 0.5 * random.random() * Constant.MAX_ZOMBIE_SPEED
        if is_super_zombie:
            self.max_speed * 5
        self.target = None
        self.state = ZombieState.IDLE
        self.world = world
        self.is_colliding = False

    def step(self):
        if self.target is not None:
            if distance((self.x, self.y), (self.world.player.x, self.world.player.y)) < self.VISION_RANGE:
                self.state = ZombieState.ATTACKING_PLAYER
                self.target = self.world.player
            elif distance((self.x, self.y), (self.target.x, self.target.y)) > self.VISION_RANGE:
                if self.state == ZombieState.ATTACKING_PLAYER:
                    # We've lost the player, got to last known location until sound overrides this
                    self.target = LostPlayerEntity(self.target.x, self.target.y)
                self.state = ZombieState.REACTING_TO_NOISE

            if distance((self.x, self.y), (self.target.x, self.target.y)) < self.max_speed:
                if self.state == ZombieState.ATTACKING_PLAYER:
                    self.speed = 0
                if self.state == ZombieState.REACTING_TO_NOISE:
                    self.state = ZombieState.IDLE
                    self.target = None

                self.angle = random.random() * 2 * pi

        if self.state == ZombieState.IDLE:
            self.angle = self.angle + (
                    (random.random() - 0.5) * 0.05)
            self.speed = self.max_speed * (0.2 + random.random() * 0.1)
        else:
            self.angle = atan2(self.target.y - self.y, self.target.x - self.x) + (
                    (random.random() - 0.5) * 0.05)
            if self.is_super_zombie:
                self.speed = self.max_speed * (3.0 + random.random() * 0.1)
            else:
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

        if self.state == ZombieState.IDLE and not can_move_to(self.x + dx, self.y + dy, self.world.grid):
            self.angle = random.random() * 2 * pi

        # De-spawn the zombie when out of range
        gx, gy = convert_world_to_grid_position(self.x, self.y)
        pgx, pgy = convert_world_to_grid_position(self.world.player.x, self.world.player.y)
        if abs(gx - pgx) > Constant.GRID_SPAWN_RANGE or abs(gy - pgy) > Constant.GRID_SPAWN_RANGE:
            self.world.zombie_handler.delete_zombie(self)

        self.check_collision()

    def draw(self, screen: Surface, camera: Camera):
        if self.is_super_zombie:
            texture = super_zombie_texture
        else:
            texture = zombie_texture
        rotated = pygame.transform.rotate(texture, -self.angle * (180.0 / pi))
        if self.is_colliding:
            rotated.fill((0, 0, 0))
        camera.blit_surface_to_screen(screen, rotated, self.x, self.y)
        if self.state == ZombieState.REACTING_TO_NOISE:
            camera.blit_surface_to_screen(screen, marker_yellow, self.x, self.y - 30.0)
        elif self.state == ZombieState.ATTACKING_PLAYER:
            camera.blit_surface_to_screen(screen, marker_red, self.x, self.y - 30.0)

    def hear(self, emitter: SoundEmitter):
        if not self.state == ZombieState.ATTACKING_PLAYER:
            if emitter.get_loudness_at_position(self.x, self.y) >= 1.0:
                if self.state == ZombieState.IDLE \
                        or not isinstance(self.target, SoundEmitter) \
                        or self.target.timestamp < emitter.timestamp \
                        or (isinstance(emitter, PlayerSoundEmitter) and not isinstance(self.target, PlayerSoundEmitter)):
                    self.target = emitter
                    self.state = ZombieState.REACTING_TO_NOISE

    def check_collision(self):
        self.is_colliding = distance((self.world.player.x, self.world.player.y), (self.x, self.y)) <= 50
        if self.is_colliding:
            self.world.player.take_damage(1)
