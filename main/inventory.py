from enum import Enum

import pygame

from entities.flamethrower import Flamethrower
from main.constants import Constant


class InventoryItem(Enum):
    FLAMETHROWER = "flamethrower",
    PIZZA = "pizza"


class Inventory(object):

    SLOT_WIDTH = 50
    SLOT_HEIGHT = 50
    SLOT_MARGIN = 20
    SELECT_THICKNESS = 3

    def __init__(self, world):
        self.world = world
        self.N_slots = 5

        self.current_item = 0

        self.items = [None] * self.N_slots

        self.add_item(InventoryItem.FLAMETHROWER)

    def step(self):
        for item in self.items:
            if item:
                item.step()

    def draw(self, window: pygame.Surface, camera):
        pygame.draw.rect(window, (123, 123, 123), pygame.Rect(Constant.SCREEN_WIDTH / 2 - self.SLOT_WIDTH / 2 - int(self.N_slots / 2) * (self.SLOT_WIDTH + self.SLOT_MARGIN) - self.SLOT_MARGIN,
                                                              Constant.SCREEN_HEIGHT - 70,
                                                              (self.SLOT_WIDTH + self.SLOT_MARGIN) * self.N_slots + self.SLOT_MARGIN,
                                                              self.SLOT_HEIGHT + 100))
        current_item_to_draw = 0
        for i in range(0 - int(self.N_slots / 2), self.N_slots - int(self.N_slots / 2)):
            if current_item_to_draw == self.current_item:
                left_offset = Constant.SCREEN_WIDTH / 2 - self.SLOT_WIDTH / 2 + i * (self.SLOT_WIDTH + self.SLOT_MARGIN)
                pygame.draw.rect(window, (255, 255, 0), pygame.Rect(left_offset - self.SELECT_THICKNESS,
                                                                    Constant.SCREEN_HEIGHT - 60 - self.SELECT_THICKNESS,
                                                                    self.SLOT_WIDTH + self.SELECT_THICKNESS * 2,
                                                                    self.SLOT_HEIGHT + self.SELECT_THICKNESS * 2))

            left_offset = Constant.SCREEN_WIDTH / 2 - self.SLOT_WIDTH / 2 + i * (self.SLOT_WIDTH + self.SLOT_MARGIN)
            pygame.draw.rect(window, (233, 233, 233), pygame.Rect(left_offset,
                                                                  Constant.SCREEN_HEIGHT - 60,
                                                                  self.SLOT_WIDTH, self.SLOT_HEIGHT))


            item_to_draw = self.items[current_item_to_draw]
            if item_to_draw:
                self.items[current_item_to_draw].draw_inventory_slot(window, camera, left_offset, Constant.SCREEN_HEIGHT - 60)
            current_item_to_draw += 1

    def add_item(self, item: InventoryItem):
        if None not in self.items:
            print("Inventory full! Unlucky bro")
            return False

        if item == InventoryItem.FLAMETHROWER:
            for i in range(len(self.items)):
                if self.items[i] is None:
                    self.items[i] = Flamethrower(self.world.player,
                                                 item_type=InventoryItem.FLAMETHROWER,
                                                 # TODO: Change to flamethrower icon
                                                 inventory_icon_file_name="pizza_inventory_icon.png")
                    return True

    def change_current_selected_item(self, direction):
        if direction == "left":
            self.current_item = (self.current_item - 1) % self.N_slots
        else:
            self.current_item = (self.current_item + 1) % self.N_slots

