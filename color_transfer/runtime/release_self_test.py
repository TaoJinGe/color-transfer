"""正式发行版运行时自检。"""

import json
import os
import traceback
import urllib.request
from pathlib import Path

from color_transfer.runtime.local_server import LocalServer


def _record(message: str) -> None:
    log_path = os.environ.get("COLOR_TRANSFER_SELF_TEST_LOG")
    if log_path:
        with Path(log_path).open("a", encoding="utf-8") as stream:
            stream.write(f"{message}\n")


def run_self_test() -> None:
    """启动本地服务并验证页面配置能够正常返回。"""
    _record("self-test started")
    server = LocalServer()
    try:
        url = server.start()
        _record(f"server started: {url}")
        with urllib.request.urlopen(f"{url.rstrip('/')}/config", timeout=30) as response:
            config = json.load(response)
        _record(f"config received: {response.status}")
        if response.status != 200 or config.get("title") != "参考图自动调色":
            raise RuntimeError("发行版页面配置验证失败。")
    except Exception as exc:
        _record(f"self-test failed: {type(exc).__name__}: {exc}")
        _record(traceback.format_exc())
        raise
    finally:
        _record("closing server")
        server.close()
        _record("self-test completed")
