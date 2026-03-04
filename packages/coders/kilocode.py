"""KiloCode 命令执行模块 - 跨平台命令执行核心逻辑

此模块提供跨平台的命令执行功能，支持 Windows PowerShell 和 macOS/Linux bash。

日志配置说明：
- 模块直接使用 loguru 的 logger
- 独立日志文件由应用层（dashboard/logger_config.py）配置
- 通过 filter=lambda record: record["name"] == "coders.kilocode" 实现日志分离
"""

import os
import subprocess
import sys
import threading
import time

from loguru import logger

from coders.platform_utils import is_linux, is_macos, is_windows


class KiloCode:
    """跨平台命令执行器"""

    def _validate_cwd(self, cwd: str | None) -> str:
        if cwd is None:
            cwd = os.path.expanduser("~")

        logger.debug(f"验证工作目录: {cwd}")

        if not os.path.exists(cwd):
            raise FileNotFoundError(f"工作目录不存在: {cwd}")

        if not os.access(cwd, os.R_OK | os.W_OK):
            raise PermissionError(f"工作目录权限不足: {cwd}")

        return cwd

    def probe(self, cwd: str | None = None) -> None:
        """探测 kilocode 命令是否可用

        Args:
            cwd: 工作目录路径，默认为用户主目录

        Note:
            - Windows: 使用 powershell -Command kilocode --version
            - macOS/Linux: 使用 bash -c kilocode --version
            - 成功时输出版本信息，失败时输出错误日志
        """
        cwd = self._validate_cwd(cwd)

        if is_windows():
            cmd = ["powershell", "-Command", "kilocode --version"]
            kwargs = {"encoding": "utf-8", "errors": "replace"}
        elif is_macos() or is_linux():
            cmd = ["bash", "-c", "kilocode --version"]
            kwargs = {}
        else:
            logger.error(f"不支持的平台: {sys.platform}")
            return

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=cwd,
                **kwargs,
            )
            if result.returncode == 0 and result.stdout.strip():
                logger.info(f"kilocode 探针成功: {result.stdout.strip()}")
            else:
                logger.error("kilocode 探针失败: 未找到 kilocode 命令或执行出错")
        except Exception as e:
            logger.error(f"kilocode 探针异常: {type(e).__name__}: {e}")

    def run_command(
        self, command: str, cwd: str | None = None
    ) -> subprocess.CompletedProcess | None:
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
        cwd = self._validate_cwd(cwd)

        if is_windows():
            prefix = ["powershell", "-Command"]
        elif is_macos() or is_linux():
            prefix = ["bash", "-c"]
        else:
            logger.error(f"不支持的平台: {sys.platform}")
            return None

        full_command = prefix + [command.strip()]
        logger.info(f"执行命令: {full_command}")

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
                args=(process.stderr, logger.info, "stderr", stderr_lines),
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
                    logger.info(
                        f"命令仍在执行中，已等待 {elapsed_seconds}s，PID: {process.pid}"
                    )
                    next_heartbeat = now + 5

                time.sleep(0.2)

            logger.info("开始等待输出线程结束...")
            stdout_thread.join(timeout=1)
            logger.info(f"stdout 线程状态: alive={stdout_thread.is_alive()}")
            stderr_thread.join(timeout=1)
            logger.info(f"stderr 线程状态: alive={stderr_thread.is_alive()}")

            stdout_text = "".join(stdout_lines)
            stderr_text = "".join(stderr_lines)
            logger.info(
                f"输出收集完成: stdout={len(stdout_text)} 字符, stderr={len(stderr_text)} 字符"
            )
            completed_process = subprocess.CompletedProcess(
                args=full_command,
                returncode=return_code,
                stdout=stdout_text,
                stderr=stderr_text,
            )

            if return_code == 0:
                elapsed_seconds = int(time.monotonic() - start_time)
                logger.info(
                    f"命令执行成功，返回码: {return_code}，耗时: {elapsed_seconds}s"
                )
                return completed_process

            elapsed_seconds = int(time.monotonic() - start_time)
            logger.error(
                f"命令执行失败，返回码: {return_code}，耗时: {elapsed_seconds}s"
            )
            return None
        except Exception as e:
            logger.error(f"命令执行异常: {type(e).__name__}: {e}")
            return None


_default_instance = KiloCode()


def probe(cwd: str | None = None) -> None:
    """探测 kilocode 命令是否可用（模块级便捷函数）

    Args:
        cwd: 工作目录路径，默认为用户主目录
    """
    _default_instance.probe(cwd)


def run_command(
    command: str, cwd: str | None = None
) -> subprocess.CompletedProcess | None:
    """执行跨平台命令（模块级便捷函数）

    Args:
        command: 要执行的命令字符串
        cwd: 工作目录路径，默认为用户主目录

    Returns:
        成功时返回 subprocess.CompletedProcess 对象，失败时返回 None
    """
    return _default_instance.run_command(command, cwd)
