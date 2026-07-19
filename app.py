"""Color Transfer V1 的本地程序入口。"""

import os

os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")

from color_transfer.ui.build_interface import build_interface


def main() -> None:
    """仅在本机地址启动 Gradio 应用。"""
    demo = build_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=False,
    )


if __name__ == "__main__":
    main()
