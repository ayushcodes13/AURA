import os

from tools.vision import capture_photo
from llm.provider import LLMProvider

class AuraToolExecutor:
    """
    Runs tools and sends results to Groq.
    """

    def __init__(self):
        self.provider = LLMProvider()

    # --------------------------
    # NORMAL TEXT HANDLING
    # --------------------------
    def answer_with_llm(self, user_query: str) -> str:
        system_prompt = (
            "You are AURA (Adaptive Understanding and Response Assistant).\n\n"

            "You are a voice-based assistive system designed for elderly users,"
            "visually impaired individuals, and people with low literacy.\n\n"

            "Your purpose is to reduce confusion and increase independence.\n"
            "You are calm, steady, and reassuring.\n\n"

            "Speak clearly. Use short sentences.\n"
            "Avoid technical language.\n"
            "Do not sound corporate or robotic.\n"
            "Respond like a steady companion.\n\n"

            "If asked about your purpose, say:\n"
            "\"I am AURA, a helpful assistant who can see the world around you and "
            "support you in daily life.\"\n\n"

            "Never mention internal tools, routing, models, or implementation details.\n\n"

            "If the user asks about their surroundings or physical environment "
            "and no image is provided, say that you need to look first."
        )

        print("\n🔵 AURA (streaming): ", end="", flush=True)

        final_text = ""

        for chunk in self.provider.generate_text_stream(system_prompt, user_query):
            print(chunk, end="", flush=True)
            final_text += chunk

        print("\n")
        return final_text.strip()

    # --------------------------
    # TOOL EXECUTION
    # --------------------------
    def execute(self, intent_result: dict, user_query: str) -> dict:

        if intent_result["type"] == "normal":
            answer = self.answer_with_llm(user_query)
            return {"type": "text", "text": answer}

        tool_name = intent_result.get("tool_name")

        if tool_name == "capture_photo":
            img_path = capture_photo()

            try:
                final_text = self.provider.generate_vision(user_query, img_path)
                return {"type": "text", "text": final_text}
            finally:
                try:
                    os.remove(img_path)
                except FileNotFoundError:
                    pass

        return {"type": "text", "text": "I couldn't complete that request."}
