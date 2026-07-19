"""生成结果按钮动作。"""

from pathlib import Path

import gradio as gr

from ..core import transfer_color_lab
from ..image_io import ImageLoadError, ImageSaveError, load_image, save_result
from ..result_store import result_path


def generate_result(
    source_path: str | Path | None,
    reference_path: str | Path | None,
    strength: float,
    luminance_protection: float,
    saturation: float,
) -> tuple[str, str]:
    """读取两张图片并生成可预览、可下载的结果。"""
    if not source_path:
        raise gr.Error("请先上传原图。")
    if not reference_path:
        raise gr.Error("请先上传参考图。")
    try:
        source = load_image(source_path)
        reference = load_image(reference_path)
        result = transfer_color_lab(
            source.rgb,
            reference.rgb,
            strength,
            luminance_protection,
            saturation,
        )
        saved = save_result(result, source.alpha, result_path())
    except (ImageLoadError, ImageSaveError, ValueError) as exc:
        raise gr.Error(str(exc)) from exc
    except MemoryError as exc:
        raise gr.Error("图片尺寸过大，请使用较小图片重试。") from exc
    except Exception as exc:
        raise gr.Error("处理失败，请尝试其他图片。") from exc
    return saved, saved
