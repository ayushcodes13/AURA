import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play
import threading
import os
from pathlib import Path
import tempfile

VOICE = "en-US-AndrewMultilingualNeural"
RUNTIME_DIR = Path(__file__).resolve().parents[1] / ".runtime"

# ---------------------------
# Generate speech (async)
# ---------------------------
async def tts_generate(text: str):
    output_file = None
    try:
        RUNTIME_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd, output_file = tempfile.mkstemp(prefix="aura_tts_", suffix=".mp3", dir=RUNTIME_DIR)
        os.close(fd)
        communicate = edge_tts.Communicate(
            text=text,
            voice=VOICE,
            rate="+0%",
            volume="+0%"
        )
        await communicate.save(output_file)
        return output_file
    except Exception as e:
        print(f"[TTS GENERATE ERROR] {e}")
        if output_file:
            try:
                os.remove(output_file)
            except FileNotFoundError:
                pass
        return None


# ---------------------------
# Play audio (threaded, non-blocking)
# ---------------------------
def play_audio(output_file):
    try:
        audio = AudioSegment.from_file(output_file, format="mp3")
        play(audio)
    except Exception as e:
        print(f"[TTS PLAYBACK ERROR] {e}")
    finally:
        try:
            os.remove(output_file)
        except FileNotFoundError:
            pass


# ---------------------------
# Main speak function
# ---------------------------
async def speak(text: str):
    """
    1. Generate audio (async)
    2. Play audio in background thread
    """
    output_file = await tts_generate(text)
    if output_file:
        threading.Thread(target=play_audio, args=(output_file,), daemon=True).start()
    
