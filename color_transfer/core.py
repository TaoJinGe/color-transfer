"""公开色彩迁移接口编排。"""

import numpy as np

from .adjustments import adjust_saturation
from .color_space import perceptual_to_rgb, rgb_to_perceptual
from .distribution_transfer import transfer_distribution
from .validation import clipped_parameter, validate_rgb


def transfer_color_distribution(
    source_rgb: np.ndarray,
    reference_rgb: np.ndarray,
    strength: float = 1.0,
    luminance_protection: float = 0.0,
    saturation: float = 1.0,
) -> np.ndarray:
    """将原图的完整颜色分布迭代迁移为参考图配色。"""
    source = validate_rgb(source_rgb, "原图")
    reference = validate_rgb(reference_rgb, "参考图")
    strength_value = clipped_parameter(strength, 0.0, 1.0, "色彩迁移强度")
    luminance_value = clipped_parameter(luminance_protection, 0.0, 1.0, "亮度保护")
    saturation_value = clipped_parameter(saturation, 0.0, 2.0, "饱和度")
    if strength_value == 0.0 and saturation_value == 1.0:
        return source.copy()
    if source.shape == reference.shape and np.array_equal(source, reference):
        transferred = source.copy()
    else:
        transferred = transfer_distribution(source, reference)
    if luminance_value > 0.0:
        transferred = _protect_luminance(source, transferred, luminance_value)
    blended = cv_blend(source, transferred, strength_value)
    return adjust_saturation(blended, saturation_value)


def transfer_color_lab(
    source_rgb: np.ndarray,
    reference_rgb: np.ndarray,
    strength: float = 1.0,
    luminance_protection: float = 0.0,
    saturation: float = 1.0,
) -> np.ndarray:
    """兼容旧调用名称；内部使用新的完整分布迁移。"""
    return transfer_color_distribution(
        source_rgb, reference_rgb, strength, luminance_protection, saturation
    )


def cv_blend(source: np.ndarray, transferred: np.ndarray, strength: float) -> np.ndarray:
    """以稳定浮点运算混合原图和迁移图。"""
    mixed = source.astype(np.float32) * (1.0 - strength)
    mixed += transferred.astype(np.float32) * strength
    return np.clip(np.rint(mixed), 0, 255).astype(np.uint8)


def _protect_luminance(source: np.ndarray, transferred: np.ndarray, amount: float) -> np.ndarray:
    source_space = rgb_to_perceptual(source)
    result_space = rgb_to_perceptual(transferred)
    result_space[..., 0] = source_space[..., 0] * amount + result_space[..., 0] * (1.0 - amount)
    rgb = perceptual_to_rgb(result_space)
    return np.clip(np.rint(rgb * 255.0), 0, 255).astype(np.uint8)
