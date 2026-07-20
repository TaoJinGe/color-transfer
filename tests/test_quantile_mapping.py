"""一维分位数映射测试。"""

import numpy as np

from color_transfer.quantile_mapping import apply_quantile_map, learn_quantile_map


def test_maps_different_sample_counts() -> None:
    source = np.linspace(0, 1, 50, dtype=np.float32)
    reference = np.linspace(10, 20, 137, dtype=np.float32)
    result = apply_quantile_map(source, learn_quantile_map(source, reference))
    assert result[0] >= 10
    assert result[-1] <= 20
    np.testing.assert_allclose(np.median(result), 15, atol=0.2)


def test_repeated_source_values_are_stable() -> None:
    source = np.ones(20, dtype=np.float32)
    reference = np.arange(10, dtype=np.float32)
    result = apply_quantile_map(source, learn_quantile_map(source, reference))
    assert np.isfinite(result).all()
    assert np.unique(result).size == 1


def test_empty_input_is_rejected() -> None:
    with np.testing.assert_raises(ValueError):
        learn_quantile_map(np.array([]), np.array([1]))
