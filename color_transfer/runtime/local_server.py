"""Gradio 本地服务生命周期。"""

import gradio as gr

from color_transfer.ui.build_interface import PAGE_CSS, build_interface

from .server_port import find_available_port


class LocalServer:
    """启动和关闭仅绑定本机地址的 Gradio 服务。"""

    def __init__(self) -> None:
        self._demo: gr.Blocks | None = None
        self.url: str | None = None

    def start(self) -> str:
        """启动服务并返回本地访问地址。"""
        if self.url is not None:
            return self.url
        port = find_available_port()
        demo = build_interface()
        _, local_url, _ = demo.launch(
            server_name="127.0.0.1",
            server_port=port,
            share=False,
            inbrowser=False,
            show_error=False,
            prevent_thread_lock=True,
            quiet=True,
            css=PAGE_CSS,
        )
        self._demo = demo
        self.url = local_url
        return local_url

    def close(self) -> None:
        """停止服务并释放端口。"""
        if self._demo is not None:
            self._demo.close(verbose=False)
        self._demo = None
        self.url = None
