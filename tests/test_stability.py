"""性能保护与连续处理稳定性测试。"""

from io import BytesIO
import gc
import tracemalloc

import numpy as np
import pytest
from PIL import Image

import color_transfer.load_image as load_module
from color_transfer.distribution_transfer import transfer_distribution
from color_transfer.image_io import ImageLoadError


def test_oversized_image_is_rejected(monkeypatch) -> None:
    stream = BytesIO()
    Image.new("RGB", (11, 10), (20, 30, 40)).save(stream, format="PNG")
    stream.seek(0)
    monkeypatch.setattr(load_module, "MAX_PIXELS", 100)
    with pytest.raises(ImageLoadError, match="尺寸过大"):
        load_module.load_image(stream)


def test_ten_consecutive_transfers_are_stable() -> None:
    generator = np.random.default_rng(20260718)
    source = generator.integers(0, 256, (180, 320, 3), dtype=np.uint8)
    reference = generator.integers(0, 256, (120, 200, 3), dtype=np.uint8)
    for index in range(10):
        result = transfer_distribution(source, reference, iterations=1, seed=index)
        assert result.shape == source.shape
        assert result.dtype == np.uint8


def test_repeated_transfers_do_not_retain_python_memory() -> None:
    source = np.full((240, 320, 3), [30, 100, 180], dtype=np.uint8)
    reference = np.full((180, 200, 3), [190, 80, 20], dtype=np.uint8)
    tracemalloc.start()
    baseline = tracemalloc.take_snapshot()
    for _ in range(10):
        transfer_distribution(source, reference, iterations=1)
    gc.collect()
    final = tracemalloc.take_snapshot()
    growth = sum(stat.size_diff for stat in final.compare_to(baseline, "filename"))
    tracemalloc.stop()
    assert growth < 10_000_000
