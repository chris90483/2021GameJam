from abc import ABC, abstractmethod
from enum import Enum
from threading import Thread

import pygame


class Songs(Enum):
    ENERGIEK = "alleenintro.mp3",


class SFX(Enum):
    WALK = None,
    RUN = None,
    SNEAK = None,


class SoundEmitter(ABC):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @abstractmethod
    def get_loudness(self):
        pass

    @abstractmethod
    def get_soundfile(self):
        pass


class AudioManagement:

    MUSIC_PATH = "./resources/audio/music/"
    SFX_PATH = "./resources/audio/sfx/"

    audio_level = 0.1

    def play_song(self, song):

        if song == Songs.ENERGIEK:
            thread = Thread(target=self.load_song, args=("energiek.mp3",))
            thread.start()

    def play_sfx(self,):
        pass

    def load_song(self, song_str):
        # song_obj = pygame.mixer.Sound(self.MUSIC_PATH + song_str)
        # song_obj.play(loops=2)
        pygame.mixer.music.load(self.MUSIC_PATH + song_str)
        pygame.mixer.music.play(loops=2)
        pygame.mixer.music.set_volume(self.audio_level)



