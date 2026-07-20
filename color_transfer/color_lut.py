"""三维颜色查找表创建与分块应用。"""

import numpy as np

LUT_SIZE = 65
LUT_CHUNK_SIZE = 500_000


def identity_lut(size: int = LUT_SIZE) -> np.ndarray:
    """创建覆盖归一化三维颜色立方体的恒等 LUT。"""
    axis = np.linspace(0.0, 1.0, size, dtype=np.float32)
    grid = np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1)
    return grid


def apply_lut_in_chunks(values: np.ndarray, lut: np.ndarray) -> None:
    """以三线性插值将 LUT 原地应用到像素数组。"""
    for start in range(0, values.shape[0], LUT_CHUNK_SIZE):
        stop = min(start + LUT_CHUNK_SIZE, values.shape[0])
        values[start:stop] = _trilinear(values[start:stop], lut)


def apply_lut(values: np.ndarray, lut: np.ndarray) -> np.ndarray:
    """将 LUT 应用于较小的颜色样本。"""
    return _trilinear(values, lut)


def smooth_lut(lut: np.ndarray, passes: int = 1) -> None:
    """以可分离三维低通平滑 LUT，抑制分位数映射色带。"""
    for _ in range(passes):
        for axis in range(3):
            previous = np.roll(lut, 1, axis=axis)
            following = np.roll(lut, -1, axis=axis)
            smoothed = (previous + 2.0 * lut + following) * 0.25
            edge_start = [slice(None)] * 4
            edge_stop = [slice(None)] * 4
            edge_start[axis] = 0
            edge_stop[axis] = -1
            smoothed[tuple(edge_start)] = lut[tuple(edge_start)]
            smoothed[tuple(edge_stop)] = lut[tuple(edge_stop)]
            lut[:] = smoothed


def _trilinear(values: np.ndarray, lut: np.ndarray) -> np.ndarray:
    size = lut.shape[0]
    coordinates = np.clip(values, 0.0, 1.0) * (size - 1)
    lower = np.floor(coordinates).astype(np.int32)
    upper = np.minimum(lower + 1, size - 1)
    weight = coordinates - lower
    result = np.zeros_like(values, dtype=np.float32)
    for corner in range(8):
        use_upper = np.array([(corner >> axis) & 1 for axis in range(3)], dtype=bool)
        indices = np.where(use_upper, upper, lower)
        corner_weight = np.prod(np.where(use_upper, weight, 1.0 - weight), axis=1)
        result += lut[indices[:, 0], indices[:, 1], indices[:, 2]] * corner_weight[:, None]
    return result
