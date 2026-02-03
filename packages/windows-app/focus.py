"""
MVP3 - 焦点管理模块
"""

import ctypes
import time

from loguru import logger

user32 = ctypes.windll.user32

# SendInput 相关常量和结构
# INPUT_KEYBOARD: 输入类型为键盘事件
INPUT_KEYBOARD = 1
# KEYEVENTF_KEYUP: 按键释放标志
KEYEVENTF_KEYUP = 0x0002
# VK_SHIFT: Shift 键的虚拟键码
VK_SHIFT = 0x10
# VK_RETURN: Enter 键的虚拟键码
VK_RETURN = 0x0D


class KEYBDINPUT(ctypes.Structure):
    """键盘输入结构体"""
    _fields_ = [
        ("wVk", ctypes.c_ushort),  # virtual_key: 虚拟键码
        ("wScan", ctypes.c_ushort),  # hardware_scan_code: 硬件扫描码
        ("dwFlags", ctypes.c_ulong),  # flags: 标志位
        ("time", ctypes.c_ulong),  # time: 时间戳
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),  # extra_info: 额外信息
    ]


class INPUT(ctypes.Structure):
    """通用输入结构体"""
    _fields_ = [
        ("type", ctypes.c_ulong),  # input_type: 输入类型
        ("ki", KEYBDINPUT),  # keyboard_input: 键盘输入数据
        ("padding", ctypes.c_ubyte * 8),  # union padding: 联合体填充字节
    ]


def send_key(virtual_key, key_up=False):
    """使用 SendInput 发送单个按键

    Args:
        virtual_key: 虚拟键码（如 VK_SHIFT, VK_RETURN）
        key_up: 是否为按键释放事件
    """
    input_struct = INPUT()
    input_struct.type = INPUT_KEYBOARD
    input_struct.ki.wVk = virtual_key
    input_struct.ki.dwFlags = KEYEVENTF_KEYUP if key_up else 0
    user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(INPUT))


def send_shift_enter():
    """发送 Shift+Enter 组合键（软换行）

    软换行：在聊天应用中不会触发发送消息，只换行
    """
    send_key(VK_SHIFT, key_up=False)   # Shift down
    send_key(VK_RETURN, key_up=False)  # Enter down
    send_key(VK_RETURN, key_up=True)   # Enter up
    send_key(VK_SHIFT, key_up=True)    # Shift up


class FocusManager:
    """焦点管理器：保存和恢复窗口焦点"""
    def __init__(self):
        self.saved_window_handle = None

    def save_current_focus(self):
        """保存当前前台窗口句柄

        Returns:
            int: 窗口句柄（HWND）
        """
        self.saved_window_handle = user32.GetForegroundWindow()
        return self.saved_window_handle

    def restore_focus(self, delay_ms=100):
        """恢复焦点到之前保存的窗口

        Args:
            delay_ms: 延迟毫秒数，避免竞争条件

        Returns:
            bool: 是否成功恢复焦点
        """
        if self.saved_window_handle:
            time.sleep(delay_ms / 1000)
            user32.SetForegroundWindow(self.saved_window_handle)
            return True
        return False

    def type_text(self, text):
        """向当前焦点窗口输入文本

        混合方案：
        - 普通字符：WM_CHAR（绕过输入法拦截）
        - 换行：SendInput 发送 Shift+Enter（软换行，避免触发聊天发送）

        Args:
            text: 要输入的文本
        """
        # WM_CHAR: 字符消息，用于发送 Unicode 字符
        WM_CHAR = 0x0102

        # 获取当前焦点控件的句柄
        window_handle = user32.GetFocus()
        if not window_handle:
            # 如果 GetFocus 失败，尝试用 GetForegroundWindow
            window_handle = user32.GetForegroundWindow()

        logger.debug(f"发送文本到控件: {window_handle}")

        for char in text:
            if char == '\n':
                # 换行：使用 SendInput 发送 Shift+Enter
                send_shift_enter()
                # 延迟 50ms：等待 SendInput 处理完成后再继续
                time.sleep(0.05)
            else:
                user32.PostMessageW(window_handle, WM_CHAR, ord(char), 0)
