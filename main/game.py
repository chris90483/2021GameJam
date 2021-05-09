"""
    This class will hold the world and all other game features
"""
from pygame.surface import Surface

from main.camera import Camera
from main.constants import Constant
from main.world import World
from main.score import Score
import hashlib
from threading import Thread


class Game(object):
    __game_over = False
    __game_started = False

    def __init__(self, player_name, amount_tiles_x, amount_tiles_y, audio_manager):
        self.player_name = player_name
        self.audio_manager = audio_manager
        self.score = Score()
        self.world = World(amount_tiles_x, amount_tiles_y, audio_manager, self.score)
        self.camera = Camera(self.world.player)

    def handle_input(self, event):
        self.world.handle_input(event)

    def step(self):
        self.world.step()
        if self.world.player.health < 1:
            self.set_game_over()

    def draw(self, screen: Surface):
        self.world.draw(screen, self.camera)

    def reset(self):
        # TODO Check if this indeed resets everything
        self.__game_over = False
        self.__game_started = False
        self.score.reset_score()
        self.world.reset()

    def set_game_over(self):
        self.__game_over = True

        Thread(target=self.__send_score, args=(self.player_name, self.score.get_score())).start()

    def start_game(self):
        self.__game_started = True

    def __send_score(self, name, score):
        pass

    def is_game_over(self):
        return self.__game_over

    def is_game_started(self):
        return self.__game_started

