"""一维完整分位数映射。"""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class QuantileMap:
    """一维分位数插值节点。"""

    source_values: np.ndarray
    target_values: np.ndarray


def learn_quantile_map(source: np.ndarray, reference: np.ndarray) -> QuantileMap:
    """学习把 source 累积分布映射到 reference 的插值节点。"""
    source_values = np.asarray(source, dtype=np.float32).reshape(-1)
    reference_values = np.asarray(reference, dtype=np.float32).reshape(-1)
    if source_values.size == 0 or reference_values.size == 0:
        raise ValueError("分位数映射输入不能为空。")
    source_sorted = np.sort(source_values)
    reference_sorted = np.sort(reference_values)
    source_q = (np.arange(source_sorted.size, dtype=np.float32) + 0.5) / source_sorted.size
    reference_q = (np.arange(reference_sorted.size, dtype=np.float32) + 0.5) / reference_sorted.size
    matched = np.interp(source_q, reference_q, reference_sorted).astype(np.float32)
    unique, first, counts = np.unique(source_sorted, return_index=True, return_counts=True)
    targets = np.add.reduceat(matched, first) / counts
    return QuantileMap(unique.astype(np.float32), targets.astype(np.float32))


def apply_quantile_map(values: np.ndarray, mapping: QuantileMap) -> np.ndarray:
    """将已学习的一维映射应用到任意数量像素。"""
    if mapping.source_values.size == 1:
        return np.full_like(values, mapping.target_values[0], dtype=np.float32)
    return np.interp(
        values,
        mapping.source_values,
        mapping.target_values,
        left=mapping.target_values[0],
        right=mapping.target_values[-1],
    ).astype(np.float32)
