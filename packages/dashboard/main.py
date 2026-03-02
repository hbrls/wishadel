"""Dashboard - 项目入口"""

import logger_config  # 触发全局日志配置

import os
import sys

from loguru import logger

# 跨包导入：使用 _agents 模块加载 agents
# 注意：不向 sys.path 添加任何目录，确保隔离性
from _agents import agents, Wisadel, MinimaxProvider

from PySide6.QtCore import QMetaObject, Qt
from PySide6.QtWidgets import QApplication

from platform_utils import is_macos, is_windows

from ui.main_window import MainWindow
from ui.system_tray import SystemTrayIcon


# 全局窗口引用
window = None


def main():
    # 需要对全局变量 window 赋值，其他函数只读取
    global window

    logger.info("=" * 50)
    logger.info("  Dashboard - 项目启动")
    logger.info("=" * 50)

    # 验证跨包导入：演示使用 Wisadel 和 MinimaxProvider
    logger.info("验证跨包导入模式...")
    logger.info(f"Wisadel 类已加载: {Wisadel}")
    logger.info(f"MinimaxProvider 类已加载: {MinimaxProvider}")

    # TASK-204: 验证 MiniMaxProvider 实际调用
    api_key = os.environ.get("WISADEL_MINIMAX_API_KEY")
    model = os.environ.get("WISADEL_MINIMAX_MODEL", "MiniMax-M2.1")
    provider = MinimaxProvider(api_key=api_key, model=model)
    test_input = "Hello MiniMax"
    messages = [{"role": "user", "content": test_input}]
    output = provider(messages)
    logger.info(f"MiniMaxProvider 输入: {test_input}")
    logger.info(f"MiniMaxProvider 输出类型: {type(output).__name__}")
    logger.info(f"MiniMaxProvider 输出: {output}")

    app = QApplication(sys.argv)

    # 设置应用属性
    app.setApplicationName("Dashboard")
    app.setApplicationDisplayName("Dashboard")

    # 创建窗口
    window = MainWindow()

    # 创建托盘图标
    tray = SystemTrayIcon(window)
    tray.show()

    # 显示窗口
    window.show()

    # 进入主循环
    sys.exit(app.exec())


if __name__ == "__main__":
    main()