import simpleaudio as sa
import threading
import time
import os
import glob

class SoundManager:
    def __init__(self):
        pass

    def play(self, filename):
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()  # Wait until sound has finished playing

    def play_async(self, filename="data/sounds/tmp.wav"):
        threading.Thread(target=self.play, args=(filename,)).start()

    def play_all(self):
        for filename in glob.glob("data/sounds/*.wav"):
            self.play(filename)

    def play_all_async(self, filename="data/sounds/tmp.wav"):
        threading.Thread(target=self.play_all).start()
    
if __name__ == "__main__":
    pass

