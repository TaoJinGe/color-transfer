"""公开色彩迁移接口编排。"""

import numpy as np

from .adjustments import adjust_saturation
from .lab_transfer import transfer_lab_statistics
from .validation import clipped_parameter, validate_rgb


def transfer_color_lab(
    source_rgb: np.ndarray,
    reference_rgb: np.ndarray,
    strength: float = 0.8,
    luminance_protection: float = 0.7,
    saturation: float = 1.0,
) -> np.ndarray:
    """将参考图的整体色彩统计迁移到原图。"""
    source = validate_rgb(source_rgb, "原图")
    reference = validate_rgb(reference_rgb, "参考图")
    strength_value = clipped_parameter(strength, 0.0, 1.0, "色彩迁移强度")
    luminance_value = clipped_parameter(luminance_protection, 0.0, 1.0, "亮度保护")
    saturation_value = clipped_parameter(saturation, 0.0, 2.0, "饱和度")
    if strength_value == 0.0 and saturation_value == 1.0:
        return source.copy()
    transferred = transfer_lab_statistics(source, reference, luminance_value)
    blended = cv_blend(source, transferred, strength_value)
    return adjust_saturation(blended, saturation_value)


def cv_blend(source: np.ndarray, transferred: np.ndarray, strength: float) -> np.ndarray:
    """以稳定浮点运算混合原图和迁移图。"""
    mixed = source.astype(np.float32) * (1.0 - strength)
    mixed += transferred.astype(np.float32) * strength
    return np.clip(np.rint(mixed), 0, 255).astype(np.uint8)
