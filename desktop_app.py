"""正式发行版桌面入口。"""

import multiprocessing
import os
import sys
from tkinter import messagebox

os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
multiprocessing.freeze_support()
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w", encoding="utf-8")

from color_transfer.desktop.controller_window import show_controller
from color_transfer.runtime.local_server import LocalServer
from color_transfer.runtime.release_self_test import run_self_test


def main() -> None:
    """启动本地服务和桌面控制窗口。"""
    if "--self-test" in sys.argv:
        run_self_test()
        return
    server = LocalServer()
    try:
        show_controller(server.start(), server.close)
    except Exception as exc:
        server.close()
        messagebox.showerror("参考图自动调色", f"程序启动失败：\n{exc}")


if __name__ == "__main__":
    main()
