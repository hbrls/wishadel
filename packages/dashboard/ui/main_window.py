"""PySide6 窗口 - 主窗口"""

import os

from loguru import logger
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QApplication,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QGroupBox

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
        self.setFixedSize(960, 510)

        # 居中显示
        self.move(
            QApplication.primaryScreen().geometry().center()
            - self.frameGeometry().center()
        )

        # 设置主部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 主布局
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 标题栏和内容之间的间距
        main_layout.addSpacing(48)

        # 创建多横排布局容器
        self._setup_control_rows(main_layout)

        # 底部边距
        main_layout.addSpacing(20)

        # 顶部弹性空间，让内容靠上对齐
        main_layout.addStretch()

        # 应用样式
        self._apply_styles()

    def _setup_control_rows(self, main_layout: QVBoxLayout):
        """设置多横排控制区域"""
        # 第一行：选择目录按钮 + cwd 文本框 + 预备按钮 + 开始按钮
        row1_layout = QHBoxLayout()
        row1_layout.setContentsMargins(20, 0, 20, 0)
        row1_layout.setSpacing(8)

        # 选择目录按钮
        self.select_dir_button = QPushButton("选择目录")
        self.select_dir_button.clicked.connect(self._on_select_directory)
        self.select_dir_button.setFixedWidth(100)
        row1_layout.addWidget(self.select_dir_button)

        # cwd 只读文本框
        self.cwd_display = QLineEdit(self.working_directory)
        self.cwd_display.setReadOnly(True)
        self.cwd_display.setFixedHeight(30)
        row1_layout.addWidget(self.cwd_display)

        # 自动扩展空白（将右侧按钮推到最右边）
        spacer = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        row1_layout.addSpacerItem(spacer)

        # 预备按钮
        self.prepare_button = QPushButton("预备")
        self.prepare_button.clicked.connect(self._on_prepare_button_clicked)
        self.prepare_button.setFixedWidth(80)
        row1_layout.addWidget(self.prepare_button)

        # 开始按钮
        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self._on_start_button_clicked)
        self.start_button.setFixedWidth(80)
        row1_layout.addWidget(self.start_button)

        # 框间距
        row1_layout.addSpacing(8)

        # PID 框（QGroupBox）
        self.pid_group = QGroupBox("PID")
        self.pid_group.setFixedWidth(80)
        self.pid_value_label = QLabel("--")
        self.pid_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pid_layout = QVBoxLayout(self.pid_group)
        pid_layout.setContentsMargins(6, 6, 6, 6)
        pid_layout.addWidget(self.pid_value_label)
        row1_layout.addWidget(self.pid_group)

        # 耗时框（QGroupBox）
        self.timer_group = QGroupBox("耗时")
        self.timer_group.setFixedWidth(90)
        self.timer_value_label = QLabel("--:--:--")
        self.timer_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timer_layout = QVBoxLayout(self.timer_group)
        timer_layout.setContentsMargins(6, 6, 6, 6)
        timer_layout.addWidget(self.timer_value_label)
        row1_layout.addWidget(self.timer_group)

        main_layout.addLayout(row1_layout)
        main_layout.addSpacing(10)

        # 第二行：占位行（禁用状态）
        row2_layout = QHBoxLayout()
        row2_layout.setContentsMargins(20, 0, 20, 0)
        row2_layout.setSpacing(8)

        btn2_1 = QPushButton("占位按钮 2-1")
        btn2_1.setEnabled(False)
        btn2_1.setFixedWidth(100)
        row2_layout.addWidget(btn2_1)

        text2 = QLineEdit("示例行 2 - 待实现")
        text2.setReadOnly(True)
        text2.setEnabled(False)
        text2.setFixedHeight(30)
        row2_layout.addWidget(text2)

        spacer2 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        row2_layout.addSpacerItem(spacer2)

        btn2_2 = QPushButton("占位")
        btn2_2.setEnabled(False)
        btn2_2.setFixedWidth(80)
        row2_layout.addWidget(btn2_2)

        main_layout.addLayout(row2_layout)
        main_layout.addSpacing(10)

        # 第三行：占位行（禁用状态）
        row3_layout = QHBoxLayout()
        row3_layout.setContentsMargins(20, 0, 20, 0)
        row3_layout.setSpacing(8)

        btn3_1 = QPushButton("占位按钮 3-1")
        btn3_1.setEnabled(False)
        btn3_1.setFixedWidth(100)
        row3_layout.addWidget(btn3_1)

        text3 = QLineEdit("示例行 3 - 待实现")
        text3.setReadOnly(True)
        text3.setEnabled(False)
        text3.setFixedHeight(30)
        row3_layout.addWidget(text3)

        spacer3 = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        row3_layout.addSpacerItem(spacer3)

        btn3_2 = QPushButton("占位")
        btn3_2.setEnabled(False)
        btn3_2.setFixedWidth(80)
        row3_layout.addWidget(btn3_2)

        main_layout.addLayout(row3_layout)

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
            self.cwd_display.setText(selected_dir)
            logger.info(f"工作目录已选择: {selected_dir}")

    def _on_prepare_button_clicked(self):
        """预备按钮点击事件处理"""
        if self.run_worker and self.run_worker.isRunning():
            return

        logger.info("预备按钮被点击")
        logger.info(f"工作目录: {self.working_directory}")
        self.prepare_button.setEnabled(False)
        self.start_button.setEnabled(False)

        # 重置状态显示
        self._reset_status_display()

        command = """
        kilocode run --model dashscope/glm-5 "阅读 TASK.md，根据 # Instruction 更新 # Current Task。"
        """.strip()

        self.run_worker = RunWorker(command, cwd=self.working_directory)
        self.run_worker.finished.connect(self._on_run_finished)
        self.run_worker.error.connect(self._on_run_error)
        self.run_worker.status_update.connect(self._on_status_update)
        self.run_worker.start()

    def _on_start_button_clicked(self):
        """开始按钮点击事件处理"""
        if self.run_worker and self.run_worker.isRunning():
            return

        logger.info("开始按钮被点击")
        logger.info(f"工作目录: {self.working_directory}")
        self.prepare_button.setEnabled(False)
        self.start_button.setEnabled(False)

        # 重置状态显示
        self._reset_status_display()

        command = """
        kilocode run --model dashscope/glm-5 "阅读 TASK.md，执行 # Current Task。"
        """.strip()

        self.run_worker = RunWorker(command, cwd=self.working_directory)
        self.run_worker.finished.connect(self._on_run_finished)
        self.run_worker.error.connect(self._on_run_error)
        self.run_worker.status_update.connect(self._on_status_update)
        self.run_worker.start()

    def _on_run_finished(self):
        """命令执行完成回调"""
        self.prepare_button.setEnabled(True)
        self.start_button.setEnabled(True)
        self.run_worker = None
        # 清空状态显示
        self._reset_status_display()
        logger.info("命令执行完成")

    def _on_run_error(self, error_msg: str):
        """命令执行失败回调"""
        self.prepare_button.setEnabled(True)
        self.start_button.setEnabled(True)
        self.run_worker = None
        # 清空状态显示
        self._reset_status_display()
        logger.error(f"命令执行失败: {error_msg}")

    def _on_status_update(self, pid: int, elapsed_seconds: int):
        """状态更新回调 - 更新 PID 和运行时间显示

        Args:
            pid: 进程 ID
            elapsed_seconds: 已运行时间（秒）
        """
        # 更新 PID 标签
        self.pid_value_label.setText(str(pid))

        # 格式化运行时间为 HH:MM:SS
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_value_label.setText(time_str)

    def _reset_status_display(self):
        """重置状态显示为默认值"""
        self.pid_value_label.setText("--")
        self.timer_value_label.setText("--:--:--")

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
            QGroupBox {
                border: 1px solid #cccccc;
                background-color: #f9f9f9;
                border-radius: 4px;
                margin-top: 8px;
                padding: 6px 10px;
                font-size: 9px;
                color: #666666;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                background-color: #f5f5f5;
            }
            QGroupBox QLabel {
                color: #333333;
                font-family: Consolas, Monaco, monospace;
                font-size: 11px;
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
