"""Gradio 界面构建测试。"""

import gradio as gr

from color_transfer.ui.build_interface import build_interface


def test_interface_builds_without_launching() -> None:
    interface = build_interface()
    assert isinstance(interface, gr.Blocks)
