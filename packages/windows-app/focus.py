# MVP3 - 焦点管理模块
import ctypes
import time
import logger

user32 = ctypes.windll.user32

# SendInput 相关常量和结构
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
VK_SHIFT = 0x10
VK_RETURN = 0x0D


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ki", KEYBDINPUT),
        ("padding", ctypes.c_ubyte * 8),  # union padding
    ]


def send_key(vk, key_up=False):
    """使用 SendInput 发送单个按键"""
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.ki.wVk = vk
    inp.ki.dwFlags = KEYEVENTF_KEYUP if key_up else 0
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


def send_shift_enter():
    """发送 Shift+Enter 组合键（软换行）"""
    send_key(VK_SHIFT, key_up=False)   # Shift down
    send_key(VK_RETURN, key_up=False)  # Enter down
    send_key(VK_RETURN, key_up=True)   # Enter up
    send_key(VK_SHIFT, key_up=True)    # Shift up


class FocusManager:
    def __init__(self):
        self.saved_hwnd = None

    def save_current_focus(self):
        """保存当前前台窗口句柄"""
        self.saved_hwnd = user32.GetForegroundWindow()
        return self.saved_hwnd

    def restore_focus(self, delay_ms=100):
        """恢复焦点到之前保存的窗口"""
        if self.saved_hwnd:
            time.sleep(delay_ms / 1000)
            user32.SetForegroundWindow(self.saved_hwnd)
            return True
        return False

    def type_text(self, text):
        """向当前焦点窗口输入文本
        
        混合方案：
        - 普通字符：WM_CHAR（绕过输入法拦截）
        - 换行：SendInput 发送 Shift+Enter（软换行，避免触发聊天发送）
        """
        WM_CHAR = 0x0102
        
        # 获取当前焦点控件的句柄
        hwnd = user32.GetFocus()
        if not hwnd:
            # 如果 GetFocus 失败，尝试用 GetForegroundWindow
            hwnd = user32.GetForegroundWindow()
        
        logger.debug(f"发送文本到控件: {hwnd}")
        
        for char in text:
            if char == '\n':
                # 换行：使用 SendInput 发送 Shift+Enter
                send_shift_enter()
                time.sleep(0.05)  # 等待 SendInput 处理完成后再继续
            else:
                user32.PostMessageW(hwnd, WM_CHAR, ord(char), 0)
