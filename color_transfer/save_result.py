"""将处理结果安全保存为 PNG 或 JPG。"""

from pathlib import Path

import numpy as np
from PIL import Image


class ImageSaveError(ValueError):
    """表示图片结果无法保存。"""


def save_result(
    rgb: np.ndarray,
    alpha: np.ndarray | None,
    output_path: str | Path,
    output_format: str = "PNG",
) -> str:
    """保存结果并返回文件路径。"""
    _validate_rgb(rgb)
    normalized_format = output_format.upper()
    if normalized_format not in {"PNG", "JPG", "JPEG"}:
        raise ImageSaveError("输出格式仅支持 PNG 或 JPG。")
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image = Image.fromarray(rgb, mode="RGB")
    if alpha is not None and normalized_format == "PNG":
        if alpha.dtype != np.uint8 or alpha.shape != rgb.shape[:2]:
            raise ImageSaveError("透明通道与图片尺寸不一致。")
        image = image.convert("RGBA")
        image.putalpha(Image.fromarray(alpha, mode="L"))
    try:
        if normalized_format == "PNG":
            image.save(destination, format="PNG")
        else:
            image.save(destination, format="JPEG", quality=100, subsampling=0)
    except OSError as exc:
        raise ImageSaveError("结果保存失败。") from exc
    return str(destination.resolve())


def _validate_rgb(rgb: np.ndarray) -> None:
    if not isinstance(rgb, np.ndarray) or rgb.dtype != np.uint8:
        raise ImageSaveError("结果图片必须为 uint8 数组。")
    if rgb.ndim != 3 or rgb.shape[2] != 3 or rgb.size == 0:
        raise ImageSaveError("结果图片必须为非空 RGB 数组。")
