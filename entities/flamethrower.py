import math
from math import atan2

import pygame

from audio.audio import SFX
from main.constants import Constant
from main.item import Item
from main.util import distance


class Flamethrower(Item):

    def __init__(self, player, item_type, inventory_icon_file_name):
        super().__init__(item_type, inventory_icon_file_name)
        self.player = player
        self.fuel_left = Constant.FLAMETHROWER_FUEL
        self.activated = False
        self.empty = False
        self.keyframes_fire_spitting_counter = 0
        self.keyframes_fire_spitting = []
        for x in range(1, 4):
            self.keyframes_fire_spitting.append(pygame.image.load("./resources/png/animations/flamethrower/fire_spitting_" + str(x) + ".png"))

        self.keyframes_empty_counter = 0
        self.keyframes_empty = []
        for x in range(1, 7):
            self.keyframes_empty.append(pygame.image.load("./resources/png/animations/flamethrower/empty_" + str(x) + ".png"))

        self.flamethrower_thickness = math.pi/16

        self.playing_fire_sfx = False

        self.flamethrower_sound = None

    def toggle(self):
        self.activated = not self.activated

    def step(self):
        currently_playing_fire_sfx = self.playing_fire_sfx

        if self.playing_fire_sfx and not self.activated:
            self.player.world.audio_manager.unload_sfx(self.flamethrower_sound)
            self.flamethrower_sound = None
            self.playing_fire_sfx = False

        if self.activated and not self.empty:
            self.playing_fire_sfx = True
            if currently_playing_fire_sfx != self.playing_fire_sfx:
                self.flamethrower_sound = self.player.world.audio_manager.play_sfx(SFX.FLAMETHROWER_FIRE)
            self.fuel_left -= 1
            if self.fuel_left < 1:
                self.empty = True

            if not self.empty:
                zombies = self.player.world.zombie_handler.zombies

                for zombie in zombies:
                    player_angle = self.player.angle
                    zombie_angle = atan2(zombie.y - self.player.y, self.player.x - zombie.x)
                    zombie_angle_min = zombie_angle - self.flamethrower_thickness
                    zombie_angle_max = zombie_angle + self.flamethrower_thickness

                    if distance((self.player.x, self.player.y), (zombie.x, zombie.y)) < 250.0 \
                            and zombie_angle_min < player_angle < zombie_angle_max:
                        self.player.world.zombie_handler.delete_zombie(zombie)
                        # print("kill zombie", i)

    def draw_inventory_slot(self, window, camera, x, y):
        super().draw_inventory_slot(window, camera, x, y)

        pygame.draw.rect(window, (0, 128, 0), pygame.Rect(x, y + Constant.SLOT_HEIGHT - 5, Constant.SLOT_WIDTH * (self.fuel_left / Constant.FLAMETHROWER_FUEL), 5))
