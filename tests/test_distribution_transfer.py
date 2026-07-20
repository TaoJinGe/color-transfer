"""完整颜色分布迁移与量化验收测试。"""

import numpy as np
import pytest

from color_transfer.core import transfer_color_distribution
from color_transfer.distribution_transfer import transfer_distribution
from color_transfer.lab_transfer import transfer_lab_statistics
from color_transfer.palette_distance import sliced_wasserstein_distance
from tests.palette_cases import PALETTE_PAIRS, palette_image


@pytest.mark.parametrize(("source_colors", "reference_colors"), PALETTE_PAIRS)
def test_new_distribution_passes_where_old_baseline_fails(source_colors, reference_colors) -> None:
    source = palette_image(source_colors)
    reference = palette_image(reference_colors)
    original_distance = sliced_wasserstein_distance(source, reference)
    old_result = transfer_lab_statistics(source, reference, luminance_protection=0.0)
    new_result = transfer_color_distribution(source, reference)
    assert sliced_wasserstein_distance(old_result, reference) > original_distance * 0.35
    assert sliced_wasserstein_distance(new_result, reference) <= original_distance * 0.35


def test_default_is_full_transfer_mode() -> None:
    source = palette_image([[20, 70, 220], [40, 140, 180]])
    reference = palette_image([[230, 80, 20], [180, 170, 30]])
    default = transfer_color_distribution(source, reference)
    explicit = transfer_color_distribution(source, reference, 1.0, 0.0, 1.0)
    assert np.array_equal(default, explicit)
    assert np.abs(default.astype(float) - source).mean() > 30


def test_fixed_seed_is_pixel_deterministic() -> None:
    generator = np.random.default_rng(10)
    source = generator.integers(0, 256, (40, 50, 3), dtype=np.uint8)
    reference = generator.integers(0, 256, (30, 60, 3), dtype=np.uint8)
    assert np.array_equal(transfer_distribution(source, reference), transfer_distribution(source, reference))


def test_identical_images_return_identical_pixels() -> None:
    generator = np.random.default_rng(12)
    image = generator.integers(0, 256, (30, 40, 3), dtype=np.uint8)
    assert np.array_equal(transfer_color_distribution(image, image), image)


def test_more_iterations_reduce_palette_distance() -> None:
    generator = np.random.default_rng(11)
    source = np.clip(generator.normal([30, 90, 210], 25, (50, 60, 3)), 0, 255).astype(np.uint8)
    reference = np.clip(generator.normal([220, 120, 25], 30, (40, 70, 3)), 0, 255).astype(np.uint8)
    first = transfer_distribution(source, reference, iterations=1)
    later = transfer_distribution(source, reference, iterations=8)
    assert sliced_wasserstein_distance(later, reference) < sliced_wasserstein_distance(first, reference)


def test_smooth_gradient_keeps_many_tonal_levels() -> None:
    ramp = np.linspace(0, 255, 256, dtype=np.uint8)
    source = np.stack([ramp, ramp, ramp], axis=1)[None].repeat(16, axis=0)
    reference = np.stack([ramp, np.clip(ramp // 2 + 60, 0, 255), 255 - ramp], axis=1)[None].repeat(16, axis=0)
    result = transfer_color_distribution(source, reference)
    assert np.unique(result.reshape(-1, 3), axis=0).shape[0] >= 128


@pytest.mark.parametrize(
    "reference_colors",
    [
        [[220, 80, 30], [250, 180, 60]],
        [[20, 80, 220], [30, 130, 225], [40, 190, 230]],
        [[220, 30, 180], [40, 230, 120], [180, 160, 40]],
        [[80, 80, 80], [130, 130, 130]],
        [[15, 20, 30], [50, 60, 80]],
        [[200, 210, 220], [245, 240, 225]],
    ],
)
def test_reference_styles_pass_distance_threshold(reference_colors) -> None:
    source = palette_image([[30, 150, 70], [100, 40, 190], [220, 120, 30]])
    reference = palette_image(reference_colors)
    result = transfer_color_distribution(source, reference)
    before = sliced_wasserstein_distance(source, reference)
    after = sliced_wasserstein_distance(result, reference)
    assert after <= before * 0.35
