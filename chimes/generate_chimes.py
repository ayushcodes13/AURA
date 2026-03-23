# chimes/generate_chimes.py
from pydub import AudioSegment
import numpy as np
import os

def tone(freq, duration=100, volume=-12):
    sr = 44100
    t = np.linspace(0, duration/1000, int(sr * duration/1000), False)
    wave = np.sin(freq * t * 2 * np.pi)
    audio = AudioSegment(
        (wave * 32767).astype(np.int16).tobytes(),
        frame_rate=sr,
        sample_width=2,
        channels=1
    )
    return audio + volume

def save(audio, filename):
    audio.export(filename, format="wav")
    print("Saved:", filename)

BASE = os.path.dirname(__file__)

# ----------------------
# 1. wake.wav (soft “tiip”)
# ----------------------
wake = tone(1000, 60, -8)
save(wake, f"{BASE}/wake.wav")

# ----------------------
# 2. thinking_start.wav
# ----------------------
thinking = tone(260, 150, -10)
save(thinking, f"{BASE}/thinking_start.wav")

# ----------------------
# 3. thinking_loop.wav (low hum)
# ----------------------
loop = tone(150, 700, -25).fade_in(50).fade_out(150)
save(loop, f"{BASE}/thinking_loop.wav")

# ----------------------
# 4. response_start.wav (smooth ding)
# ----------------------
resp = tone(1400, 110, -6)
save(resp, f"{BASE}/response_start.wav")

# ----------------------
# 5. error.wav (boop-boop)
# ----------------------
err = tone(700, 120, -6) + tone(540, 140, -6)
save(err, f"{BASE}/error.wav")

# ----------------------
# 6. interrupt.wav (short click)
# ----------------------
click = tone(950, 70, -5)
save(click, f"{BASE}/interrupt.wav")