# helper_functions/camera.py

from __future__ import annotations
from pathlib import Path
import time

from picamera2 import Picamera2


_picam2: Picamera2 | None = None


def init_camera(size: tuple[int, int] = (640, 480)) -> Picamera2:
    """
    Initialize and start the Pi camera once, then reuse it.
    """
    global _picam2
    if _picam2 is None:
        _picam2 = Picamera2()
        config = _picam2.create_still_configuration(main={"size": size})
        _picam2.configure(config)
        _picam2.start()
        # Small warm-up helps stabilize exposure/white balance
        time.sleep(0.5)
    return _picam2


def capture_image(save_path: str | Path, size: tuple[int, int] = (640, 480)) -> str:
    """
    Capture a still image and save it to disk.
    Returns the saved path as a string.
    """
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    cam = init_camera(size=size)
    # capture_file writes a JPEG/PNG based on extension
    cam.capture_file(str(save_path))
    return str(save_path)


def close_camera() -> None:
    """
    Stop the camera cleanly.
    """
    global _picam2
    if _picam2 is not None:
        try:
            _picam2.stop()
        except Exception:
            pass
        _picam2 = None
