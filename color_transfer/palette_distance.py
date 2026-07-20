"""确定性 Sliced Wasserstein 配色距离。"""

import numpy as np

from .color_space import rgb_to_perceptual
from .rotations import orthogonal_rotations

DISTANCE_SAMPLE_LIMIT = 50_000


def sliced_wasserstein_distance(
    first_rgb: np.ndarray,
    second_rgb: np.ndarray,
    directions: int = 32,
    seed: int = 20260720,
) -> float:
    """计算两张图片在多个固定颜色投影上的平均分位数距离。"""
    first = _sample(rgb_to_perceptual(first_rgb).reshape(-1, 3))
    second = _sample(rgb_to_perceptual(second_rgb).reshape(-1, 3))
    distances: list[float] = []
    for rotation in orthogonal_rotations(directions, seed):
        for axis in range(3):
            direction = rotation[:, axis]
            distances.append(_quantile_distance(first @ direction, second @ direction))
    return float(np.mean(distances))


def _quantile_distance(first: np.ndarray, second: np.ndarray) -> float:
    quantiles = np.linspace(0.01, 0.99, 99)
    first_q = np.quantile(first, quantiles)
    second_q = np.quantile(second, quantiles)
    return float(np.mean(np.abs(first_q - second_q)))


def _sample(values: np.ndarray) -> np.ndarray:
    if values.shape[0] <= DISTANCE_SAMPLE_LIMIT:
        return values
    indices = np.linspace(0, values.shape[0] - 1, DISTANCE_SAMPLE_LIMIT, dtype=np.int64)
    return values[indices]
