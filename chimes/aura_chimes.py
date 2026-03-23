import simpleaudio as sa
import os

BASE = os.path.dirname(__file__)

class AuraChimes:
    def __init__(self):
        self.sounds = {
            "wake": self.load("wake.wav"),
            "thinking_start": self.load("thinking_start.wav"),
            "thinking_loop": self.load("thinking_loop.wav"),
            "response_start": self.load("response_start.wav"),
            "error": self.load("error.wav"),
            "interrupt": self.load("interrupt.wav"),
        }

    def load(self, name):
        path = os.path.join(BASE, name)
        return sa.WaveObject.from_wave_file(path)

    def play(self, name):
        try:
            self.sounds[name].play()
        except:
            print("[CHIME ERROR] failed to play:", name)