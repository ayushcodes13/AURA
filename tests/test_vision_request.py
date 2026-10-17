import unittest

from intent.vision_request import is_explicit_vision_request


class VisionRequestTests(unittest.TestCase):
    def test_explicit_visual_requests(self):
        requests = (
            "What do you see?",
            "Please read this label.",
            "Take a picture of the item.",
            "What's in this photo?",
            "Look at that.",
        )
        for request in requests:
            with self.subTest(request=request):
                self.assertTrue(is_explicit_vision_request(request))

    def test_nonvisual_requests_do_not_directly_open_camera(self):
        requests = (
            "Is it hot in here?",
            "Can you see if my package was delivered?",
            "Tell me how to take a photo.",
            "How do I read a label?",
            "Should I take a photo?",
            "I will look at the instructions later.",
            "What is the weather around me?",
            "What is this process?",
            "What's this word mean?",
        )
        for request in requests:
            with self.subTest(request=request):
                self.assertFalse(is_explicit_vision_request(request))


if __name__ == "__main__":
    unittest.main()
