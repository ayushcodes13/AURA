import asyncio
import sounddevice as sd
from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
import os
from dotenv import load_dotenv
from chimes.aura_chimes import AuraChimes
chimes = AuraChimes()

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_MS = 80
CHUNK_SIZE = int(SAMPLE_RATE * (CHUNK_MS / 1000))

class AuraFluxSTT:
    """
    A wrapper around your working Flux code so the rest of AURA can call:
        await stt.listen_once()
    """

    def __init__(self):
        env_path = os.path.join(os.path.dirname(__file__), "../config/.env")
        load_dotenv(env_path)

        self.api_key = os.getenv("DEEPGRAM_API_KEY")
        if not self.api_key:
            raise RuntimeError("DEEPGRAM_API_KEY missing in config/.env")

        self.client = AsyncDeepgramClient(api_key=self.api_key)
        self.connection_ctx = None
        self.connection = None

        self.final_text = None
        self.partial_text = None
        self.turn_done = asyncio.Event()

    async def connect(self):
        """Connect once and keep the socket alive."""
        if self.connection:
            return  # already connected

        self.connection_ctx = self.client.listen.v2.connect(
            model="flux-general-en",
            encoding="linear16",
            sample_rate=SAMPLE_RATE
        )

        self.connection = await self.connection_ctx.__aenter__()

        # Register handlers
        self.connection.on(EventType.MESSAGE, self._handle_msg)
        self.connection.on(EventType.ERROR, lambda e: print("Flux error:", e))

        asyncio.create_task(self.connection.start_listening())
        await asyncio.sleep(0.2)

    def _handle_msg(self, msg):
        event = getattr(msg, "event", None)
        transcript = getattr(msg, "transcript", None)

        if transcript:
            self.partial_text = transcript
            print(f"\r[PARTIAL]: {transcript}", end="", flush=True)

        if event == "EndOfTurn":
            self.final_text = transcript.strip()
            self.turn_done.set()

        if event == "TurnResumed":
            print("User interrupted")
            chimes.play("interrupt")

    async def listen_once(self):
        """
        Records ONE user utterance and returns final text.
        This is what main.py will call each turn.
        """

        await self.connect()

        self.final_text = None
        self.turn_done.clear()

        # Start mic stream
        with sd.InputStream(
            channels=CHANNELS,
            samplerate=SAMPLE_RATE,
            dtype="int16",
            blocksize=CHUNK_SIZE
        ) as stream:
            while True:
                audio, _ = stream.read(CHUNK_SIZE)
                await self.connection._send(audio.tobytes())

                # if speech ended
                if self.turn_done.is_set():
                    break

                await asyncio.sleep(0)

        return self.final_text