"""桌面窗口打开页面动作。"""

import webbrowser


def open_page(url: str) -> None:
    """使用系统默认浏览器打开应用页面。"""
    webbrowser.open(url)
