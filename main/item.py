import pygame

from main.util import distance
from pygame import Surface
from math import atan2, pi

class Item:

    IMAGE_FOLDER_LOCATION = "./resources/png/"

    def __init__(self, item_type, inventory_icon_file_name):
        self.item_type = item_type
        self.inventory_icon_file_name = inventory_icon_file_name

    def step(self):
        pass

    def draw_inventory_slot(self, window: Surface, camera, x, y):
        item_texture = pygame.image.load(self.IMAGE_FOLDER_LOCATION + self.inventory_icon_file_name)
        window.blit(item_texture, (x, y))


class Pizza(Item):

    def __init__(self, item_type, inventory_icon_file_name):
        super().__init__(item_type, inventory_icon_file_name)
        self.item_type = item_type
        self.inventory_icon_file_name = inventory_icon_file_name

    def step(self):
        pass

    def draw_inventory_slot(self, window: Surface, camera, x, y):
        item_texture = pygame.image.load(self.IMAGE_FOLDER_LOCATION + self.inventory_icon_file_name)
        window.blit(item_texture, (x, y))


class Knife(Item):

    def __init__(self, item_type, inventory_icon_file_name, player):
        super().__init__(item_type, inventory_icon_file_name)
        self.item_type = item_type
        self.inventory_icon_file_name = inventory_icon_file_name
        self.activated = False
        self.player = player
        self.knife_range = pi/4

    def step(self):
        if self.activated:
            zombies = self.player.world.zombie_handler.zombies
            zombies_to_delete = []

            for zombie in zombies:
                player_angle = self.player.angle
                zombie_angle = atan2(zombie.y - self.player.y, self.player.x - zombie.x)
                zombie_angle_min = zombie_angle - self.knife_range
                zombie_angle_max = zombie_angle + self.knife_range

                if distance((self.player.x, self.player.y), (zombie.x, zombie.y)) < 50.0 \
                        and zombie_angle_min < player_angle < zombie_angle_max:
                    self.player.world.zombie_handler.delete_zombie(zombie)

    def draw_inventory_slot(self, window: Surface, camera, x, y):
        item_texture = pygame.image.load(self.IMAGE_FOLDER_LOCATION + self.inventory_icon_file_name)
        window.blit(item_texture, (x, y))

