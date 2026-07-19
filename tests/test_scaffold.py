"""阶段 0 项目脚手架测试。"""


def test_package_can_be_imported() -> None:
    import color_transfer

    assert color_transfer.__version__ == "1.0.0"
