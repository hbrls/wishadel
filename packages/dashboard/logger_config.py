"""
日志模块（全局配置）

使用 loguru 库实现日志功能：
- 开发阶段：控制台输出
- exe 形态：文件日志（应用目录、大小滚动）
- 跨平台支持：Windows/macOS/Linux
"""

import sys
import os
from loguru import logger
from platform_utils import get_log_dir


def _is_executable() -> bool:
    """判断是否在打包后的可执行文件中运行"""
    return hasattr(sys, "frozen")


def init_logger():
    """
    初始化日志配置

    开发阶段：输出到控制台
    exe 形态：输出到文件（Dashboard 目录、大小滚动）
    """
    logger.remove()

    if _is_executable():
        log_dir = get_log_dir("Dashboard")
        log_file = os.path.join(log_dir, "Dashboard-{time:YYYY-MM-DD}.log")

        logger.add(
            log_file,
            rotation="1 MB",
            retention="10 days",
            level="DEBUG",
            encoding="utf-8",
            filter=lambda record: record["name"] != "coders.kilocode",
        )

        kilocode_log_file = os.path.join(
            log_dir, "Dashboard-KiloCode-{time:YYYY-MM-DD}.log"
        )
        logger.add(
            kilocode_log_file,
            filter=lambda record: record["name"] == "coders.kilocode",
            rotation="1 MB",
            retention="10 days",
            level="DEBUG",
            encoding="utf-8",
        )
    else:
        logger.add(sys.stderr, level="DEBUG")


# 初始化日志配置
init_logger()
