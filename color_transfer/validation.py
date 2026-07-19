"""色彩迁移输入与参数校验。"""

import numpy as np


def validate_rgb(image: np.ndarray, name: str) -> np.ndarray:
    """验证非空 uint8 RGB 图片。"""
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError(f"{name}必须是 numpy 数组。")
    if image.size == 0:
        raise ValueError(f"{name}不能为空。")
    if image.dtype != np.uint8:
        raise ValueError(f"{name}必须是 uint8 RGB 图片。")
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(f"{name}必须包含 3 个 RGB 通道。")
    return image


def clipped_parameter(value: float, minimum: float, maximum: float, name: str) -> float:
    """将有限数值参数裁剪到合法范围。"""
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}必须是数值。") from exc
    if not np.isfinite(numeric):
        raise ValueError(f"{name}必须是有限数值。")
    return float(np.clip(numeric, minimum, maximum))
