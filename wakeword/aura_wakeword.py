import pvporcupine
import sounddevice as sd
import struct
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))
ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")

if os.uname().sysname == "Darwin":
    KEYWORD_PATH = os.path.join(os.path.dirname(__file__), "hey_aura_new.ppn")
else:
    KEYWORD_PATH = os.path.join(os.path.dirname(__file__), "hello_aura_rpi.ppn")

porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[KEYWORD_PATH],
    sensitivities=[1.0]
)

SAMPLE_RATE = porcupine.sample_rate
FRAME_LENGTH = porcupine.frame_length

def listen_for_wake_word():
    print("🎧 Wake word engine active — say: 'Hey Aura'")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=FRAME_LENGTH,
        dtype='int16',
        channels=1
    ) as stream:

        while True:
            frame = stream.read(FRAME_LENGTH)[0]
            pcm = struct.unpack_from("h" * FRAME_LENGTH, frame)
            result = porcupine.process(pcm)

            if result >= 0:
                print("✨ Wake word detected: HEY AURA")
                return True  

if __name__ == "__main__":
    listen_for_wake_word()