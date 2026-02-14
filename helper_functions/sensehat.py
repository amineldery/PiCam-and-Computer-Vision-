# helper_functions/sensehat.py

from __future__ import annotations
import time

try:
    from sense_hat import SenseHat
    _sense = SenseHat()
except Exception:
    _sense = None


def clear() -> None:
    if _sense:
        _sense.clear()


def flash_alert(seconds: float = 2.0, blink_hz: float = 4.0) -> None:
    """
    Flash the SenseHAT screen red/blank for the specified time.
    If SenseHAT isn't available, prints an alert instead.
    """
    if not _sense:
        print("[SENSEHAT] ALERT (SenseHAT not detected) 🚨")
        return

    red = (255, 0, 0)
    off = (0, 0, 0)

    period = 1.0 / max(blink_hz, 0.1)
    end_time = time.time() + seconds

    while time.time() < end_time:
        _sense.clear(red)
        time.sleep(period / 2)
        _sense.clear(off)
        time.sleep(period / 2)

    _sense.clear()
