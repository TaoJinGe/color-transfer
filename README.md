# Color Transfer V1

完全在本地运行的参考图自动调色工具。上传原图和参考图后，可调整迁移强度、亮度保护与饱和度，预览并下载原尺寸 PNG 结果。

## Windows 启动

双击 `start.bat`。首次启动会创建 `.venv` 并安装依赖，之后可以断网启动。浏览器默认打开 `http://127.0.0.1:7860`，关闭启动窗口即可停止服务。

需要 Python 3.11，支持 JPG、JPEG、PNG、WEBP。带透明通道的 PNG 会保留 Alpha，所有图片处理均在本机完成，不会上传互联网。

## 参数

- 色彩迁移强度：0 保留原图，1 使用完整迁移结果，默认 0.8。
- 亮度保护：数值越高越接近原图亮度，默认 0.7。
- 饱和度：0 为灰度，1 不调整，2 增强饱和度，默认 1.0。

## 开发测试

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe app.py
```

V1 使用整体 Lab 颜色统计，不理解人物、天空等语义；极端参考图或构图差异较大时可能偏色。权威需求与 TODO 见根目录的 `Color_Transfer_V1_开发文档与TODO.md`。
