import asyncio
import os
from dotenv import load_dotenv
from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType

load_dotenv(os.path.join("config", ".env"))
API_KEY = os.getenv("DEEPGRAM_API_KEY")


async def test_deepgram():
    client = AsyncDeepgramClient(api_key=API_KEY)

    print("Trying to open a Deepgram Flux WS connection...")

    async with client.listen.v2.connect(
        model="flux-general-en",
        encoding="linear16",
        sample_rate=16000
    ) as conn:

        conn.on(EventType.OPEN, lambda _: print("⚡ OPEN"))
        conn.on(EventType.ERROR, lambda e: print("🔥 ERROR", e))
        conn.on(EventType.CLOSE, lambda _: print("🔴 CLOSED"))

        # Try for 2 seconds
        await asyncio.sleep(2)
        print("Done.")

asyncio.run(test_deepgram())




import sys
print("EXECUTABLE:", sys.executable)
print("VERSION:", sys.version)