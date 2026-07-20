"""Gradio 界面构建测试。"""

import gradio as gr

from color_transfer.ui.build_interface import build_interface


def test_interface_builds_without_launching() -> None:
    interface = build_interface()
    assert isinstance(interface, gr.Blocks)


def test_primary_workflow_uses_compact_first_screen_layout() -> None:
    config = build_interface().config
    components = config["components"]
    images = [item for item in components if item["type"] == "image"]
    downloads = [item for item in components if item["type"] == "downloadbutton"]

    assert len(images) == 3
    assert all(item["props"]["height"] == "42vh" for item in images)
    assert len(downloads) == 1
