"""RGB 与归一化感知 Lab 颜色空间转换。"""

import cv2
import numpy as np


def rgb_to_perceptual(rgb: np.ndarray) -> np.ndarray:
    """将 uint8 RGB 转为三个轴尺度接近的 float32 Lab。"""
    lab = cv2.cvtColor(rgb.astype(np.float32) / 255.0, cv2.COLOR_RGB2LAB)
    normalized = np.empty_like(lab, dtype=np.float32)
    normalized[..., 0] = lab[..., 0] / 100.0
    normalized[..., 1] = (lab[..., 1] + 128.0) / 255.0
    normalized[..., 2] = (lab[..., 2] + 128.0) / 255.0
    return normalized


def perceptual_to_rgb(perceptual: np.ndarray) -> np.ndarray:
    """将归一化 float32 Lab 转回 float32 RGB。"""
    lab = np.empty_like(perceptual, dtype=np.float32)
    lab[..., 0] = perceptual[..., 0] * 100.0
    lab[..., 1] = perceptual[..., 1] * 255.0 - 128.0
    lab[..., 2] = perceptual[..., 2] * 255.0 - 128.0
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
