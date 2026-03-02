"""平台工具函数 - 跨平台系统判断"""

import sys


def is_windows() -> bool:
    """判断当前系统是否为 Windows"""
    return sys.platform == "win32"


def is_macos() -> bool:
    """判断当前系统是否为 macOS"""
    return sys.platform == "darwin"


def is_linux() -> bool:
    """判断当前系统是否为 Linux"""
    return sys.platform.startswith("linux")