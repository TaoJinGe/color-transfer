"""Gradio 中文界面构建。"""

import gradio as gr

from .generate_action import generate_result
from .reset_action import reset_inputs


def build_interface() -> gr.Blocks:
    """创建本地图片调色页面及按钮事件绑定。"""
    with gr.Blocks(title="参考图自动调色") as demo:
        gr.Markdown("# 参考图自动调色")
        gr.Markdown("上传原图和参考图，将参考图的色彩风格应用到原图。所有处理均在本地完成。")
        with gr.Row():
            source = gr.Image(label="原图", type="filepath", sources=["upload"])
            reference = gr.Image(label="参考图", type="filepath", sources=["upload"])
        strength = gr.Slider(0.0, 1.0, value=0.8, step=0.05, label="色彩迁移强度")
        luminance = gr.Slider(0.0, 1.0, value=0.7, step=0.05, label="亮度保护")
        saturation = gr.Slider(0.0, 2.0, value=1.0, step=0.05, label="饱和度")
        with gr.Row():
            generate = gr.Button("生成结果", variant="primary")
            reset = gr.Button("重置")
        result_preview = gr.Image(label="结果预览", type="filepath", interactive=False)
        download = gr.File(label="下载结果", interactive=False)
        generate.click(
            fn=generate_result,
            inputs=[source, reference, strength, luminance, saturation],
            outputs=[result_preview, download],
            show_progress="full",
        )
        reset.click(
            fn=reset_inputs,
            outputs=[source, reference, strength, luminance, saturation, result_preview, download],
        )
    return demo
