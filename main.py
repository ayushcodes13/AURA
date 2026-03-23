import asyncio
import time
import os
from wakeword.aura_wakeword import listen_for_wake_word
from stt.aura_flux_stt import AuraFluxSTT
from intent.aura_intent import AuraIntentRouter
from tools.executor import AuraToolExecutor
from tts.aura_tts import speak
from chimes.aura_chimes import AuraChimes
chimes = AuraChimes()

async def main():

    print("✨ AURA BOOTING…")
    router = AuraIntentRouter()
    executor = AuraToolExecutor()

    stt = AuraFluxSTT()
    print("✨ AURA READY — waiting for wakeword…")

    while True:
        
        listen_for_wake_word()
        print("\n🔵 Session Started - AURA listening continuously...")
        chimes.play("wake")

        user_query = await stt.listen_once()
        if not user_query:
            print("❌ No speech detected.")
            continue
        print(f"[USER]: {user_query}")
        chimes.play("thinking_start")

        intent = router.route(user_query)
        print(f"[INTENT]: {intent}")

        result = executor.execute(intent, user_query)
        print(f"[AURA RESULT]: {result['text']}")

        chimes.play("response_start")
        await speak(result['text'])
        
        print("\n✨ AURA listening again…\n")
        await asyncio.sleep(0.2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down AURA…")