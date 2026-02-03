"""
MVP3 - 日志模块（全局配置）

使用 loguru 库实现日志功能：
- 开发阶段：控制台输出
- exe 形态：文件日志（Wisadel 目录、大小滚动）
"""

import sys
from loguru import logger


def _get_log_dir() -> str:
    """获取日志目录"""
    import os
    log_dir = os.path.join(os.environ["LOCALAPPDATA"], "Temp", "Wisadel")
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def _is_executable() -> bool:
    """判断是否在打包后的可执行文件中运行"""
    return hasattr(sys, "frozen")


def init_logger():
    """
    初始化日志配置

    开发阶段：输出到控制台
    exe 形态：输出到文件（Wisadel 目录、大小滚动）
    """
    # 移除默认的控制台输出
    logger.remove()

    if _is_executable():
        # exe 形态：文件日志
        log_dir = _get_log_dir()
        log_file = f"{log_dir}/Wisadel-{{time:YYYY-MM-DD}}.log"

        logger.add(
            log_file,
            rotation="1 MB",  # 单文件不超过 1MB
            retention="10 days",  # 保留 10 天的日志
            level="DEBUG",
            encoding="utf-8"
        )
    else:
        # 开发阶段：控制台输出
        logger.add(sys.stderr, level="DEBUG")


# 初始化日志配置
init_logger()
