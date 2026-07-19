"""Lab 空间颜色统计迁移。"""

import cv2
import numpy as np

EPSILON = 1e-6
STATISTICS_MAX_EDGE = 1600


def transfer_lab_statistics(
    source_rgb: np.ndarray,
    reference_rgb: np.ndarray,
    luminance_protection: float,
) -> np.ndarray:
    """将参考图的 Lab 统计映射到原图。"""
    source_lab = cv2.cvtColor(source_rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    source_stats = cv2.cvtColor(_statistics_sample(source_rgb), cv2.COLOR_RGB2LAB)
    reference_stats = cv2.cvtColor(_statistics_sample(reference_rgb), cv2.COLOR_RGB2LAB)
    source_mean, source_std = _channel_statistics(source_stats)
    reference_mean, reference_std = _channel_statistics(reference_stats)
    safe_std = np.maximum(source_std, EPSILON)
    mapped = (source_lab - source_mean) * (reference_std / safe_std) + reference_mean
    mapped = np.clip(mapped, 0.0, 255.0)
    mapped[..., 0] = (
        source_lab[..., 0] * luminance_protection
        + mapped[..., 0] * (1.0 - luminance_protection)
    )
    return cv2.cvtColor(mapped.astype(np.uint8), cv2.COLOR_LAB2RGB)


def _statistics_sample(rgb: np.ndarray) -> np.ndarray:
    height, width = rgb.shape[:2]
    longest = max(height, width)
    if longest <= STATISTICS_MAX_EDGE:
        return rgb
    scale = STATISTICS_MAX_EDGE / longest
    size = (max(1, round(width * scale)), max(1, round(height * scale)))
    return cv2.resize(rgb, size, interpolation=cv2.INTER_AREA)


def _channel_statistics(lab: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pixels = lab.reshape(-1, 3).astype(np.float32)
    return pixels.mean(axis=0), pixels.std(axis=0)
