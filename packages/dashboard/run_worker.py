"""命令执行工作线程 - 跨平台命令执行抽象

注意：核心命令执行逻辑已迁移至 coders.kilocode 模块，
此模块仅保留 UI 线程封装（RunWorker）。
"""

from loguru import logger
from PySide6.QtCore import QThread, Signal

from _coders import run_command


class RunWorker(QThread):
    """后台执行命令线程"""

    error = Signal(str)

    def __init__(self, command: str, cwd: str | None = None, parent=None):
        super().__init__(parent)
        self.command = command
        self.cwd = cwd

    def run(self):
        try:
            run_command(self.command, cwd=self.cwd)
        except Exception as exc:
            self.error.emit(str(exc))
