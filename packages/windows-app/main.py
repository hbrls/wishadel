"""
Wisadel - 桌面级文本润色验证工具
(PySide6 迁移版本)
"""

import logger_config  # 触发全局日志配置

# ============================================================
# 待后续阶段迁移（暂时保留原结构）
# ============================================================
import keyboard
import os
from focus import FocusManager
from hotkey_manager import register_global_hotkey, unregister_global_hotkey
from agent import Wisadel, MinimaxProvider
from loguru import logger

# pynput 键盘常量
from pynput import keyboard

# 平台检测工具
from platform_utils import is_macos, is_windows
# ============================================================

from PySide6.QtCore import QMetaObject, Qt
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.system_tray import SystemTrayIcon

import sys


# 全局焦点管理器
focus_mgr = FocusManager()
window = None


def register_hotkey(hotkey, callback):
    """注册全局快捷键，suppress=True 阻止按键传递给其他应用"""
    keyboard.add_hotkey(hotkey, callback, suppress=True)


def on_hotkey():
    """快捷键回调：唤起 GUI（必须在主线程执行）"""
    logger.debug("快捷键触发")

    # 记录焦点（已注释）
    hwnd = focus_mgr.save_current_focus()
    logger.debug(f"已记录原窗口句柄: {hwnd}")

    # 显示 GUI - 使用 QMetaObject.invokeMethod 确保在主线程执行
    QMetaObject.invokeMethod(
        window,
        "show",
        Qt.QueuedConnection
    )


def on_accept(text):
    """Accept 按钮回调：本期仅关闭窗口"""
    logger.debug(f"Accept 点击，文本长度: {len(text)}")

    window.hide()

    # Windows 焦点恢复 + 文本注入（已注释）
    if not focus_mgr.saved_window_handle:
        logger.warning("没有保存的窗口句柄，跳过注入")
        window.hide()
        return
    window.hide()
    logger.debug(f"恢复焦点到窗口: {focus_mgr.saved_window_handle}")
    focus_mgr.restore_focus(delay_ms=100)
    if text:
        focus_mgr.type_text(text)
        logger.debug("文本注入完成")
    else:
        logger.debug("文本为空，跳过注入")


def create_wisadel():
    """创建 Wisadel Agent 实例"""
    api_key = os.getenv("WISADEL_MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("请设置环境变量 WISADEL_MINIMAX_API_KEY")

    model = MinimaxProvider(api_key=api_key)
    return Wisadel(model=model)


def main():
    # 需要对全局变量 window 赋值，其他函数只读取
    global window

    logger.info("=" * 50)
    logger.info("  Wisadel - 桌面级文本润色验证工具")
    logger.info("=" * 50)
    logger.info("  快捷键: Alt+W (Windows) / Ctrl+Option+W (macOS)")
    logger.info("  流程: 左侧输入原文 → 润色 → Accept 上屏")
    logger.info("=" * 50)

    app = QApplication(sys.argv)

    # 设置应用属性
    app.setApplicationName("Wisadel")
    app.setApplicationDisplayName("Wisadel")

    # 创建 Wisadel 实例（暂时保留，后续阶段迁移）
    try:
        wisadel = create_wisadel()
    except ValueError as e:
        logger.warning(f"未配置 API Key，Agent 功能暂时不可用: {e}")
        wisadel = None

    # 创建窗口（PySide6 版本）
    window = MainWindow(on_accept_callback=on_accept, wisadel=wisadel)

    # 创建托盘图标
    tray = SystemTrayIcon(window)
    tray.show()

    # 注册全局快捷键（跨平台）
    # 使用 pynput 提供的 Key 枚举
    if is_macos():
        # macOS: Ctrl + Option + W
        register_global_hotkey((keyboard.Key.ctrl, keyboard.Key.alt, keyboard.KeyCode.from_char('w')), on_hotkey)
    elif is_windows():
        # Windows: Alt + W
        register_global_hotkey((keyboard.Key.alt, keyboard.KeyCode.from_char('w')), on_hotkey)
    else:
        raise RuntimeError("Linux 平台尚未支持全局快捷键功能")

    # 进入主循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
