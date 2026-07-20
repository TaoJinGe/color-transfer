"""Gradio 中文界面构建。"""

import gradio as gr

from .generate_action import generate_result
from .reset_action import reset_inputs


PAGE_CSS = """
.gradio-container { max-width: 1500px !important; padding: 10px 18px !important; }
.compact-header { margin-bottom: 4px !important; }
.compact-header h1 { font-size: 1.55rem; margin: 0 0 2px; }
.compact-header p { margin: 0; color: var(--body-text-color-subdued); }
.image-panel { min-width: 0 !important; }
.compact-actions { align-items: end; }
"""


def build_interface() -> gr.Blocks:
    """创建本地图片调色页面及按钮事件绑定。"""
    with gr.Blocks(title="参考图自动调色", fill_width=True) as demo:
        gr.Markdown(
            "# 参考图自动调色\n上传原图和参考图，一键生成相同配色。所有处理均在本地完成。",
            elem_classes="compact-header",
        )
        with gr.Row():
            source = gr.Image(
                label="① 原图", type="filepath", sources=["upload"], height="42vh", elem_classes="image-panel"
            )
            reference = gr.Image(
                label="② 参考图", type="filepath", sources=["upload"], height="42vh", elem_classes="image-panel"
            )
            result_preview = gr.Image(
                label="③ 结果预览", type="filepath", interactive=False, height="42vh", elem_classes="image-panel"
            )
        with gr.Row():
            strength = gr.Slider(0.0, 1.0, value=1.0, step=0.05, label="迁移强度")
            luminance = gr.Slider(0.0, 1.0, value=0.0, step=0.05, label="亮度保护")
            saturation = gr.Slider(0.0, 2.0, value=1.0, step=0.05, label="饱和度")
        with gr.Row(elem_classes="compact-actions"):
            generate = gr.Button("生成结果", variant="primary", scale=3)
            reset = gr.Button("重置", scale=1)
            download = gr.DownloadButton("下载结果 PNG", variant="secondary", scale=2)
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
