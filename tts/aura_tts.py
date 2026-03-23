import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play
import threading

VOICE = "en-US-AndrewMultilingualNeural"
OUTPUT_FILE = "tts_output.mp3"

# ---------------------------
# Generate speech (async)
# ---------------------------
async def tts_generate(text: str):
    try:
        communicate = edge_tts.Communicate(
            text=text,
            voice=VOICE,
            rate="+0%",
            volume="+0%"
        )
        await communicate.save(OUTPUT_FILE)
    except Exception as e:
        print(f"[TTS GENERATE ERROR] {e}")


# ---------------------------
# Play audio (threaded, non-blocking)
# ---------------------------
def play_audio():
    try:
        audio = AudioSegment.from_file(OUTPUT_FILE, format="mp3")
        play(audio)
    except Exception as e:
        print(f"[TTS PLAYBACK ERROR] {e}")


# ---------------------------
# Main speak function
# ---------------------------
async def speak(text: str):
    """
    1. Generate audio (async)
    2. Play audio in background thread
    """
    await tts_generate(text)
    threading.Thread(target=play_audio, daemon=True).start()
    
