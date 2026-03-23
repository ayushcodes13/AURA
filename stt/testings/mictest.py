import sounddevice as sd
import numpy as np

SAMPLE_RATE = 16000
DURATION = 3
CHANNELS = 1

print("Recording test… speak something...")
audio = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
sd.wait()

print("Audio mean:", np.abs(audio).mean())
print("Audio max:", np.abs(audio).max())

if np.abs(audio).max() < 50:
    print("❌ Your mic is not capturing audio at 16kHz")
else:
    print("✅ Mic is working!")