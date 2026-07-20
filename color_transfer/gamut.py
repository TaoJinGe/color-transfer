"""迁移结果的平滑色域压缩。"""

import numpy as np


def compress_perceptual_gamut(values: np.ndarray) -> np.ndarray:
    """围绕中点缩放越界颜色，避免逐通道硬裁剪。"""
    pixels = np.asarray(values, dtype=np.float32)
    minimum = pixels.min(axis=1)
    maximum = pixels.max(axis=1)
    lower_scale = np.where(minimum < 0.0, 1.0 - 2.0 * minimum, 1.0)
    upper_scale = np.where(maximum > 1.0, 2.0 * maximum - 1.0, 1.0)
    scale = np.maximum.reduce([np.ones_like(minimum), lower_scale, upper_scale])
    compressed = 0.5 + (pixels - 0.5) / scale[:, None]
    return np.clip(compressed, 0.0, 1.0)
