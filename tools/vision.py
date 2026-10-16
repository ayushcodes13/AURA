import cv2
import os
import platform
from pathlib import Path
import tempfile

def capture_photo():
    """
    Capture a single frame and immediately release the camera.
    No preview. No UI. No async issues.
    """

    runtime_dir = Path(__file__).resolve().parents[1] / ".runtime"
    runtime_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, save_path = tempfile.mkstemp(prefix="aura_photo_", suffix=".jpg", dir=runtime_dir)
    os.close(fd)

    for cam_index in [0, 1, 2, 3]:
        if platform.system() == "Darwin":
            cap = cv2.VideoCapture(cam_index, cv2.CAP_AVFOUNDATION)
        else:
            cap = cv2.VideoCapture(cam_index)

        if not cap.isOpened():
            cap.release()
            continue

        for _ in range(5):
            cap.read()

        ret, frame = cap.read()
        cap.release()

        if ret and frame is not None:
            if cv2.imwrite(save_path, frame):
                return save_path

    try:
        os.remove(save_path)
    except FileNotFoundError:
        pass
    raise RuntimeError("No usable camera found.")
