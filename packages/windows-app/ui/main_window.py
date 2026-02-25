"""PySide6 窗口 - 迁移自 gui.py"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QFrame, QApplication, QSizePolicy
)
from PySide6.QtCore import Qt, QSize, QThread, QEvent
from PySide6.QtGui import QFont, QTextCursor, QTextDocument

import ctypes

from .polish_worker import PolishWorker

# 文本字体设置 - 按优先级指定字体族（跨平台）
from platform_utils import get_font_family

TEXT_FONT_FAMILIES = get_font_family()

user32 = ctypes.windll.user32


class MainWindow(QMainWindow):
    """主窗口 - 迁移自 Tkinter"""

    def __init__(self, on_accept_callback=None, wisadel=None, parent=None):
        super().__init__(parent)

        self.on_accept = on_accept_callback
        self.wisadel = wisadel
        self.polish_worker = None  # 润色工作线程

        # 窗口基本配置
        self.setWindowTitle("Wisadel")
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # Topmost，禁用最小化和最大化按钮（显示但不可点击）
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 居中显示
        self.move(
            QApplication.primaryScreen().geometry().center() - self.frameGeometry().center()
        )

        # 设置主部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 文本区域容器
        text_container = QWidget()
        text_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        text_layout = QHBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(10)

        # =====================================
        # 左区：左文字区 + 润按钮（垂直排列）
        # =====================================
        left_zone = QFrame()
        left_zone_layout = QVBoxLayout(left_zone)
        left_zone_layout.setContentsMargins(0, 0, 0, 0)
        left_zone_layout.setSpacing(5)
        left_zone_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 左侧文本框 - width=350, height=400
        self.left_text = QTextEdit()
        self.left_text.setFont(QFont(TEXT_FONT_FAMILIES[0], 10))
        self.left_text.setFixedSize(QSize(350, 400))
        # TODO: spacing2/spacing3 行间距待 PySide6 兼容
        # self.left_text.document().setLineSpacing(2)
        self.left_text.setPlaceholderText("在此输入原文...")
        left_zone_layout.addWidget(self.left_text)

        # 润按钮 - 移至左区下方
        self.polish_btn = QPushButton("润")
        self.polish_btn.clicked.connect(self._on_polish)
        self.polish_btn.setFixedHeight(40)
        left_zone_layout.addWidget(self.polish_btn)

        text_layout.addWidget(left_zone)

        # =====================================
        # 右区：右文字区（宽度缩减10-15%）
        # =====================================
        right_zone = QFrame()
        right_zone_layout = QVBoxLayout(right_zone)
        right_zone_layout.setContentsMargins(0, 0, 0, 0)
        right_zone_layout.setSpacing(0)
        right_zone_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 右侧文本框 - width=600, height=500
        self.right_text = QTextEdit()
        self.right_text.setFont(QFont(TEXT_FONT_FAMILIES[0], 10))
        self.right_text.setFixedSize(QSize(600, 500))
        # TODO: spacing2/spacing3 行间距待 PySide6 兼容
        # self.right_text.document().setLineSpacing(2)
        self.right_text.setPlaceholderText("润色结果将显示在此...")
        right_zone_layout.addWidget(self.right_text)

        text_layout.addWidget(right_zone)

        main_layout.addWidget(text_container)

        # =====================================
        # 下按钮区：复制按钮 + Accept按钮
        # =====================================
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(10)

        # 左侧留白，与左区宽度对齐（使复制按钮与右区左对齐）
        left_spacer = QWidget()
        left_spacer.setFixedSize(350, 40)  # 左区宽度(350)，按钮布局的spacing(10)会自动添加
        btn_layout.addWidget(left_spacer)

        # 复制按钮 - 与右文字区左对齐
        self.copy_btn = QPushButton("复制")
        self.copy_btn.clicked.connect(self._on_copy)
        self.copy_btn.setEnabled(False)  # 暂不实现功能
        btn_layout.addWidget(self.copy_btn)

        # 中间弹性空间
        middle_spacer = QWidget()
        middle_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        btn_layout.addWidget(middle_spacer)

        # Accept按钮 - 与右文字区右对齐
        self.accept_btn = QPushButton("Accept")
        self.accept_btn.clicked.connect(self._on_accept)
        btn_layout.addWidget(self.accept_btn)

        main_layout.addWidget(btn_container)

        # 应用样式
        self._apply_styles()

    def _apply_styles(self):
        """应用样式"""
        self.setStyleSheet("""
            QMainWindow {
                background: #f5f5f5;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                background: white;
            }
            QTextEdit:focus {
                border-color: #0078d4;
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
            QFrame {
                background: transparent;
            }
        """)

    def _on_polish(self):
        """润色按钮点击：异步调用 Wisadel 润色左侧文本"""
        text = self.left_text.toPlainText().strip()
        if not text:
            return

        # 防止重复点击
        if self.polish_worker and self.polish_worker.isRunning():
            return

        # 显示"润色中..."状态
        self.right_text.setPlainText("润色中...")
        self.polish_btn.setEnabled(False)

        # 创建并启动工作线程
        self.polish_worker = PolishWorker(self.wisadel, text)
        self.polish_worker.finished.connect(self._on_polish_finished)
        self.polish_worker.error.connect(self._on_polish_error)
        self.polish_worker.start()

    def _on_polish_finished(self, result):
        """润色完成回调"""
        self.right_text.setPlainText(result)
        self.polish_btn.setEnabled(True)
        self.polish_worker = None

    def _on_polish_error(self, error_msg):
        """润色失败回调"""
        self.right_text.setPlainText(f"润色失败: {error_msg}")
        self.polish_btn.setEnabled(True)
        self.polish_worker = None

    def _on_accept(self):
        """Accept 按钮点击"""
        if self.on_accept:
            text = self.get_output_text()
            self.on_accept(text)

    def _on_copy(self):
        """复制按钮点击 - 暂不实现功能"""
        # TODO: 实现复制功能
        pass

    def closeEvent(self, event):
        """窗口关闭时清理资源"""
        if self.polish_worker and self.polish_worker.isRunning():
            self.polish_worker.terminate()
            self.polish_worker.wait()
        super().closeEvent(event)

    def _focus_left_text(self):
        """聚焦左侧文本框并全选"""
        cursor = self.left_text.textCursor()
        cursor.select(QTextCursor.Document)
        self.left_text.setTextCursor(cursor)
        self.left_text.setFocus()

    def show(self):
        """显示窗口"""
        super().show()
        self.activateWindow()
        # 使用 Windows API 请求前台焦点
        hwnd = self.winId()
        user32.SetForegroundWindow(hwnd)
        # 唤起时自动全选左侧文本
        self._focus_left_text()

    def changeEvent(self, event):
        """窗口状态变化事件"""
        if event.type() == QEvent.Type.ActivationChange:
            if self.isActiveWindow():
                # 窗口被激活时获取焦点
                self._focus_left_text()
        super().changeEvent(event)

    def hide(self):
        """隐藏窗口"""
        super().hide()

    def get_output_text(self):
        """获取右侧输出文本"""
        return self.right_text.toPlainText().strip()

    def closeEvent(self, event):
        """点击关闭按钮时隐藏到托盘，不退出程序"""
        self.hide()
        event.ignore()

    def _apply_translucent_style(self):
        """应用半透明磨砂效果样式"""
        self.central_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(245, 245, 245, 200);
                border-radius: 10px;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #0078d4;
                border-radius: 4px;
            }
        """)
