# main_rpi.py

from __future__ import annotations
from pathlib import Path
import time
import datetime

from helper_functions.camera import capture_image, close_camera
from helper_functions.computer_vision import person_detected
from helper_functions.sensehat import flash_alert, clear


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
IMAGES_DIR = DATA_DIR / "images"

BACKGROUND_PATH = IMAGES_DIR / "background.jpg"
TEST_PATH = IMAGES_DIR / "test.jpg"
INTRUDERS_DIR = IMAGES_DIR / "intruders"


def countdown(seconds: int, message: str) -> None:
    print(message)
    for i in range(seconds, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    print("  Go!\n")


def take_background() -> None:
    countdown(5, "Background photo will be taken in:")
    capture_image(BACKGROUND_PATH)
    print(f"✅ Saved background image: {BACKGROUND_PATH}")


def arm_system(threshold: int, interval_sec: int) -> None:
    if not BACKGROUND_PATH.exists():
        print("⚠️ No background image found. Choose option 1 first.\n")
        return

    countdown(5, "Arming system. Exit camera view in:")

    print("🛡️ Monitoring started. Press CTRL+C to stop.\n")
    clear()

    INTRUDERS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        while True:
            capture_image(TEST_PATH)
            detected, score = person_detected(BACKGROUND_PATH, TEST_PATH, threshold)

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] diff score = {score} (threshold={threshold})")

            if detected:
                print("🚨 INTRUDER DETECTED! 🚨")
                flash_alert(seconds=2.0, blink_hz=4.0)

                # Optional: keep a copy of the image that triggered
                stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                saved = INTRUDERS_DIR / f"intruder_{stamp}.jpg"
                TEST_PATH.replace(saved)  # move test image to intruders folder
                print(f"📸 Saved intruder image: {saved}")

            time.sleep(interval_sec)

    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.\n")
    finally:
        clear()


def get_int(prompt: str, default: int, min_val: int = 1) -> int:
    s = input(f"{prompt} [default={default}]: ").strip()
    if s == "":
        return default
    try:
        v = int(s)
        if v < min_val:
            print(f"Using minimum value {min_val}.")
            return min_val
        return v
    except ValueError:
        print(f"Invalid input. Using default {default}.")
        return default


def main() -> None:
    threshold_t1 = 5_000_000  # Start here, then adjust experimentally
    interval_sec = 2

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    while True:
        print("===== SYSC3010 Lab5 Mini-Project: Home Security System =====")
        print("1) Take new background image (empty room)")
        print("2) Set sensitivity threshold (t1)")
        print("3) Set monitoring interval (X seconds)")
        print("4) Arm system (start monitoring)")
        print("5) Quit")
        choice = input("Select option: ").strip()

        if choice == "1":
            take_background()
            print()

        elif choice == "2":
            threshold_t1 = get_int("Enter threshold t1 (bigger = less sensitive)", threshold_t1, min_val=1)
            print(f"✅ Threshold set to {threshold_t1}\n")

        elif choice == "3":
            interval_sec = get_int("Enter monitoring interval (seconds)", interval_sec, min_val=1)
            print(f"✅ Interval set to {interval_sec} seconds\n")

        elif choice == "4":
            arm_system(threshold_t1, interval_sec)

        elif choice == "5":
            print("Bye!")
            break

        else:
            print("Invalid option.\n")

    close_camera()


if __name__ == "__main__":
    main()
