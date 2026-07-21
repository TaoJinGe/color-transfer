"""图片读取与保存测试。"""

from io import BytesIO

import numpy as np
import pytest
from PIL import Image

from color_transfer.image_io import ImageLoadError, load_image, save_result


def _image_bytes(mode: str, size: tuple[int, int], fmt: str) -> BytesIO:
    image = Image.new(mode, size, 128 if mode == "L" else (10, 20, 30, 77))
    stream = BytesIO()
    image.save(stream, format=fmt)
    stream.seek(0)
    return stream


@pytest.mark.parametrize("fmt", ["JPEG", "PNG", "WEBP"])
def test_load_supported_formats(fmt: str) -> None:
    stream = _image_bytes("RGB", (7, 5), fmt)
    data = load_image(stream)
    assert data.rgb.shape == (5, 7, 3)
    assert data.rgb.dtype == np.uint8


def test_load_grayscale_as_rgb() -> None:
    data = load_image(_image_bytes("L", (4, 3), "PNG"))
    assert data.rgb.shape == (3, 4, 3)
    assert np.array_equal(data.rgb[..., 0], data.rgb[..., 1])


def test_exif_orientation_is_applied() -> None:
    image = Image.new("RGB", (7, 3), (10, 20, 30))
    exif = Image.Exif()
    exif[274] = 6
    stream = BytesIO()
    image.save(stream, format="JPEG", exif=exif)
    stream.seek(0)
    data = load_image(stream)
    assert (data.width, data.height) == (3, 7)


def test_preserve_alpha_when_saving(tmp_path) -> None:
    data = load_image(_image_bytes("RGBA", (6, 4), "PNG"))
    output = save_result(data.rgb, data.alpha, tmp_path / "result.png")
    with Image.open(output) as saved:
        assert saved.mode == "RGBA"
        assert saved.size == (6, 4)
        assert np.asarray(saved)[0, 0, 3] == 77


def test_save_rgb_as_png(tmp_path) -> None:
    rgb = np.full((3, 5, 3), 42, dtype=np.uint8)
    output = save_result(rgb, None, tmp_path / "nested" / "result.png")
    with Image.open(output) as saved:
        assert saved.format == "PNG"
        assert saved.size == (5, 3)


def test_save_alpha_image_as_opaque_jpg(tmp_path) -> None:
    rgb = np.full((3, 5, 3), 42, dtype=np.uint8)
    alpha = np.zeros((3, 5), dtype=np.uint8)
    output = save_result(rgb, alpha, tmp_path / "result.jpg", "JPG")
    with Image.open(output) as saved:
        assert saved.format == "JPEG"
        assert saved.mode == "RGB"
        assert saved.size == (5, 3)


@pytest.mark.parametrize("payload", [b"broken", b"", None])
def test_reject_invalid_images(payload) -> None:
    value = None if payload is None else BytesIO(payload)
    with pytest.raises(ImageLoadError, match="图片读取失败"):
        load_image(value)


def test_reject_unsupported_format() -> None:
    with pytest.raises(ImageLoadError, match="不支持"):
        load_image(_image_bytes("RGB", (2, 2), "BMP"))
