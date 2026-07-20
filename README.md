# Color Transfer V1.2

完全在本地运行的强参考配色迁移工具。程序会迭代匹配参考图的完整三维颜色分布，同时保留原图构图、分辨率与细节位置。

## Windows 正式版

运行 `ColorTransfer-Setup-1.2.0.exe` 并按提示安装，不需要另装 Python。安装后从桌面或开始菜单打开“参考图自动调色”，程序会自动打开本地页面；控制窗口可重新打开页面或安全退出程序。

默认使用 `http://127.0.0.1:7860`，端口被占用时会自动选择其他本地端口。支持 Windows 10/11 x64，以及 JPG、JPEG、PNG、WEBP；透明 PNG 会保留 Alpha。图片只在本机处理，不会上传互联网。

## 参数

- 色彩迁移强度：默认 1.0，完整使用迁移结果；降低后混回原图颜色。
- 亮度保护：默认 0.0，完整采用参考图明暗配色；提高后保留更多原图亮度。
- 饱和度：0 为灰度，1 不调整，2 增强饱和度，默认 1.0。

## 源码开发

开发环境需要 Python 3.11。双击 `start.bat` 可创建 `.venv`、安装依赖并启动；也可运行：

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe app.py
```

构建正式安装包需要 Inno Setup 6：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\build_release.ps1
```

产物输出至 `release\ColorTransfer-Setup-1.2.0.exe`。V1.2 使用 Pitié–Kokaram–Dahyot 思路的迭代式三维颜色概率分布迁移，并通过确定性 3D LUT 分块应用到原图全尺寸；它不理解人物、天空等语义，极端参考图也会产生相应的极端配色。
