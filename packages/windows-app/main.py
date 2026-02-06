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
from agent import Wisadel, MinimaxProvider
from loguru import logger
# ============================================================

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
    """快捷键回调：唤起 GUI"""
    logger.debug("快捷键触发: Alt+W")

    # 记录当前前台窗口（唤起前）
    hwnd = focus_mgr.save_current_focus()
    logger.debug(f"已记录原窗口句柄: {hwnd}")

    # 显示 GUI
    window.show()


def on_accept(text):
    """Accept 按钮回调：将右侧文本注入原窗口"""
    logger.debug(f"Accept 点击，准备注入 {len(text)} 字符")

    # 检查是否有保存的窗口句柄
    if not focus_mgr.saved_window_handle:
        logger.warning("没有保存的窗口句柄，跳过注入")
        window.hide()
        return

    # 隐藏 GUI 并恢复焦点
    window.hide()
    logger.debug(f"恢复焦点到窗口: {focus_mgr.saved_window_handle}")
    # 延迟原因：GUI 隐藏和焦点转移需要时间，避免竞争条件导致焦点设置失败
    focus_mgr.restore_focus(delay_ms=100)

    # 注入 GUI 右侧文本到原窗口
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
    logger.info("  快捷键: Alt+W")
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

    # 注册全局快捷键
    register_hotkey('alt+w', on_hotkey)

    # 进入主循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
