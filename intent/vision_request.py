import re


_EXPLICIT_VISION_REQUESTS = (
    "what do you see",
    "what can you see",
    "what am i looking at",
    "what is in front of me",
    "what's in front of me",
    "what is around me",
    "what's around me",
    "identify this",
    "identify that",
    "describe this",
    "describe that",
    "describe what you see",
    "read this",
    "read that",
    "read the label",
    "read this label",
    "read the text",
    "read this text",
    "look at this",
    "look at that",
    "take a photo",
    "take a picture",
    "capture a photo",
    "capture a picture",
    "what is in this picture",
    "what's in this picture",
    "what is in this photo",
    "what's in this photo",
    "what is in this image",
    "what's in this image",
)


def is_explicit_vision_request(text: str) -> bool:
    """Return true only for clear requests to inspect the user's current view."""
    normalized = re.sub(r"\s+", " ", text.lower()).strip()
    if re.match(r"^(?:(?:tell me )?how (?:do i|to)|should i|can i|may i)\b", normalized):
        return False
    return any(re.search(rf"\b{re.escape(phrase)}\b", normalized) for phrase in _EXPLICIT_VISION_REQUESTS)
