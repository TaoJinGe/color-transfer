"""本次进程临时结果文件管理。"""

import atexit
import shutil
import tempfile
from pathlib import Path

_RESULT_DIRECTORY = Path(tempfile.mkdtemp(prefix="color_transfer_v1_"))
atexit.register(shutil.rmtree, _RESULT_DIRECTORY, ignore_errors=True)


def result_path(output_format: str = "PNG") -> Path:
    """返回固定下载文件名的进程级临时路径。"""
    suffix = ".jpg" if output_format.upper() in {"JPG", "JPEG"} else ".png"
    return _RESULT_DIRECTORY / f"color_transfer_result{suffix}"
