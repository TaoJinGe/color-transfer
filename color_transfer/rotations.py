"""确定性三维正交旋转矩阵生成。"""

import numpy as np


def orthogonal_rotations(count: int, seed: int) -> tuple[np.ndarray, ...]:
    """生成包含单位矩阵的可复现正交旋转序列。"""
    if count < 1:
        raise ValueError("迭代轮数必须大于零。")
    generator = np.random.default_rng(seed)
    matrices = [np.eye(3, dtype=np.float32)]
    for _ in range(count - 1):
        matrix = generator.normal(size=(3, 3))
        q, r = np.linalg.qr(matrix)
        signs = np.where(np.diag(r) < 0.0, -1.0, 1.0)
        q *= signs
        if np.linalg.det(q) < 0.0:
            q[:, 0] *= -1.0
        matrices.append(q.astype(np.float32))
    return tuple(matrices)
