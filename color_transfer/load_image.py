"""安全读取并标准化本地图片。"""

from pathlib import Path
from typing import BinaryIO

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError

from .image_data import ImageData

SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}
MAX_PIXELS = 50_000_000


class ImageLoadError(ValueError):
    """表示用户可理解的图片读取错误。"""


def load_image(path_or_file: str | Path | BinaryIO) -> ImageData:
    """读取图片、纠正 EXIF、识别 Alpha 并转换为统一格式。"""
    if path_or_file is None:
        raise ImageLoadError("图片读取失败，请更换文件。")
    try:
        with Image.open(path_or_file) as opened:
            source_format = opened.format
            if source_format not in SUPPORTED_FORMATS:
                raise ImageLoadError("不支持该图片格式，请使用 JPG、PNG 或 WEBP。")
            if opened.width * opened.height > MAX_PIXELS:
                raise ImageLoadError("图片尺寸过大，请使用较小图片重试。")
            oriented = ImageOps.exif_transpose(opened)
            alpha = _extract_alpha(oriented)
            rgb = np.asarray(oriented.convert("RGB"), dtype=np.uint8).copy()
    except ImageLoadError:
        raise
    except (UnidentifiedImageError, OSError, ValueError, TypeError) as exc:
        raise ImageLoadError("图片读取失败，请更换文件。") from exc
    return ImageData(
        rgb=rgb,
        alpha=alpha,
        width=rgb.shape[1],
        height=rgb.shape[0],
        source_format=source_format,
    )


def _extract_alpha(image: Image.Image) -> np.ndarray | None:
    if "A" not in image.getbands() and "transparency" not in image.info:
        return None
    return np.asarray(image.convert("RGBA").getchannel("A"), dtype=np.uint8).copy()
