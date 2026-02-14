# helper_functions/computer_vision.py

from __future__ import annotations
from pathlib import Path

import numpy as np
from PIL import Image


def load_image_as_gray_array(image_path: str | Path) -> np.ndarray:
    """
    Load image as grayscale numpy array (dtype=int32) for safe subtraction.
    """
    img = Image.open(str(image_path)).convert("L")  # L = grayscale
    arr = np.array(img, dtype=np.int32)
    return arr


def image_difference_score(background_path: str | Path, test_path: str | Path) -> int:
    """
    Compute sum of absolute pixel differences between background and test image.
    Larger score => more change in scene.
    """
    bg = load_image_as_gray_array(background_path)
    test = load_image_as_gray_array(test_path)

    # Ensure same size (if not, compare only overlapping area)
    h = min(bg.shape[0], test.shape[0])
    w = min(bg.shape[1], test.shape[1])
    bg = bg[:h, :w]
    test = test[:h, :w]

    diff = np.abs(test - bg)
    score = int(np.sum(diff))
    return score


def person_detected(background_path: str | Path, test_path: str | Path, threshold_t1: int) -> tuple[bool, int]:
    """
    Returns (detected, score).
    detected is True if score > threshold_t1.
    """
    score = image_difference_score(background_path, test_path)
    return (score > threshold_t1), score
