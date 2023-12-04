class SoundHandler:
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager

    def play_sound(self, path="data/sounds/tmp.wav"):
        self.sound_manager.play_async(path)

    def play_sound_all(self, path="data/sounds/tmp.wav"):
        self.sound_manager.play_all_async(path)