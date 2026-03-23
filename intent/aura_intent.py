
from llm.provider import LLMProvider

VISION_KEYWORDS = [
    "see", "look", "show", "view",
    "picture", "photo", "image",
    "camera", "front of me",
    "what do you see", "what is in front of me",
    "around me", "here", "this place"
]

provider = LLMProvider()
class AuraIntentRouter:
    def __init__(self):
        self.router_prompt = (
            "You are AURA’s intent router.\n\n"

            "Your task: decide if the user request requires vision.\n\n"

            "You must choose EXACTLY ONE of the following:\n"
            "1) Call function capture_photo\n"
            "2) Return a normal text response\n\n"

            "Call capture_photo ONLY if the user is asking about:\n"
            "- Their physical surroundings\n"
            "- Objects, people, or environment near them\n"
            "- What is in front of them or around them\n"
            "- Anything that requires real-world visual observation\n\n"

            "Use semantic understanding. Do not rely on keywords.\n\n"

            "Rules:\n"
            "- If vision is required, you MUST call capture_photo.\n"
            "- If vision is NOT required, return normal.\n"
            "- Never answer in text when vision is required.\n"
            "- Never describe an image yourself.\n"
            "- Never mix text with a tool call.\n"

                )

    def route(self, text: str):
        text_l = text.lower()
        for keyword in VISION_KEYWORDS:
            if keyword in text_l:
                return {
                    "type": "tool_call",
                    "tool_name": "capture_photo",
                    "args": {}
                }
        return provider.classify_intent(self.router_prompt, text)