"""测量强颜色分布迁移耗时与 Windows 峰值工作集。"""

import argparse
import ctypes
import os
import time

import numpy as np

from color_transfer.core import transfer_color_distribution


class ProcessMemoryCounters(ctypes.Structure):
    """Windows PROCESS_MEMORY_COUNTERS 结构。"""

    _fields_ = [
        ("cb", ctypes.c_ulong),
        ("PageFaultCount", ctypes.c_ulong),
        ("PeakWorkingSetSize", ctypes.c_size_t),
        ("WorkingSetSize", ctypes.c_size_t),
        ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPagedPoolUsage", ctypes.c_size_t),
        ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
        ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
        ("PagefileUsage", ctypes.c_size_t),
        ("PeakPagefileUsage", ctypes.c_size_t),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--height", type=int, required=True)
    parser.add_argument("--runs", type=int, default=1)
    arguments = parser.parse_args()
    generator = np.random.default_rng(20260720)
    source = generator.integers(0, 256, (arguments.height, arguments.width, 3), dtype=np.uint8)
    reference = generator.integers(0, 256, (900, 1200, 3), dtype=np.uint8)
    started = time.perf_counter()
    for _ in range(arguments.runs):
        result = transfer_color_distribution(source, reference)
        assert result.shape == source.shape
    elapsed = time.perf_counter() - started
    peak_mb = _peak_working_set() / (1024 * 1024)
    print(f"{arguments.width}x{arguments.height} runs={arguments.runs} time={elapsed:.2f}s peak={peak_mb:.1f}MB")


def _peak_working_set() -> int:
    counters = ProcessMemoryCounters()
    counters.cb = ctypes.sizeof(counters)
    handle = ctypes.windll.kernel32.OpenProcess(0x0400 | 0x0010, False, os.getpid())
    if not handle:
        return 0
    try:
        ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb)
        return int(counters.PeakWorkingSetSize)
    finally:
        ctypes.windll.kernel32.CloseHandle(handle)


if __name__ == "__main__":
    main()
