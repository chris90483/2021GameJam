from audio.audio import SoundEmitter


class Footstep(SoundEmitter):
    def __init__(self, x, y, speed):
        super().__init__(x, y)
        self.loudness = speed * 100.0

    def get_soundfile(self):
        return None

    def get_loudness(self):
        return self.loudness


class DogBark(SoundEmitter):

    def get_soundfile(self):
        return None

    def get_loudness(self):
        return 500
