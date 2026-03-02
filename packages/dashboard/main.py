"""Dashboard - 项目入口"""

import logger_config  # 触发全局日志配置

import sys

from loguru import logger

# 跨包导入：使用 _agents 模块加载 agents
# 注意：不向 sys.path 添加任何目录，确保隔离性
from _agents import agents, Wisadel, MinimaxProvider

# 跨包导入：使用 _coders 模块加载 coders
# 注意：不向 sys.path 添加任何目录，确保隔离性
from _coders import KiloCode, ClaudeCode, run_command

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