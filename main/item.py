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
        camera.blit_surface_to_screen(window, item_texture, x, y)

