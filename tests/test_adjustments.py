"""饱和度调整测试。"""

import cv2
import numpy as np

from color_transfer.adjustments import adjust_saturation


def _mean_saturation(rgb: np.ndarray) -> float:
    return float(cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)[..., 1].mean())


def test_zero_saturation_is_grayscale() -> None:
    rgb = np.array([[[220, 50, 20], [10, 180, 70]]], dtype=np.uint8)
    result = adjust_saturation(rgb, 0.0)
    assert np.max(np.ptp(result.astype(np.int16), axis=2)) <= 1


def test_default_saturation_preserves_pixels() -> None:
    rgb = np.array([[[20, 80, 140]]], dtype=np.uint8)
    assert np.array_equal(adjust_saturation(rgb, 1.0), rgb)


def test_enhanced_saturation_increases_mean() -> None:
    rgb = np.array([[[100, 130, 150], [80, 110, 100]]], dtype=np.uint8)
    assert _mean_saturation(adjust_saturation(rgb, 2.0)) > _mean_saturation(rgb)
