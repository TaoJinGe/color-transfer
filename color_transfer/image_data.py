"""统一图片数据结构。"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class ImageData:
    """保存标准 RGB 像素及可选透明通道。"""

    rgb: np.ndarray
    alpha: np.ndarray | None
    width: int
    height: int
    source_format: str | None
