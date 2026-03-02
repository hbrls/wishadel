"""PySide6 窗口 - 主窗口"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 窗口基本配置
        self.setWindowTitle("Dashboard")
        self.setFixedSize(960, 510)  # 保持原窗口大小: 350+10+600=960, max(400,500)+10=510

        # 居中显示
        self.move(
            QApplication.primaryScreen().geometry().center() - self.frameGeometry().center()
        )

        # 设置主部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Hello Dashboard 标题
        title = QLabel("Hello Dashboard")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # 应用样式
        self._apply_styles()

    def _apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            QMainWindow {
                background: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
        """)

    def show(self):
        """显示窗口"""
        super().show()
        self.activateWindow()

    def hide(self):
        """隐藏窗口"""
        super().hide()

    def closeEvent(self, event):
        """点击关闭按钮时隐藏到托盘，不退出程序"""
        self.hide()
        event.ignore()