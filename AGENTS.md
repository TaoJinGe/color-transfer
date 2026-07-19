# AGENTS.md

## 项目目标

这是一个完全本地运行的图片色彩迁移工具。

## 开发规则

1. 开发前依次阅读 `../docs/AI_SYSTEM_RULES.md`、对应索引和 `DEVELOPMENT.md`。
2. 每次只完成一个明确任务，并保持文件职责单一、代码文件不超过 300 行。
3. 核心算法与界面分离，关键功能必须有测试。
4. 修改后必须运行相关测试，不得删除测试来规避失败。
5. 不得上传用户图片、添加网络请求、数据库或深度学习依赖。
6. 不得擅自扩大 V1 范围或使用硬编码绝对路径。
7. 新增、移动或删除文件后同步更新 ROOT_MAP、TREE_MAP 和相关功能链路索引。

## 常用命令

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest
python app.py
```

## 模块边界

- `load_image.py` 与 `save_result.py` 分别负责读取和输出，不放置调色算法。
- `lab_transfer.py` 只负责 Lab 统计映射，参数编排统一通过 `core.py`。
- `ui/` 内页面构建、生成动作、重置动作必须保持独立。
- 用户图片只能存在于内存、Gradio 临时目录或进程级临时结果目录，退出时清理。
