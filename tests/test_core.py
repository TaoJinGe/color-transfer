"""Lab 色彩迁移公开接口测试。"""

import cv2
import numpy as np
import pytest

from color_transfer.core import transfer_color_lab


def _gradient(height: int = 24, width: int = 32) -> np.ndarray:
    x = np.linspace(0, 255, width, dtype=np.uint8)
    y = np.linspace(0, 255, height, dtype=np.uint8)[:, None]
    return np.stack(np.broadcast_arrays(x, y, ((x[None, :] // 2 + y // 2))), axis=2)


def test_result_shape_type_and_range() -> None:
    source = _gradient()
    reference = np.full((9, 13, 3), [180, 80, 40], dtype=np.uint8)
    result = transfer_color_lab(source, reference)
    assert result.shape == source.shape
    assert result.dtype == np.uint8
    assert result.min() >= 0 and result.max() <= 255


def test_zero_strength_returns_source() -> None:
    source = _gradient()
    reference = np.full((4, 7, 3), [10, 200, 30], dtype=np.uint8)
    assert np.array_equal(transfer_color_lab(source, reference, strength=0), source)


def test_full_strength_is_affected_by_reference() -> None:
    source = _gradient()
    reference = np.full((8, 8, 3), [200, 40, 20], dtype=np.uint8)
    result = transfer_color_lab(source, reference, strength=1, luminance_protection=0)
    assert np.mean(np.abs(result.astype(float) - source.astype(float))) > 10


def test_parameters_are_clipped() -> None:
    source = _gradient()
    reference = np.flip(source, axis=2).copy()
    clipped = transfer_color_lab(source, reference, 1, 0, 2)
    outside = transfer_color_lab(source, reference, 5, -3, 7)
    assert np.array_equal(clipped, outside)


def test_luminance_protection_keeps_source_luminance_closer() -> None:
    source = np.full((10, 10, 3), 180, dtype=np.uint8)
    reference = np.full((10, 10, 3), 30, dtype=np.uint8)
    protected = transfer_color_lab(source, reference, 1, 1)
    unprotected = transfer_color_lab(source, reference, 1, 0)
    source_l = cv2.cvtColor(source, cv2.COLOR_RGB2LAB)[..., 0].mean()
    protected_l = cv2.cvtColor(protected, cv2.COLOR_RGB2LAB)[..., 0].mean()
    unprotected_l = cv2.cvtColor(unprotected, cv2.COLOR_RGB2LAB)[..., 0].mean()
    assert abs(protected_l - source_l) < abs(unprotected_l - source_l)


@pytest.mark.parametrize("value", [0, 255])
def test_black_and_white_images_do_not_crash(value: int) -> None:
    source = np.full((5, 7, 3), value, dtype=np.uint8)
    result = transfer_color_lab(source, 255 - source)
    assert result.shape == source.shape
    assert np.isfinite(result).all()


def test_single_pixel_and_different_sizes() -> None:
    source = np.array([[[20, 40, 60]]], dtype=np.uint8)
    reference = _gradient(30, 40)
    assert transfer_color_lab(source, reference).shape == (1, 1, 3)


@pytest.mark.parametrize(
    "invalid",
    [None, np.array([], dtype=np.uint8), np.zeros((3, 3), dtype=np.uint8), np.zeros((2, 2, 4), dtype=np.uint8)],
)
def test_reject_invalid_source(invalid) -> None:
    with pytest.raises(ValueError):
        transfer_color_lab(invalid, np.zeros((2, 2, 3), dtype=np.uint8))
