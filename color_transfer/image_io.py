"""图片输入输出公共 API。"""

from .image_data import ImageData
from .load_image import ImageLoadError, load_image
from .save_result import ImageSaveError, save_result

__all__ = [
    "ImageData",
    "ImageLoadError",
    "ImageSaveError",
    "load_image",
    "save_result",
]
