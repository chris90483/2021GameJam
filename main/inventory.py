from enum import Enum

import pygame

from entities.flamethrower import Flamethrower
from entities.skateboard import Skateboard
from main.constants import Constant
from main.item import Pizza, Knife, Klok


class InventoryItem(Enum):
    FLAMETHROWER = "flamethrower"
    PIZZA = "pizza"
    SKATEBOARD = "skateboard"
    KNIFE = "knife"
    KLOK = "Klok"


class Inventory(object):

    SLOT_MARGIN = 20
    SELECT_THICKNESS = 3

    def __init__(self, world):
        self.world = world
        self.N_slots = 5

        self.current_item = 0

        self.items = [None] * self.N_slots

        self.add_item(InventoryItem.FLAMETHROWER)
        self.add_item(InventoryItem.PIZZA)
        self.add_item(InventoryItem.SKATEBOARD)
        self.add_item(InventoryItem.KNIFE)
        self.add_item(InventoryItem.KLOK)

    def step(self):
        for item in self.items:
            if item:
                item.step()

    def get_item(self, item_type: InventoryItem):
        for x in range(0, len(self.items)):
            if not self.items[x] is None:
                if self.items[x].item_type == item_type:
                    return self.items[x]

    def draw(self, window: pygame.Surface, camera):
        pygame.draw.rect(window, (123, 123, 123), pygame.Rect(Constant.SCREEN_WIDTH / 2 - Constant.SLOT_WIDTH / 2 - int(self.N_slots / 2) * (Constant.SLOT_WIDTH + self.SLOT_MARGIN) - self.SLOT_MARGIN,
                                                              Constant.SCREEN_HEIGHT - 70,
                                                              (Constant.SLOT_WIDTH + self.SLOT_MARGIN) * self.N_slots + self.SLOT_MARGIN,
                                                              Constant.SLOT_HEIGHT + 100))
        current_item_to_draw = 0
        for i in range(0 - int(self.N_slots / 2), self.N_slots - int(self.N_slots / 2)):
            if current_item_to_draw == self.current_item:
                left_offset = Constant.SCREEN_WIDTH / 2 - Constant.SLOT_WIDTH / 2 + i * (Constant.SLOT_WIDTH + self.SLOT_MARGIN)
                pygame.draw.rect(window, (255, 255, 0), pygame.Rect(left_offset - self.SELECT_THICKNESS,
                                                                    Constant.SCREEN_HEIGHT - 60 - self.SELECT_THICKNESS,
                                                                    Constant.SLOT_WIDTH + self.SELECT_THICKNESS * 2,
                                                                    Constant.SLOT_HEIGHT + self.SELECT_THICKNESS * 2))

            left_offset = Constant.SCREEN_WIDTH / 2 - Constant.SLOT_WIDTH / 2 + i * (Constant.SLOT_WIDTH + self.SLOT_MARGIN)
            pygame.draw.rect(window, (233, 233, 233), pygame.Rect(left_offset,
                                                                  Constant.SCREEN_HEIGHT - 60,
                                                                  Constant.SLOT_WIDTH, Constant.SLOT_HEIGHT))

            item_to_draw = self.items[current_item_to_draw]
            if item_to_draw:
                self.items[current_item_to_draw].draw_inventory_slot(window, camera, left_offset, Constant.SCREEN_HEIGHT - 60)
            current_item_to_draw += 1

    def add_item(self, item: InventoryItem):
        if None not in self.items:
            print("Inventory full! Unlucky bro")
            return False

        for i in range(len(self.items)):
            if self.items[i] is None:
                if item == InventoryItem.FLAMETHROWER:
                    self.items[i] = Flamethrower(self.world.player,
                                                 item_type=InventoryItem.FLAMETHROWER,
                                                 inventory_icon_file_name="flamethrower_inventory_icon.png")
                    return True
                if item == InventoryItem.PIZZA:
                    self.items[i] = Pizza(InventoryItem.PIZZA, inventory_icon_file_name="pizza_inventory_icon.png")
                    return True
                if item == InventoryItem.SKATEBOARD:
                    self.items[i] = Skateboard(InventoryItem.SKATEBOARD, inventory_icon_file_name="skateboard_inventory_icon.png")
                    return True
                if item == InventoryItem.KNIFE:
                    self.items[i] = Knife(InventoryItem.KNIFE, "knife_inventory_icon.png", self.world.player)
                    return True
                if item == InventoryItem.KLOK:
                    self.items[i] = Klok(InventoryItem.KLOK, "klok_inventory_icon.png")
                    return True

    def set_current_item(self, new_current_item):
        if self.items[self.current_item] and self.items[self.current_item].item_type in [InventoryItem.FLAMETHROWER, InventoryItem.KNIFE] and self.items[self.current_item].activated:
            self.items[self.current_item].activated = False
        if new_current_item in range(0, self.N_slots):
            self.current_item = new_current_item

    def remove_item(self, to_remove_item: InventoryItem):
        for i in range(len(self.items)):
            if self.items[i]:
                if self.items[i].item_type == to_remove_item:
                    self.items[i] = None

    def change_current_selected_item(self, direction):
        if self.items[self.current_item] and self.items[self.current_item].item_type in [InventoryItem.FLAMETHROWER, InventoryItem.KNIFE] and self.items[self.current_item].activated:
            self.items[self.current_item].activated = False
        if direction == "left":
            self.current_item = (self.current_item - 1) % self.N_slots
        else:
            self.current_item = (self.current_item + 1) % self.N_slots
