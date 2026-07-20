"""迭代式三维颜色概率分布迁移。"""

import numpy as np

from .color_space import perceptual_to_rgb, rgb_to_perceptual
from .color_lut import apply_lut, apply_lut_in_chunks, identity_lut, smooth_lut
from .gamut import compress_perceptual_gamut
from .quantile_mapping import apply_quantile_map, learn_quantile_map
from .rotations import orthogonal_rotations

SAMPLE_LIMIT = 100_000
DEFAULT_ITERATIONS = 12
DEFAULT_SEED = 20260720


def transfer_distribution(
    source_rgb: np.ndarray,
    reference_rgb: np.ndarray,
    iterations: int = DEFAULT_ITERATIONS,
    seed: int = DEFAULT_SEED,
) -> np.ndarray:
    """将原图完整颜色分布迭代映射到参考图。"""
    source_space = rgb_to_perceptual(source_rgb)
    source_pixels = source_space.reshape(-1, 3)
    original_sample = _sample_rows(source_pixels, SAMPLE_LIMIT).copy()
    source_sample = original_sample.copy()
    reference_sample = rgb_to_perceptual(_sample_rgb(reference_rgb, SAMPLE_LIMIT)).reshape(-1, 3)
    lut = identity_lut()
    for rotation in orthogonal_rotations(iterations, seed):
        maps = _learn_rotated_maps(source_sample, reference_sample, rotation)
        source_sample = _apply_rotation(source_sample, rotation, maps)
        lut[:] = _apply_rotation(lut.reshape(-1, 3), rotation, maps).reshape(lut.shape)
    smooth_lut(lut)
    _correct_lut_distribution(lut, original_sample, reference_sample, seed + iterations)
    apply_lut_in_chunks(source_pixels, lut)
    compressed = compress_perceptual_gamut(source_pixels)
    rgb_float = perceptual_to_rgb(compressed.reshape(source_space.shape))
    return np.clip(np.rint(rgb_float * 255.0), 0, 255).astype(np.uint8)


def _learn_rotated_maps(source: np.ndarray, reference: np.ndarray, rotation: np.ndarray):
    source_rotated = source @ rotation
    reference_rotated = reference @ rotation
    return tuple(
        learn_quantile_map(source_rotated[:, axis], reference_rotated[:, axis])
        for axis in range(3)
    )


def _apply_rotation(values: np.ndarray, rotation: np.ndarray, maps) -> np.ndarray:
    rotated = values @ rotation
    for axis, mapping in enumerate(maps):
        rotated[:, axis] = apply_quantile_map(rotated[:, axis], mapping)
    return rotated @ rotation.T


def _sample_rows(values: np.ndarray, limit: int) -> np.ndarray:
    if values.shape[0] <= limit:
        return values
    indices = np.linspace(0, values.shape[0] - 1, limit, dtype=np.int64)
    return values[indices]


def _correct_lut_distribution(
    lut: np.ndarray, source: np.ndarray, reference: np.ndarray, seed: int
) -> None:
    """沿多个方向修正 LUT 插值造成的分布误差。"""
    lut_values = lut.reshape(-1, 3)
    for rotation in orthogonal_rotations(4, seed):
        sample = apply_lut(source, lut)
        maps = _learn_rotated_maps(sample, reference, rotation)
        lut_values[:] = _apply_rotation(lut_values, rotation, maps)


def _sample_rgb(rgb: np.ndarray, limit: int) -> np.ndarray:
    pixels = rgb.reshape(-1, 3)
    return _sample_rows(pixels, limit).reshape(-1, 1, 3)
