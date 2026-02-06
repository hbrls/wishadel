"""润色任务工作线程"""

from PySide6.QtCore import QThread, Signal


class PolishWorker(QThread):
    """润色任务工作线程"""

    # 信号定义
    finished = Signal(str)  # 润色完成，传递结果
    error = Signal(str)     # 润色失败，传递错误信息

    def __init__(self, wisadel, text, parent=None):
        super().__init__(parent)
        self.wisadel = wisadel
        self.text = text

    def run(self):
        """执行润色任务（在子线程中运行）"""
        try:
            result = self.wisadel.run(self.text)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
