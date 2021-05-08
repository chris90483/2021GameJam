"""
    Defines all code for the player object
"""
from collections import defaultdict
from math import atan2, pi, sqrt
from audio.sound_emitter import Footstep
from main.constants import Constant
import pygame
from pygame.event import EventType
from main.grid import CellType


class Player(object):
    def __init__(self, grid, world):
        self.grid = grid
        self.angle = 0
        self.held_keys = defaultdict(lambda: False)
        self.keyframes_walking = []
        self.keyframes_walking_animation_counter = 0
        self.moving = False
        for x in range(1, 6):
            self.keyframes_walking.append(
                pygame.image.load('./resources/png/animations/player/player_walking_' + str(x) + '.png'))

        for delta_x, delta_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x = self.grid.doominos_location[0] + delta_x
            y = self.grid.doominos_location[1] + delta_y
            if self.grid.grid[x][y].type == CellType.ROAD:
                self.x = x * Constant.TILE_SIZE
                self.y = y * Constant.TILE_SIZE
                break
        self.world = world
        self.step_no = 0

    def gen_texture(self):
        if self.moving:
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
        self.angle = atan2(- (Constant.SCREEN_HEIGHT // 2 - mouse_y), Constant.SCREEN_WIDTH // 2 - mouse_x)
        moving = False

        speed = Constant.PLAYER_SPEED
        player_pos = self.get_grid_position()
        if self.grid.grid[player_pos[0]][player_pos[1]].type == CellType.NATURE:
            speed *= Constant.PLAYER_SPEED_GRASS_MULTIPLIER

        if self.held_keys[pygame.K_LSHIFT]:
            speed *=  Constant.PLAYER_SPEED_SLOW_WALKING_MULTIPLIER

        # Silly Python has no switch case statement >:-(
        delta_x = 0
        delta_y = 0
        if self.held_keys[pygame.K_w] or self.held_keys[pygame.K_UP]:
            delta_y -= speed
        if self.held_keys[pygame.K_s] or self.held_keys[pygame.K_DOWN]:
            delta_y += speed
        if self.held_keys[pygame.K_a] or self.held_keys[pygame.K_LEFT]:
            delta_x -= speed
        if self.held_keys[pygame.K_d] or self.held_keys[pygame.K_RIGHT]:
            delta_x += speed

        if delta_x != 0 and delta_y != 0:
            delta_x /= sqrt(2)
            delta_y /= sqrt(2)

        new_grid_x = (self.x + delta_x + Constant.TILE_SIZE * 0.5) // Constant.TILE_SIZE
        new_grid_y = (self.y + delta_y + Constant.TILE_SIZE * 0.5) // Constant.TILE_SIZE
        if (delta_x != 0 or delta_y != 0) and \
                self.grid.grid[int(new_grid_x)][int(new_grid_y)].type not in [CellType.BUILDING, CellType.DOOMINOS] and \
                new_grid_x >= 0 and new_grid_y >= 0 and new_grid_x <= Constant.GRID_WIDTH and new_grid_y <= Constant.GRID_HEIGHT:
            self.x += delta_x
            self.y += delta_y
            self.moving = True
        else:
            self.moving = False

        self.step_no += 1

        if self.step_no % 15 == 0 and self.moving:
            self.world.emitter_handler.add_emitter(Footstep(self.x, self.y))

    def draw(self, screen: pygame.Surface, camera):
        rotated = pygame.transform.rotate(self.gen_texture(), self.angle * (180.0 / pi))
        camera.blit_surface_to_screen(screen, rotated, self.x, self.y)

    def get_grid_position(self, as_int=True):
        """
        Return the coordinates of the grid cell the player is currently in
        :param as_int: should the coordinates be returned as integers (default) or floats
        :return: tuple of x,y coordinates
        """
        if as_int:
            return (
                int((self.x + Constant.TILE_SIZE // 2) // Constant.TILE_SIZE),
                int((self.y + Constant.TILE_SIZE // 2) // Constant.TILE_SIZE),
            )
        else:
            return (
                (self.x + Constant.TILE_SIZE / 2) / Constant.TILE_SIZE,
                (self.y + Constant.TILE_SIZE / 2) / Constant.TILE_SIZE,
            )