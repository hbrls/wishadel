# MVP3 - GUI 窗口模块
import tkinter as tk
import ctypes

user32 = ctypes.windll.user32


class PolishWindow:
    def __init__(self, on_accept_callback=None):
        self.root = tk.Tk()
        self.root.title("Wisadel")
        self.root.attributes('-topmost', True)
        # 去掉最小化、最大化按钮，只保留关闭按钮
        self.root.resizable(False, False)
        self.root.attributes('-toolwindow', True)
        self.on_accept = on_accept_callback
        self._setup_ui()

    def _setup_ui(self):
        # 主容器
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10)

        # 左右文本区容器
        text_frame = tk.Frame(main_frame)
        text_frame.pack()

        # 左侧：原始文本区
        left_frame = tk.Frame(text_frame)
        left_frame.pack(side=tk.LEFT, padx=(0, 5))
        tk.Label(left_frame, text="原始文本").pack()
        self.left_text = tk.Text(left_frame, width=40, height=20)
        self.left_text.pack()

        # 右侧：输出文本区
        right_frame = tk.Frame(text_frame)
        right_frame.pack(side=tk.LEFT, padx=(5, 0))
        tk.Label(right_frame, text="输出文本").pack()
        self.right_text = tk.Text(right_frame, width=40, height=20)
        self.right_text.pack()

        # 按钮区
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=(10, 0))

        # 复制按钮：将左侧文本复制到右侧
        self.copy_btn = tk.Button(btn_frame, text="复制到右侧", command=self._on_copy)
        self.copy_btn.pack(side=tk.LEFT, padx=5)

        # Accept 按钮
        self.accept_btn = tk.Button(btn_frame, text="Accept", command=self._on_accept)
        self.accept_btn.pack(side=tk.LEFT, padx=5)

    def _on_copy(self):
        """将左侧文本复制到右侧"""
        text = self.left_text.get("1.0", tk.END).rstrip('\n')
        # TODO: 用 AI 润色
        self.right_text.delete("1.0", tk.END)
        self.right_text.insert("1.0", text)

    def _on_accept(self):
        """Accept 按钮点击"""
        if self.on_accept:
            text = self.get_output_text()
            self.on_accept(text)

    def show(self):
        """显示窗口"""
        self.root.deiconify()
        self.root.lift()
        # 方案 A：立即用 Windows API 请求前台焦点
        hwnd = self.root.winfo_id()
        user32.SetForegroundWindow(hwnd)
        # 方案 C：唤起时自动全选左侧文本
        self.left_text.tag_add(tk.SEL, "1.0", tk.END)
        self.left_text.mark_set(tk.INSERT, "1.0")
        self.left_text.focus_set()

    def hide(self):
        """隐藏窗口"""
        self.root.withdraw()

    def get_output_text(self):
        """获取右侧输出文本"""
        # Tkinter Text.get() 会在末尾自动加一个 \n，需要去掉
        text = self.right_text.get("1.0", tk.END)
        if text.endswith('\n'):
            text = text[:-1]
        return text

    def run(self):
        """启动主循环"""
        self.root.mainloop()
