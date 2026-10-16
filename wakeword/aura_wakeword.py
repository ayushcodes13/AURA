import os
import struct
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "../config/.env"))
def listen_for_wake_word():
    import pvporcupine
    import sounddevice as sd

    access_key = os.getenv("PICOVOICE_ACCESS_KEY")
    if not access_key:
        raise RuntimeError("PICOVOICE_ACCESS_KEY is missing. Set it in config/.env or the environment.")
    if os.uname().sysname == "Darwin":
        keyword_path = os.path.join(os.path.dirname(__file__), "hey_aura_new.ppn")
    else:
        keyword_path = os.path.join(os.path.dirname(__file__), "hello_aura_rpi.ppn")
    if not os.path.isfile(keyword_path):
        raise RuntimeError(
            f"Porcupine keyword model is missing: {keyword_path}. "
            "Download the model for this platform from Picovoice and keep it local."
        )

    porcupine = pvporcupine.create(
        access_key=access_key,
        keyword_paths=[keyword_path],
        sensitivities=[1.0]
    )
    sample_rate = porcupine.sample_rate
    frame_length = porcupine.frame_length
    print("🎧 Wake word engine active — say: 'Hey Aura'")
    try:
        with sd.RawInputStream(
            samplerate=sample_rate,
            blocksize=frame_length,
            dtype='int16',
            channels=1
        ) as stream:
            while True:
                frame = stream.read(frame_length)[0]
                pcm = struct.unpack_from("h" * frame_length, frame)
                result = porcupine.process(pcm)
                if result >= 0:
                    print("✨ Wake word detected: HEY AURA")
                    return True
    finally:
        porcupine.delete()

if __name__ == "__main__":
    listen_for_wake_word()
