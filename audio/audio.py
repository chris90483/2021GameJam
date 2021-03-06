import time
from abc import ABC, abstractmethod
from enum import Enum
from threading import Thread

import pygame

from main.util import distance


class Songs(Enum):
    ENERGIEK = "energiek.wav",
    PIZZATHEME = "pizzatheme.wav",
    PIZZATHEMELOOP = "pizzathemeloopver.wav",


class SFX(Enum):
    SLOW_WALK = "walk_slow.wav",
    FAST_WALK = "walk_fast.wav",
    DOG_GROWL = "dog_growl.wav",
    DOG_BARK = "dog_bark.wav",
    FLAMETHROWER_FIRE = "flamethrower_fire.wav",
    FLAMETHROWER_EMPTY = "flamethrower_empty.wav",
    KNIFE_SWISH = "knife_swish.wav",
    SKATEBOARD = "skateboard.wav"


class SoundEmitter(ABC):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.step_v = 0
        self.timestamp = time.time()

    @abstractmethod
    def get_loudness(self):
        pass

    @abstractmethod
    def get_soundfile(self):
        pass

    def get_loudness_at_position(self, x, y):
        dist = distance((x, y), (self.x, self.y))
        if dist == 0:
            return self.get_loudness()
        return (self.get_loudness())/dist

    def step(self):
        self.step_v += 1
        # The emitter will be removed after 100 steps
        return self.step_v > 100

    def draw(self, screen, camera):
        # Circles for debug:
        if 2 < self.step_v < 30:
            screen_x, screen_y = camera.compute_screen_position(self.x, self.y)
            pygame.draw.circle(screen, (255, 255, 255, int(30 * ((15 - abs(15 - self.step_v))/30.0))),
                               (int(screen_x), int(screen_y)),
                               int(self.get_loudness()), 0)


class AudioManager:
    MUSIC_PATH = "./resources/audio/music/"
    SFX_PATH = "./resources/audio/sfx/"

    music_audio_level = 0.1
    sfx_audio_level = 0.2

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

    def play_sfx(self, sfx, sound_factor=1):
        if sfx == SFX.FAST_WALK:
            return self.load_sfx("walk_fast.wav", sound_factor=1, loop=-1)
        if sfx == SFX.SLOW_WALK:
            return self.load_sfx("walk_slow.wav", sound_factor=1, loop=-1)
        if sfx == SFX.DOG_GROWL:
            return self.load_sfx("dog_growl.wav", sound_factor, loop=0)
        if sfx == SFX.DOG_BARK:
            return self.load_sfx("dog_bark.wav", sound_factor, loop=0)
        if sfx == SFX.FLAMETHROWER_FIRE:
            return self.load_sfx("flamethrower_fire.wav", sound_factor=1, loop=-1)
        if sfx == SFX.FLAMETHROWER_EMPTY:
            return self.load_sfx("flamethrower_empty.wav", sound_factor=1, loop=-1)
        if sfx == SFX.KNIFE_SWISH:
            return self.load_sfx("knife_swish.wav", sound_factor=1, loop=0)
        if sfx == SFX.SKATEBOARD:
            return self.load_sfx("skateboard_sound.wav", sound_factor=1, loop=-1)

    def load_song(self, song_str):
        # song_obj = pygame.mixer.Sound(self.MUSIC_PATH + song_str)
        # song_obj.play(loops=2)
        pygame.mixer.music.load(self.MUSIC_PATH + song_str)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(self.music_audio_level)

    def load_sfx(self, sfx_str, sound_factor, loop):
        sound = pygame.mixer.Sound(self.SFX_PATH + sfx_str)
        sound.set_volume(self.sfx_audio_level * sound_factor)
        sound.play(loop)
        return sound

    def unload_sfx(self, sound):
        sound.stop()

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




