"""KiloCode 命令执行模块 - 跨平台命令执行核心逻辑

此模块提供跨平台的命令执行功能，支持 Windows PowerShell 和 macOS/Linux bash。
"""

import os
import shutil
import subprocess
import sys
import threading
import time

from loguru import logger

from coders.platform_utils import is_windows, is_macos


class KiloCode:
    """跨平台命令执行器"""

    def __init__(self):
        logger.info("KiloCode 初始化完成")

    def run_command(self, command: str, cwd: str | None = None) -> subprocess.CompletedProcess | None:
        """执行跨平台命令

        Args:
            command: 要执行的命令字符串
            cwd: 工作目录路径，默认为用户主目录

        Returns:
            成功时返回 subprocess.CompletedProcess 对象，失败时返回 None

        Note:
            - Windows: 使用 powershell -Command 执行
            - macOS/Linux: 使用 bash -c 执行
            - 子进程 stdin 使用 DEVNULL，避免标准输入等待
            - 流式输出 stdout/stderr 到日志
            - 每 5 秒输出心跳日志
        """
        # 设置默认工作目录
        if cwd is None:
            cwd = os.path.expanduser("~")

        # 验证工作目录
        if not os.path.exists(cwd):
            logger.error(f"工作目录不存在: {cwd}")
            return None

        if not os.access(cwd, os.R_OK | os.W_OK):
            logger.error(f"工作目录权限不足: {cwd}")
            return None

        logger.info(f"工作目录: {cwd}")
        if is_windows():
            prefix = ["powershell", "-Command"]
        elif is_macos() or sys.platform.startswith("linux"):
            prefix = ["bash", "-c"]
        else:
            logger.error(f"不支持的平台: {sys.platform}")
            return None

        full_command = prefix + [command.strip()]
        logger.info(f"执行命令: {full_command}")
        logger.info(f"当前工作目录: {os.getcwd()}")
        logger.info(f"powershell 路径: {shutil.which('powershell')}")

        if is_windows():
            probe = subprocess.run(
                [
                    "powershell",
                    "-Command",
                    "Get-Command kilocode -ErrorAction SilentlyContinue | Select-Object Name,Source,CommandType | Format-List",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            if probe.stdout.strip():
                logger.info(f"kilocode 探针: {probe.stdout.strip()}")
            else:
                logger.error("kilocode 探针: 未找到 kilocode 命令")

        try:
            start_time = time.monotonic()
            process = subprocess.Popen(
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
            logger.info(f"子进程已启动，PID: {process.pid}")

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
                args=(process.stdout, logger.info, "stdout", stdout_lines),
                daemon=True,
            )
            stderr_thread = threading.Thread(
                target=stream_reader,
                args=(process.stderr, logger.error, "stderr", stderr_lines),
                daemon=True,
            )
            stdout_thread.start()
            stderr_thread.start()
            logger.info("输出读取线程已启动")

            next_heartbeat = start_time + 5

            while True:
                return_code = process.poll()
                now = time.monotonic()

                if return_code is not None:
                    logger.info(f"进程已结束，返回码: {return_code}")
                    break

                if now >= next_heartbeat:
                    elapsed_seconds = int(now - start_time)
                    logger.info(f"命令仍在执行中，已等待 {elapsed_seconds}s，PID: {process.pid}")
                    next_heartbeat = now + 5

                time.sleep(0.2)

            logger.info("开始等待输出线程结束...")
            stdout_thread.join(timeout=1)
            logger.info(f"stdout 线程状态: alive={stdout_thread.is_alive()}")
            stderr_thread.join(timeout=1)
            logger.info(f"stderr 线程状态: alive={stderr_thread.is_alive()}")

            stdout_text = "".join(stdout_lines)
            stderr_text = "".join(stderr_lines)
            logger.info(f"输出收集完成: stdout={len(stdout_text)} 字符, stderr={len(stderr_text)} 字符")
            completed_process = subprocess.CompletedProcess(
                args=full_command,
                returncode=return_code,
                stdout=stdout_text,
                stderr=stderr_text,
            )

            if return_code == 0:
                elapsed_seconds = int(time.monotonic() - start_time)
                logger.info(f"命令执行成功，返回码: {return_code}，耗时: {elapsed_seconds}s")
                return completed_process

            elapsed_seconds = int(time.monotonic() - start_time)
            logger.error(f"命令执行失败，返回码: {return_code}，耗时: {elapsed_seconds}s")
            return None
        except Exception as e:
            logger.error(f"命令执行异常: {type(e).__name__}: {e}")
            return None


# 模块级默认实例，提供便捷的函数式调用
_default_instance = KiloCode()


def run_command(command: str, cwd: str | None = None) -> subprocess.CompletedProcess | None:
    """执行跨平台命令（模块级便捷函数）

    Args:
        command: 要执行的命令字符串
        cwd: 工作目录路径，默认为用户主目录

    Returns:
        成功时返回 subprocess.CompletedProcess 对象，失败时返回 None
    """
    return _default_instance.run_command(command, cwd)