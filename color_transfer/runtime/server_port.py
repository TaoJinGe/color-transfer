"""本地服务端口选择。"""

import socket


def find_available_port(preferred: int = 7860, attempts: int = 50) -> int:
    """从首选端口开始返回第一个可绑定的本机端口。"""
    for port in range(preferred, preferred + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            try:
                probe.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError("找不到可用的本地端口，请关闭部分程序后重试。")
