import asyncio
import sounddevice as sd
import numpy as np
from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from dotenv import load_dotenv
import os
import time

# -------------------------
# Load env
# -------------------------
env_path = os.path.join(os.path.dirname(__file__), "../config/.env")
load_dotenv(dotenv_path=env_path)
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

print("ENV PATH:", env_path)
print("ENV EXISTS:", os.path.exists(env_path))
print("DEEPGRAM KEY LOADED:", bool(DEEPGRAM_API_KEY))

# -------------------------
# Constants
# -------------------------
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_MS = 80
CHUNK_SIZE = int(SAMPLE_RATE * (CHUNK_MS / 1000))  # samples per chunk

RESET = "\033[0m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"

# -------------------------
# Helpers
# -------------------------
def print_partial(text):
    print(f"{YELLOW}[PARTIAL] {text}{RESET}")

def print_final(text):
    print(f"{GREEN}[FINAL - END OF TURN] {text}{RESET}")

def print_barge():
    print(f"{RED}[BARGE-IN] User interrupted AURA{RESET}")

# -------------------------
# Main debug runner
# -------------------------
async def run_debug():
    if not DEEPGRAM_API_KEY:
        print(f"{RED}DEEPGRAM_API_KEY not found in {env_path}{RESET}")
        return

    client = AsyncDeepgramClient(api_key=DEEPGRAM_API_KEY)
    print(f"{CYAN}Connecting to Deepgram Flux...{RESET}")

    # NOTE: use async context manager as required by SDK
    async with client.listen.v2.connect(
        model="flux-general-en",
        encoding="linear16",
        sample_rate=SAMPLE_RATE
    ) as conn:

        # Event handler that extracts transcripts and events
        def on_message(msg):
            # msg may include event and transcript attributes depending on payload
            event = getattr(msg, "event", None)
            transcript = getattr(msg, "transcript", None)

            if transcript:
                print_partial(transcript)

            if event == "EndOfTurn" and transcript:
                print_final(transcript.strip())

            if event == "TurnResumed":
                print_barge()

        # Connection lifecycle logging
        conn.on(EventType.OPEN, lambda _: print("⚡ CONNECTION OPEN"))
        conn.on(EventType.CLOSE, lambda _: print("🔴 CONNECTION CLOSED"))
        conn.on(EventType.ERROR, lambda e: print("🔥 ERROR:", e))
        conn.on(EventType.MESSAGE, on_message)

        # Start the websocket listener loop
        asyncio.create_task(conn.start_listening())

        # Give socket a tiny warmup time
        await asyncio.sleep(0.25)
        print(f"{CYAN}🎤 Mic active — Speak into your microphone...{RESET}")

        # Stream microphone in configured chunks
        try:
            with sd.InputStream(
                channels=CHANNELS,
                samplerate=SAMPLE_RATE,
                dtype='int16',
                blocksize=CHUNK_SIZE
            ) as stream:
                while True:
                    audio, _ = stream.read(CHUNK_SIZE)
                    data = audio.tobytes()
                    # Debug: bytes per chunk (should be around CHUNK_SIZE * 2 bytes since int16)
                    try:
                        await conn._send(data)
                    except Exception as e_send:
                        print(f"{RED}Error sending audio chunk: {e_send}{RESET}")
                        # break so the context manager can exit cleanly and show CLOSE
                        break
                    # small optional sleep to avoid tight-loop printing spam on slow terminals
                    await asyncio.sleep(0)
        except Exception as e:
            print(f"{RED}Microphone stream error: {e}{RESET}")

# Entry
if __name__ == "__main__":
    try:
        asyncio.run(run_debug())
    except KeyboardInterrupt:
        print(f"\n{RED}Stopped by user.{RESET}")