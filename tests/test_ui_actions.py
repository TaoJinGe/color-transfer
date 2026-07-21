"""界面按钮动作测试。"""

import numpy as np
import pytest
from PIL import Image

from color_transfer.ui.generate_action import generate_result
from color_transfer.ui.reset_action import reset_inputs


def _save(path, color, mode="RGB") -> None:
    Image.new(mode, (8, 6), color).save(path)


def test_generate_returns_preview_and_download(tmp_path) -> None:
    source = tmp_path / "source.png"
    reference = tmp_path / "reference.jpg"
    _save(source, (20, 60, 100, 91), "RGBA")
    _save(reference, (180, 90, 30))
    preview, download = generate_result(source, reference, 0.8, 0.7, 1.0)
    assert preview == download
    with Image.open(download) as result:
        assert result.size == (8, 6)
        assert result.mode == "RGBA"
        assert np.asarray(result)[0, 0, 3] == 91


def test_generate_can_output_jpg_without_alpha(tmp_path) -> None:
    source = tmp_path / "source.png"
    reference = tmp_path / "reference.jpg"
    _save(source, (20, 60, 100, 91), "RGBA")
    _save(reference, (180, 90, 30))
    preview, download = generate_result(source, reference, 0.8, 0.7, 1.0, "JPG")
    assert preview == download
    assert download.endswith(".jpg")
    with Image.open(download) as result:
        assert result.format == "JPEG"
        assert result.mode == "RGB"


@pytest.mark.parametrize(
    ("source", "reference", "message"),
    [(None, "reference.png", "请先上传原图"), ("source.png", None, "请先上传参考图")],
)
def test_generate_requires_both_images(source, reference, message) -> None:
    with pytest.raises(Exception, match=message):
        generate_result(source, reference, 0.8, 0.7, 1.0)


def test_reset_restores_defaults() -> None:
    assert reset_inputs() == (None, None, 1.0, 0.0, 1.0, None, None)
