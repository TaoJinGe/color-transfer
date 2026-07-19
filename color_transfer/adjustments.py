"""结果图片饱和度调整。"""

import cv2
import numpy as np


def adjust_saturation(rgb: np.ndarray, saturation: float) -> np.ndarray:
    """按倍率调整 RGB 图片饱和度。"""
    if saturation == 1.0:
        return rgb.copy()
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[..., 1] = np.clip(hsv[..., 1] * saturation, 0.0, 255.0)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
