import os
from groq import Groq
from dotenv import load_dotenv
from PIL import Image
import base64
from io import BytesIO

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, "config", ".env"))

class LLMProvider:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is missing. Set it in config/.env or the environment.")

        self.client = Groq(api_key=api_key)
        self.text_model = "llama-3.3-70b-versatile"  
        self.vision_model = "meta-llama/llama-4-maverick-17b-128e-instruct"
        
        # --------------------------------------------------
    # INTENT CLASSIFICATION
    # --------------------------------------------------
    def classify_intent(self, system_prompt: str, user_query: str) -> dict:
        completion = self.client.chat.completions.create(
            model=self.text_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            temperature=0,
        )

        response_text = completion.choices[0].message.content.strip().lower()

        if "capture_photo" in response_text:
            return {
                "type": "tool_call",
                "tool_name": "capture_photo",
                "args": {}
            }

        return {
            "type": "normal"
        }

    # --------------------------------------------------
    # TEXT GENERATION (Streaming)
    # --------------------------------------------------
    def generate_text_stream(self, system_prompt: str, user_query: str):
        completion = self.client.chat.completions.create(
            model=self.text_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            temperature=0.4,
            stream=True,
        )

        for chunk in completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    # --------------------------------------------------
    # TEXT GENERATION (Non-stream)
    # --------------------------------------------------
    def generate_text(self, system_prompt: str, user_query: str) -> str:
        completion = self.client.chat.completions.create(
            model=self.text_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            temperature=0.4,
        )

        return completion.choices[0].message.content.strip()

    # --------------------------------------------------
    # IMAGE TO BASE64
    # --------------------------------------------------
    def _image_to_base64(self, image_path: str) -> str:
        with Image.open(image_path) as img:
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")

    # --------------------------------------------------
    # VISION GENERATION
    # --------------------------------------------------
    def generate_vision(self, user_query: str, image_path: str) -> str:
        image_base64 = self._image_to_base64(image_path)

        completion = self.client.chat.completions.create(
            model=self.vision_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"User asked: {user_query}. Describe clearly what you see."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ],
                }
            ],
            temperature=0.3,
        )

        return completion.choices[0].message.content.strip()
