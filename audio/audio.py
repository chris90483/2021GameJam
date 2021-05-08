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
        self.step_v = 0

    @abstractmethod
    def get_loudness(self):
        pass

    @abstractmethod
    def get_soundfile(self):
        pass

    def step(self):
        self.step_v += 1

        return self.step_v > 100

    def draw(self, screen, camera):
        if self.step_v < 30:
            screen_x, screen_y = camera.compute_screen_position(self.x, self.y)
            pygame.draw.circle(screen, (246, 1, 1), (screen_x, screen_y), self.step_v * 2 + 1, 1)


class AudioManagement:
    MUSIC_PATH = "./resources/audio/music/"
    SFX_PATH = "./resources/audio/sfx/"

    audio_level = 0.1

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

    def play_sfx(self, ):
        pass

    def load_song(self, song_str):
        # song_obj = pygame.mixer.Sound(self.MUSIC_PATH + song_str)
        # song_obj.play(loops=2)
        pygame.mixer.music.load(self.MUSIC_PATH + song_str)
        pygame.mixer.music.play(loops=2)
        pygame.mixer.music.set_volume(self.audio_level)
