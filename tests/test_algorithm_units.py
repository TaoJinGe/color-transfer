"""强颜色迁移基础模块测试。"""

import numpy as np

from color_transfer.color_space import perceptual_to_rgb, rgb_to_perceptual
from color_transfer.color_lut import identity_lut, smooth_lut
from color_transfer.gamut import compress_perceptual_gamut
from color_transfer.rotations import orthogonal_rotations


def test_color_space_round_trip_is_close() -> None:
    rgb = np.array([[[0, 0, 0], [255, 255, 255], [20, 130, 240], [230, 60, 90]]], dtype=np.uint8)
    restored = np.clip(np.rint(perceptual_to_rgb(rgb_to_perceptual(rgb)) * 255), 0, 255).astype(np.uint8)
    assert np.max(np.abs(restored.astype(np.int16) - rgb.astype(np.int16))) <= 1


def test_rotations_are_orthogonal_and_reproducible() -> None:
    first = orthogonal_rotations(8, seed=123)
    second = orthogonal_rotations(8, seed=123)
    for left, right in zip(first, second):
        np.testing.assert_array_equal(left, right)
        np.testing.assert_allclose(left.T @ left, np.eye(3), atol=1e-6)
        np.testing.assert_allclose(np.linalg.det(left), 1.0, atol=1e-6)


def test_gamut_compression_is_finite_and_bounded() -> None:
    values = np.array([[-2.0, 0.5, 3.0], [0.1, 0.5, 0.9], [np.inf, 0.0, 1.0]], dtype=np.float32)
    values = np.nan_to_num(values, nan=0.5, posinf=4.0, neginf=-4.0)
    result = compress_perceptual_gamut(values)
    assert np.isfinite(result).all()
    assert result.min() >= 0.0 and result.max() <= 1.0


def test_gamut_compression_preserves_in_range_values() -> None:
    values = np.array([[0.1, 0.5, 0.9], [0.0, 0.4, 1.0]], dtype=np.float32)
    np.testing.assert_allclose(compress_perceptual_gamut(values), values)


def test_lut_smoothing_reduces_local_discontinuity() -> None:
    lut = identity_lut(17)
    lut[8:, :, :, 0] += 0.5
    before = np.abs(np.diff(lut[..., 0], axis=0)).max()
    smooth_lut(lut, passes=3)
    after = np.abs(np.diff(lut[..., 0], axis=0)).max()
    assert after < before
