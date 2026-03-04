"""命令执行工作线程 - 跨平台命令执行抽象

注意：核心命令执行逻辑已迁移至 coders.kilocode 模块，
此模块仅保留 UI 线程封装（RunWorker）。
"""

import subprocess
import threading
import time

from loguru import logger
from PySide6.QtCore import QThread, Signal

from _coders import probe
from coders.platform_utils import is_linux, is_macos, is_windows


class RunWorker(QThread):
    """后台执行命令线程

    支持实时状态更新，发射 PID 和运行时间信号。
    """

    error = Signal(str)
    status_update = Signal(int, int)  # (pid, elapsed_seconds)

    def __init__(self, command: str, cwd: str | None = None, parent=None):
        super().__init__(parent)
        self.command = command
        self.cwd = cwd
        self._process: subprocess.Popen | None = None
        self._start_time: float | None = None
        self._stop_flag = False

    def run(self):
        """执行命令，定期发射状态更新信号"""
        try:
            self._execute_command()
        except Exception as exc:
            self.error.emit(str(exc))

    def _execute_command(self):
        """跨平台执行命令，支持实时状态更新"""
        # 确定工作目录
        import os
        cwd = self.cwd
        if cwd is None:
            cwd = os.path.expanduser("~")

        # 构建跨平台命令
        if is_windows():
            prefix = ["powershell", "-Command"]
        elif is_macos() or is_linux():
            prefix = ["bash", "-c"]
        else:
            self.error.emit(f"不支持的平台")
            return

        full_command = prefix + [self.command.strip()]
        logger.info(f"执行命令: {full_command}")

        try:
            self._start_time = time.monotonic()
            self._process = subprocess.Popen(
                full_command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                cwd=cwd,
            )
            logger.info(f"子进程已启动，PID: {self._process.pid}")

            # 启动输出读取线程
            stdout_lines: list[str] = []
            stderr_lines: list[str] = []

            def stream_reader(stream, line_logger, tag: str, line_buffer: list[str]):
                try:
                    for line in iter(stream.readline, ""):
                        stripped_line = line.rstrip("\r\n")
                        if stripped_line:
                            line_logger(f"{tag}: {stripped_line}")
                        line_buffer.append(line)
                finally:
                    stream.close()

            stdout_thread = threading.Thread(
                target=stream_reader,
                args=(self._process.stdout, logger.info, "stdout", stdout_lines),
                daemon=True,
            )
            stderr_thread = threading.Thread(
                target=stream_reader,
                args=(self._process.stderr, logger.info, "stderr", stderr_lines),
                daemon=True,
            )
            stdout_thread.start()
            stderr_thread.start()
            logger.info("输出读取线程已启动")

            # 状态更新循环
            while not self._stop_flag:
                return_code = self._process.poll()
                now = time.monotonic()

                if return_code is not None:
                    logger.info(f"进程已结束，返回码: {return_code}")
                    break

                # 每 0.5 秒发射状态更新信号
                if self._start_time is not None:
                    elapsed_seconds = int(now - self._start_time)
                    self.status_update.emit(self._process.pid, elapsed_seconds)

                time.sleep(0.5)

            # 等待输出线程结束
            logger.info("开始等待输出线程结束...")
            stdout_thread.join(timeout=1)
            logger.info(f"stdout 线程状态: alive={stdout_thread.is_alive()}")
            stderr_thread.join(timeout=1)
            logger.info(f"stderr 线程状态: alive={stderr_thread.is_alive()}")

            elapsed_seconds = int(time.monotonic() - self._start_time) if self._start_time else 0
            return_code = self._process.returncode

            if return_code == 0:
                logger.info(
                    f"命令执行成功，返回码: {return_code}，耗时: {elapsed_seconds}s"
                )
            else:
                logger.error(
                    f"命令执行失败，返回码: {return_code}，耗时: {elapsed_seconds}s"
                )

        except Exception as e:
            logger.error(f"命令执行异常: {type(e).__name__}: {e}")
            self.error.emit(str(e))
        finally:
            self._process = None
            self._start_time = None
