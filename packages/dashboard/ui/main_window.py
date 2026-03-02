"""PySide6 窗口 - 主窗口"""

import os

from loguru import logger
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QApplication, QPushButton, QFileDialog, QLineEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from run_worker import RunWorker


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.run_worker = None

        # 工作目录（默认为用户主目录）
        self.working_directory = os.path.expanduser("~")

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

        # 添加弹性空间，将按钮推到下方
        main_layout.addStretch()

        # 工作目录选择区域
        self._setup_directory_selector(main_layout)

        # "润"按钮
        self.run_button = QPushButton("润")
        self.run_button.clicked.connect(self._on_run_button_clicked)
        self.run_button.setFixedHeight(40)
        main_layout.addWidget(self.run_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 按钮下方留一些边距
        main_layout.addSpacing(20)

        # 应用样式
        self._apply_styles()

    def _setup_directory_selector(self, layout: QVBoxLayout):
        """设置目录选择器"""
        # 目录选择按钮
        self.select_dir_button = QPushButton("选择工作目录")
        self.select_dir_button.clicked.connect(self._on_select_directory)
        layout.addWidget(self.select_dir_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 目录路径显示（只读文本框）
        self.directory_display = QLineEdit(self.working_directory)
        self.directory_display.setReadOnly(True)
        self.directory_display.setFixedWidth(500)
        self.directory_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.directory_display, alignment=Qt.AlignmentFlag.AlignCenter)

        # 添加间距
        layout.addSpacing(10)

    def _on_select_directory(self):
        """选择工作目录"""
        selected_dir = QFileDialog.getExistingDirectory(
            self,
            "选择工作目录",
            self.working_directory,
            QFileDialog.Option.ShowDirsOnly
        )
        if selected_dir:
            self.working_directory = selected_dir
            self.directory_display.setText(selected_dir)
            logger.info(f"工作目录已选择: {selected_dir}")

    def _on_run_button_clicked(self):
        """润按钮点击事件处理"""
        if self.run_worker and self.run_worker.isRunning():
            return

        logger.info("润按钮被点击")
        logger.info(f"工作目录: {self.working_directory}")
        self.run_button.setEnabled(False)

        self.run_worker = RunWorker(
            """
            kilocode run --model dashscope/glm-5 "前进！前进！不择手段的前进！"
            """,
            cwd=self.working_directory
        )
        self.run_worker.finished.connect(self._on_run_finished)
        self.run_worker.error.connect(self._on_run_error)
        self.run_worker.start()

    def _on_run_finished(self):
        """命令执行完成回调"""
        self.run_button.setEnabled(True)
        self.run_worker = None
        logger.info("命令执行完成")

    def _on_run_error(self, error_msg: str):
        """命令执行失败回调"""
        self.run_button.setEnabled(True)
        self.run_worker = None
        logger.error(f"命令执行失败: {error_msg}")

    def _apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            QMainWindow {
                background: #f5f5f5;
            }
            QLabel {
                color: #333;
            }
            QPushButton {
                padding: 8px 20px;
                border-radius: 4px;
                background: #0078d4;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background: #1084d8;
            }
            QPushButton:pressed {
                background: #006cbf;
            }
            QPushButton:disabled {
                background: #cccccc;
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