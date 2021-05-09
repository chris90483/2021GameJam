"""
    This class will hold the world and all other game features
"""
from pygame.surface import Surface

from main.camera import Camera
from main.constants import Constant
from main.world import World
from main.score import Score
import hashlib
import urllib.request, urllib.parse
from threading import Thread


class Game(object):
    __game_over = False
    __game_started = False

    def __init__(self, amount_tiles_x, amount_tiles_y, audio_manager):
        self.player_name = ''
        self.audio_manager = audio_manager
        self.score = Score()
        self.world = World(amount_tiles_x, amount_tiles_y, audio_manager, self.score)
        self.camera = Camera(self.world.player)

        self.set_game_over() # TODO Remove

    def handle_input(self, event):
        self.world.handle_input(event)

    def step(self):
        self.world.step()
        if self.world.player.health < 1:
            self.set_game_over()

    def draw(self, screen: Surface):
        self.world.draw(screen, self.camera)

    def set_game_over(self):
        self.__game_over = True

        Thread(target=self.__send_score, args=(self.player_name, self.score.get_score())).start()

    def start_game(self):
        self.__game_started = True

    def __send_score(self, name, score):
        name = 'Test' # TODO Remove
        if name.strip() == '':
            return

        score = str(round(score, 2))

        sha256 = hashlib.sha256()
        sha256.update((name + str(score) + "manySecureMuchSafeSalt").encode())
        hash = sha256.hexdigest()

        name = urllib.parse.quote(name)
        hash = urllib.parse.quote(hash)

        try:
            resp = urllib.request.urlopen(
                Constant.SCORE_SUBMIT_URL + "?name={}&score={}&hash={}".format(name, score, hash),
                timeout=4
            )
            if resp.getcode() != 200:
                print("Error submitting scores: %s" % resp)
            else:
                print("Score successfully submitted to server")
        except Exception as e:
            print("Error submitting scores: %s" % e)

    def is_game_over(self):
        return self.__game_over

    def is_game_started(self):
        return self.__game_started

