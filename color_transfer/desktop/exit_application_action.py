"""桌面窗口退出动作。"""

import tkinter as tk
from collections.abc import Callable


def exit_application(root: tk.Tk, close_server: Callable[[], None]) -> None:
    """停止本地服务并关闭控制窗口。"""
    close_server()
    root.destroy()
