"""平台检测工具（跨平台版本）"""

import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication


def is_windows():
    """检测是否为 Windows 平台"""
    return sys.platform == "win32"


def is_macos():
    """检测是否为 macOS 平台"""
    return sys.platform == "darwin"


def is_linux():
    """检测是否为 Linux 平台"""
    return sys.platform.startswith("linux")


def get_platform_name():
    """获取当前平台名称"""
    if is_windows():
        return "Windows"
    elif is_macos():
        return "macOS"
    elif is_linux():
        return "Linux"
    else:
        return "Unknown"


def get_font_family():
    """获取当前平台的默认字体族列表

    Returns:
        list: 字体族列表，按优先级排序

    Raises:
        RuntimeError: 不支持的平台
    """
    if is_macos():
        # macOS 字体
        return ["PingFang SC", "Helvetica", "Arial", "sans-serif"]
    elif is_windows():
        # Windows 字体
        return ["Microsoft YaHei", "SimSun", "Cambria", "Cochin", "Georgia", "Times New Roman", "serif"]
    elif is_linux():
        # Linux 字体
        return ["Noto Sans CJK SC", "WenQuanYi Micro Hei", "DejaVu Sans", "sans-serif"]
    else:
        raise RuntimeError("未知平台")


def get_tray_icon():
    """获取托盘图标，支持平台差异

    优先使用自定义 PNG 图标，回退到 Qt 内置图标
    """
    # 获取图标资源目录
    base_path = os.path.join(os.path.dirname(__file__), "ui", "assets")

    # 根据平台选择图标文件
    if is_macos():
        icon_filename = "icon-mac.png"
    elif is_windows():
        icon_filename = "icon-win.png"
    else:
        icon_filename = "icon-mac.png"  # Linux 默认使用 macOS 图标

    icon_path = os.path.join(base_path, icon_filename)

    # 如果图标文件存在，使用自定义图标
    if os.path.exists(icon_path):
        return QIcon(icon_path)

    # 回退到 Qt 内置图标
    style = QApplication.style()
    return style.standardIcon(style.StandardPixmap.SP_MessageBoxInformation)


def get_log_dir(app_name="Dashboard"):
    """获取日志目录（跨平台）

    Args:
        app_name: 应用名称，默认为 "Dashboard"

    Returns:
        str: 日志目录路径
    """
    if is_windows():
        # Windows: %LOCALAPPDATA%/Temp/{app_name}
        log_dir = os.path.join(
            os.environ.get("LOCALAPPDATA", os.path.expanduser("~")),
            "Temp",
            app_name
        )
    elif is_macos():
        # macOS: ~/Library/Logs/{app_name}
        log_dir = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Logs",
            app_name
        )
    else:
        # Linux: ~/.local/share/{app_name}/logs
        log_dir = os.path.join(
            os.path.expanduser("~"),
            ".local",
            "share",
            app_name,
            "logs"
        )

    os.makedirs(log_dir, exist_ok=True)
    return log_dir