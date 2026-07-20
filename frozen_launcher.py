"""正式版原生启动器入口。"""

import os
import subprocess
import sys
from pathlib import Path
from tkinter import messagebox


def main() -> None:
    """使用安装包内置运行时启动应用。"""
    install_dir = Path(sys.executable).resolve().parent
    pythonw = install_dir / "runtime" / "pythonw.exe"
    entrypoint = install_dir / "app" / "desktop_app.py"
    if not pythonw.is_file() or not entrypoint.is_file():
        messagebox.showerror("参考图自动调色", "程序文件不完整，请重新安装。")
        raise SystemExit(1)
    environment = os.environ.copy()
    environment["PYTHONUTF8"] = "1"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [str(pythonw), str(entrypoint), *sys.argv[1:]],
        cwd=entrypoint.parent,
        env=environment,
        check=False,
    )
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
