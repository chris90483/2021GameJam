"""
    Defines all code for the player object
"""
import sys
from collections import defaultdict
from math import atan2, pi, sqrt

from audio.audio import SFX
from audio.sound_emitter import Footstep
from entities.pizza import Pizza
from main.constants import Constant
import pygame
from pygame.event import EventType
from main.grid import CellType
from main.util import distance
from main.inventory import Inventory, InventoryItem


class Player(object):
    def __init__(self, world, audio_manager):
        self.audio_manager = audio_manager
        self.grid = world.grid
        self.angle = 0
        self.held_keys = defaultdict(lambda: False)
        self.keyframes_walking = []
        self.keyframes_walking_holding_knife = []
        self.keyframes_knife_attacking = []
        self.keyframes_knife_attacking_counter = 0
        self.keyframes_walking_animation_counter = 0
        self.moving = False
        self.moving_sound = None
        self.health = Constant.PLAYER_HEALTH
        for x in range(1, 6):
            self.keyframes_walking.append(
                pygame.image.load('./resources/png/animations/player/player_walking_' + str(x) + '.png'))
        for x in range(1, 6):
            self.keyframes_walking_holding_knife.append(
                pygame.image.load('./resources/png/animations/player/player_walking_holding_knife_' + str(x) + '.png'))
        for x in range(1, 7):
            self.keyframes_knife_attacking.append(
                pygame.image.load('./resources/png/animations/player/player_knife_attacking_' + str(x) + '.png'))
        self.set_start_location()
        self.world = world
        self.step_no = 0

    def set_start_location(self):
        for delta_x, delta_y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x = self.grid.doominos_location[0] + delta_x
            y = self.grid.doominos_location[1] + delta_y
            if self.grid.grid[x][y].type == CellType.ROAD:
                self.x = x * Constant.TILE_SIZE + Constant.TILE_SIZE//2
                self.y = y * Constant.TILE_SIZE + Constant.TILE_SIZE//2
                break

    def gen_texture(self):
        player_sprite = pygame.image.load('./resources/png/player_standing.png')

        player_sprite = pygame.transform.rotate(player_sprite, 90)
        player_sprite = pygame.transform.scale(player_sprite, (50, 50))

        if self.moving:
            if self.world.inventory.items[self.world.inventory.current_item]:
                if not self.world.inventory.items[0].activated and not self.world.inventory.items[self.world.inventory.current_item].item_type in [InventoryItem.SKATEBOARD, InventoryItem.PIZZA, InventoryItem.KNIFE]:
                    player_sprite = self.keyframes_walking[self.keyframes_walking_animation_counter // 5]
                    self.keyframes_walking_animation_counter = \
                        (self.keyframes_walking_animation_counter + 1) % (5 * len(self.keyframes_walking))

                    player_sprite = pygame.transform.rotate(player_sprite, 90)
                    player_sprite = pygame.transform.scale(player_sprite, (50, 50))
                elif self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.SKATEBOARD:
                    player_sprite = pygame.image.load('./resources/png/player_skateboarding.png')
                    player_sprite = pygame.transform.scale(player_sprite, (50, 75))
                    player_sprite = pygame.transform.rotate(player_sprite, 90)

                elif self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.PIZZA:
                    player_sprite = pygame.image.load('./resources/png/player_holding_pizza.png')
                    player_sprite = pygame.transform.scale(player_sprite, (50, 100))
                    player_sprite = pygame.transform.rotate(player_sprite, 90)
                elif self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.KNIFE:
                    if self.world.inventory.items[self.world.inventory.current_item].activated:
                        player_sprite = self.keyframes_knife_attacking[self.keyframes_knife_attacking_counter // 3]
                        self.keyframes_knife_attacking_counter = \
                            (self.keyframes_knife_attacking_counter + 1) % (3 * len(self.keyframes_knife_attacking))
                        if self.keyframes_knife_attacking_counter == 0:
                            self.world.inventory.items[self.world.inventory.current_item].activated = False
                        player_sprite = pygame.transform.scale(player_sprite, (50, 100))
                    else:
                        player_sprite = self.keyframes_walking_holding_knife[self.keyframes_walking_animation_counter // 5]
                        self.keyframes_walking_animation_counter = \
                            (self.keyframes_walking_animation_counter + 1) % (5 * len(self.keyframes_walking))
                        player_sprite = pygame.transform.scale(player_sprite, (50, 80))

                    player_sprite = pygame.transform.rotate(player_sprite, 90)

                elif self.world.inventory.items[0].activated:
                    if not self.world.inventory.items[0].empty:
                        player_sprite = self.world.inventory.items[0].keyframes_fire_spitting[
                            self.world.inventory.items[0].keyframes_fire_spitting_counter // 5]
                        self.world.inventory.items[0].keyframes_fire_spitting_counter = \
                            (self.world.inventory.items[0].keyframes_fire_spitting_counter + 1) \
                            % (5 * len(self.world.inventory.items[0].keyframes_fire_spitting))
                    else:
                        player_sprite = self.world.inventory.items[0].keyframes_empty[
                            self.world.inventory.items[0].keyframes_empty_counter // 5]
                        self.world.inventory.items[0].keyframes_empty_counter = \
                            (self.world.inventory.items[0].keyframes_empty_counter + 1) \
                            % (5 * len(self.world.inventory.items[0].keyframes_empty))
                    player_sprite = pygame.transform.rotate(player_sprite, 90)
                    player_sprite = pygame.transform.scale(player_sprite, (450, 100))
            else:
                player_sprite = self.keyframes_walking[self.keyframes_walking_animation_counter // 5]
                self.keyframes_walking_animation_counter = \
                    (self.keyframes_walking_animation_counter + 1) % (5 * len(self.keyframes_walking))

                player_sprite = pygame.transform.rotate(player_sprite, 90)
                player_sprite = pygame.transform.scale(player_sprite, (50, 50))
        else: # not self.moving
            if self.world.inventory.current_item == 0 and not self.world.inventory.items[0].activated:
                player_sprite = pygame.image.load('./resources/png/player_holding_flamethrower.png')

                player_sprite = pygame.transform.rotate(player_sprite, 90)
                player_sprite = pygame.transform.scale(player_sprite, (149, 50))

            elif self.world.inventory.items[0].activated:
                if not self.world.inventory.items[0].empty:
                    player_sprite = self.world.inventory.items[0].keyframes_fire_spitting[
                        self.world.inventory.items[0].keyframes_fire_spitting_counter // 5]
                    self.world.inventory.items[0].keyframes_fire_spitting_counter = \
                        (self.world.inventory.items[0].keyframes_fire_spitting_counter + 1) \
                        % (5 * len(self.world.inventory.items[0].keyframes_fire_spitting))
                else:
                    player_sprite = self.world.inventory.items[0].keyframes_empty[
                        self.world.inventory.items[0].keyframes_empty_counter // 5]
                    self.world.inventory.items[0].keyframes_empty_counter = \
                        (self.world.inventory.items[0].keyframes_empty_counter + 1) \
                        % (5 * len(self.world.inventory.items[0].keyframes_empty))
                player_sprite = pygame.transform.rotate(player_sprite, 90)
                player_sprite = pygame.transform.scale(player_sprite, (450, 100))
            elif self.world.inventory.items[self.world.inventory.current_item]:
                if self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.SKATEBOARD:
                    player_sprite = pygame.image.load('./resources/png/player_skateboarding.png')
                    player_sprite = pygame.transform.scale(player_sprite, (50, 75))
                elif self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.PIZZA:
                    player_sprite = pygame.image.load('./resources/png/player_holding_pizza.png')
                    player_sprite = pygame.transform.scale(player_sprite, (50, 100))

                elif self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.KNIFE:
                    if self.world.inventory.items[self.world.inventory.current_item].activated:
                        player_sprite = self.keyframes_knife_attacking[self.keyframes_knife_attacking_counter // 3]
                        self.keyframes_knife_attacking_counter = \
                            (self.keyframes_knife_attacking_counter + 1) % (3 * len(self.keyframes_knife_attacking))
                        if self.keyframes_knife_attacking_counter == 0:
                            self.world.inventory.items[self.world.inventory.current_item].activated = False
                        player_sprite = pygame.transform.scale(player_sprite, (50, 100))
                    else:
                        player_sprite = pygame.image.load('./resources/png/player_holding_knife.png')
                        player_sprite = pygame.transform.scale(player_sprite, (50, 100))
                else:
                    player_sprite = pygame.image.load('./resources/png/player_standing.png')
                    player_sprite = pygame.transform.scale(player_sprite, (50, 50))

                player_sprite = pygame.transform.rotate(player_sprite, 90)

        return player_sprite

    def handle_input(self, event: EventType):
        """
        Handles a single pygame event. Is used for detecting WASD input
        :param event: pygame event
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.world.inventory.items[self.world.inventory.current_item]:
                # Activate flamethrower
                if self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.FLAMETHROWER:
                    self.world.inventory.items[self.world.inventory.current_item].activated = True

                # Throw away pizza
                if self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.PIZZA:
                    self.world.destination.set_mission_to_go_to_doominos()
                    self.world.inventory.remove_item(InventoryItem.PIZZA)
                    self.throw_pizza(pygame.mouse.get_pos())
                    self.world.score.decrement_score(10)

                # Knife
                if self.world.inventory.items[self.world.inventory.current_item] and self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.KNIFE:
                    already_activated = self.world.inventory.items[self.world.inventory.current_item].activated
                    self.world.inventory.items[self.world.inventory.current_item].activated = True
                    if already_activated != self.world.inventory.items[self.world.inventory.current_item].activated:
                        self.world.audio_manager.play_sfx(SFX.KNIFE_SWISH)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.world.inventory.items[self.world.inventory.current_item]:
                # Deactivate flamethrower
                if self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.FLAMETHROWER:
                    self.world.inventory.items[self.world.inventory.current_item].activated = False
                if self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.PIZZA:
                    pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                pass
                # self.world.inventory.items[0].toggle()
            else:
                self.held_keys[event.key] = True

        elif event.type == pygame.KEYUP:
            self.held_keys[event.key] = False

    def throw_pizza(self, location):
        player_location_on_screen = Constant.SCREEN_WIDTH / 2, Constant.SCREEN_HEIGHT / 2
        dist_player_to_mouse = distance(player_location_on_screen, location)

        self.world.pizza = Pizza(self.x, self.y, dist_player_to_mouse, self.angle, self.world)

        # if self.world.destination.delivery_time is None:
        #     print("You don't have a pizza, why tf you trynna throw one?")
        # else:
        #     self.world.destination.delivery_time = None
        #     self.world.destination = self.grid.doominos_location
        #     self.world.destination_doominos = True

    def step(self):
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = atan2(- (Constant.SCREEN_HEIGHT // 2 - mouse_y), Constant.SCREEN_WIDTH // 2 - mouse_x)

        if self.world.inventory.items[self.world.inventory.current_item]:
            if self.world.inventory.items[self.world.inventory.current_item].item_type == InventoryItem.SKATEBOARD:
              speed = Constant.PLAYER_SPEED_SKATEBOARD
            else:
                speed = Constant.PLAYER_SPEED
        else:
            speed = Constant.PLAYER_SPEED
        player_pos = self.get_grid_position()
        if self.grid.grid[player_pos[0]][player_pos[1]].type == CellType.NATURE:
            speed *= Constant.PLAYER_SPEED_GRASS_MULTIPLIER

        if self.held_keys[pygame.K_LSHIFT]:
            speed *= Constant.PLAYER_SPEED_SLOW_WALKING_MULTIPLIER

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

        new_grid_x = (self.x + delta_x) // Constant.TILE_SIZE
        new_grid_y = (self.y + delta_y) // Constant.TILE_SIZE

        old_moving = self.moving

        if (delta_x != 0 or delta_y != 0) and \
                new_grid_x >= 0 and new_grid_y >= 0 and new_grid_x < Constant.GRID_WIDTH and new_grid_y < Constant.GRID_HEIGHT:
            if self.grid.grid[int(new_grid_x)][self.get_grid_position(True)[1]].type not in [CellType.BUILDING, CellType.DOOMINOS]:
                self.x += delta_x
            if self.grid.grid[self.get_grid_position(True)[0]][int(new_grid_y)].type not in [CellType.BUILDING, CellType.DOOMINOS]:
                self.y += delta_y

            self.moving = True
        else:
            self.moving = False
            if self.moving_sound:
                self.moving_sound.stop()
                self.moving_sound = None

        if not old_moving and self.moving:
            self.moving_sound = self.audio_manager.play_sfx(SFX.FAST_WALK)

        if not self.moving:
            if self.moving_sound:
                self.moving_sound.stop()
                self.moving_sound = None

        self.step_no += 1

        if self.step_no % 15 == 0 and self.moving:
            self.world.emitter_handler.add_emitter(Footstep(self.x, self.y, distance((0, 0), (delta_x, delta_y))))

        self.world.inventory.step()

    def draw(self, screen: pygame.Surface, camera):
        rotated = pygame.transform.rotate(self.gen_texture(), self.angle * (180.0 / pi))
        camera.blit_surface_to_screen(screen, rotated, self.x, self.y)
        # self.world.inventory.draw(screen, camera)

    def take_damage(self, amount):
        self.is_taking_damage = True
        self.health = max(0, self.health - 1)

    def get_grid_position(self, as_int=True):
        """
        Return the coordinates of the grid cell the player is currently in
        :param as_int: should the coordinates be returned as integers (default) or floats
        :return: tuple of x,y coordinates
        """
        if as_int:
            return (
                int(self.x // Constant.TILE_SIZE),
                int(self.y // Constant.TILE_SIZE),
            )
        else:
            return (
                self.x / Constant.TILE_SIZE,
                self.y / Constant.TILE_SIZE,
            )
