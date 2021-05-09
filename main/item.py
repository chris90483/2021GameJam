import pygame

from pygame import Surface


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

    def __init__(self, item_type, inventory_icon_file_name):
        super().__init__(item_type, inventory_icon_file_name)
        self.item_type = item_type
        self.inventory_icon_file_name = inventory_icon_file_name
        self.activated = False

    def step(self):
        pass

    def draw_inventory_slot(self, window: Surface, camera, x, y):
        item_texture = pygame.image.load(self.IMAGE_FOLDER_LOCATION + self.inventory_icon_file_name)
        window.blit(item_texture, (x, y))

