import asyncio

from tts.aura_tts import speak


async def main():
    await speak("Hello Ayush, your AURA text to speech is now working perfectly.")


if __name__ == "__main__":
    asyncio.run(main())
