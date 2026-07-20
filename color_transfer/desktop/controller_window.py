"""正式版桌面控制窗口。"""

import tkinter as tk
from collections.abc import Callable
from functools import partial

from color_transfer.desktop.exit_application_action import exit_application
from color_transfer.desktop.open_page_action import open_page


def show_controller(url: str, close_server: Callable[[], None]) -> None:
    """显示重新打开页面和退出程序的桌面控制窗口。"""
    root = tk.Tk()
    root.title("参考图自动调色")
    root.geometry("420x190")
    root.resizable(False, False)

    tk.Label(root, text="参考图自动调色", font=("Microsoft YaHei UI", 18, "bold")).pack(pady=(24, 6))
    tk.Label(root, text="程序正在本机运行，关闭本窗口即可安全退出。", font=("Microsoft YaHei UI", 10)).pack()

    actions = tk.Frame(root)
    actions.pack(pady=24)
    tk.Button(actions, text="重新打开页面", width=16, command=partial(open_page, url)).pack(side=tk.LEFT, padx=6)
    exit_action = partial(exit_application, root, close_server)
    tk.Button(actions, text="退出程序", width=12, command=exit_action).pack(side=tk.LEFT, padx=6)
    root.protocol("WM_DELETE_WINDOW", exit_action)
    open_page(url)
    root.mainloop()
