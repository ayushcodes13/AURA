import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.playback import play
import threading
import io


VOICE = "en-US-AndrewMultilingualNeural"


async def stream_tts(text: str):
    """
    Adaptive streaming TTS:
    - Small chunks initially (fast start)
    - Larger chunks later (natural cadence)
    - Plays while receiving
    """
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="+0%",
        volume="+0%"
    )

    # this gives an async generator of chunks
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes = chunk["data"]

            # convert MP3 chunk to AudioSegment
            seg = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")

            # SMALL initial chunks = instant voice start
            if len(seg) < 400:
                threading.Thread(target=play, args=(seg,), daemon=True).start()
                continue

            # Larger chunks later = natural delivery
            threading.Thread(target=play, args=(seg,), daemon=True).start()


async def speak(text: str):
    """
    Drop-in TTS function for main.py
    """
    await stream_tts(text)