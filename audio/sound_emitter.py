from audio.audio import SoundEmitter


class Footstep(SoundEmitter):

    def get_soundfile(self):
        return None

    def get_loudness(self):
        return 10


class DogBark(SoundEmitter):

    def get_soundfile(self):
        return None

    def get_loudness(self):
        return 100
