from abc import ABC, abstractmethod
from enum import Enum
from threading import Thread

import pygame


class Songs(Enum):
    ENERGIEK = "energiek.wav",
    PIZZATHEME = "pizzatheme.wav",
    PIZZATHEMELOOP = "pizzathemeloopver.wav",


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

    music_audio_level = 0.1
    sfx_audio_level = 0.1

    def play_song(self, song):

        if song == Songs.ENERGIEK:
            thread = Thread(target=self.load_song, args=("energiek.wav",))
            thread.start()
        if song == Songs.PIZZATHEME:
            thread = Thread(target=self.load_song, args=("pizzatheme.wav",))
            thread.start()
        if song == Songs.PIZZATHEMELOOP:
            thread = Thread(target=self.load_song, args=("pizzathemeloopver.wav",))
            thread.start()

    def play_sfx(self,):
        pass

    def load_song(self, song_str):
        # song_obj = pygame.mixer.Sound(self.MUSIC_PATH + song_str)
        # song_obj.play(loops=2)
        pygame.mixer.music.load(self.MUSIC_PATH + song_str)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(self.music_audio_level)

    def update_music_audio_level(self, direction):
        if direction == 'left':
            self.music_audio_level -= 0.05
        elif direction == 'right':
            self.music_audio_level += 0.05
        else:
            print("Update music audio level requires a valid direction. wtf even is " + str(direction) + "???")
        if self.music_audio_level < 0:
            self.music_audio_level = 0
        elif self.music_audio_level > 1:
            self.music_audio_level = 1
        pygame.mixer.music.set_volume(self.music_audio_level)

    def update_sfx_audio_level(self, direction):
        if direction == 'left':
            self.sfx_audio_level -= 0.05
        elif direction == 'right':
            self.sfx_audio_level += 0.05
        else:
            print("Update sfx audio level requires a valid direction. wtf even is " + str(direction) + "???")
        if self.sfx_audio_level < 0:
            self.sfx_audio_level = 0
        elif self.sfx_audio_level > 1:
            self.sfx_audio_level = 1







