"""正式版运行时测试。"""

import socket

import pytest

from color_transfer.runtime.local_server import LocalServer
from color_transfer.runtime.server_port import find_available_port


def test_port_selection_skips_occupied_preferred_port() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as occupied:
        occupied.bind(("127.0.0.1", 0))
        preferred = occupied.getsockname()[1]
        selected = find_available_port(preferred, attempts=2)
    assert selected == preferred + 1


def test_port_selection_reports_exhaustion() -> None:
    sockets = []
    try:
        first = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        first.bind(("127.0.0.1", 0))
        sockets.append(first)
        port = first.getsockname()[1]
        second = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        second.bind(("127.0.0.1", port + 1))
        sockets.append(second)
        with pytest.raises(RuntimeError, match="找不到可用"):
            find_available_port(port, attempts=2)
    finally:
        for item in sockets:
            item.close()


def test_local_server_close_is_idempotent() -> None:
    server = LocalServer()
    server.close()
    server.close()
    assert server.url is None
