"""系统托盘图标"""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction


class SystemTrayIcon(QSystemTrayIcon):
    """系统托盘图标"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent

        # 设置托盘图标
        self.setIcon(QIcon.fromTheme("dialog-information"))

        # 创建右键菜单
        self.menu = QMenu()

        # 显示窗口动作
        self.show_action = QAction("显示窗口", self)
        self.show_action.triggered.connect(self.show_window)
        self.menu.addAction(self.show_action)

        # 退出动作
        self.quit_action = QAction("退出", self)
        self.quit_action.triggered.connect(self.quit_app)
        self.menu.addAction(self.quit_action)

        # 设置上下文菜单
        self.setContextMenu(self.menu)

        # 显示托盘图标
        self.show()

    def show_window(self):
        """显示窗口"""
        if self.parent_window:
            self.parent_window.show()
            self.parent_window.activateWindow()

    def quit_app(self):
        """退出程序"""
        from PySide6.QtWidgets import QApplication
        QApplication.quit()
