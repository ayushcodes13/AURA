import cv2
import time

def capture_photo():
    """
    Capture a single frame and immediately release the camera.
    No preview. No UI. No async issues.
    """

    save_path = f"/tmp/aura_photo_{int(time.time())}.jpg"

    for cam_index in [0, 1, 2, 3]:
        cap = cv2.VideoCapture(cam_index, cv2.CAP_AVFOUNDATION)

        if not cap.isOpened():
            continue

        for _ in range(5):
            cap.read()

        ret, frame = cap.read()
        cap.release()

        if ret and frame is not None:
            cv2.imwrite(save_path, frame)
            return save_path

    raise RuntimeError("No usable camera found.")