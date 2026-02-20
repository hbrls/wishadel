"""
Hotkey Manager - 跨平台快捷键管理器

功能分层：
- 唤起（Invoke）：显示窗口、展开界面
- 焦点获取（Focus）：将窗口置前、激活应用（本期不实现）

本模块仅负责按键监听与事件分发，不包含任何焦点获取逻辑。

统一使用 pynput 实现跨平台快捷键注册。
必须使用 pynput 提供的 Key 枚举（如 keyboard.Key.alt）。
"""

import sys
from typing import Callable, Optional, Tuple
from loguru import logger

# 统一使用 pynput（跨平台）
from pynput import keyboard


class HotkeyManager:
    """跨平台快捷键管理器"""

    def __init__(self):
        self._listener: Optional[keyboard.Listener] = None
        self._hotkey: Optional[Tuple] = None
        self._callback: Optional[Callable] = None
        self._running: bool = False

    def register_hotkey(self, key: Tuple, callback: Callable) -> bool:
        """
        注册热键

        Args:
            key: 快捷键元组，必须使用 pynput.Key 枚举
                  例如：(keyboard.Key.alt, keyboard.KeyCode.from_char('w'))
            callback: 回调函数

        Returns:
            注册是否成功
        """
        if not isinstance(key, tuple):
            raise ValueError(f"快捷键必须使用 tuple 格式，不支持字符串: {key}")

        self._hotkey = key
        self._callback = callback
        logger.info(f"注册热键: {key}")
        return True

    def unregister_hotkey(self) -> bool:
        """注销热键"""
        self.stop()
        self._hotkey = None
        self._callback = None
        logger.info("已注销热键")
        return True

    def start(self) -> bool:
        """启动热键监听"""
        if self._running:
            logger.warning("热键监听已在运行中")
            return True

        if not self._hotkey or not self._callback:
            logger.error("未注册热键，无法启动")
            return False

        try:
            self._start_pynput()
            return True
        except Exception as e:
            logger.error(f"启动热键监听失败: {e}")
            return False

    def _start_pynput(self):
        """使用 pynput 启动监听"""
        # 元组格式：(keyboard.Key.alt, keyboard.KeyCode.from_char('w'))
        hotkey = keyboard.HotKey(self._hotkey, self._callback)

        # 创建监听器
        self._listener = keyboard.Listener(
            on_press=hotkey.press,
            on_release=hotkey.release
        )

        # 在后台线程运行
        self._listener.daemon = True
        self._listener.start()
        self._running = True
        logger.info(f"热键监听已启动: {self._hotkey}")

    def stop(self):
        """停止热键监听"""
        if self._listener:
            self._listener.stop()
            self._listener = None
        self._running = False
        logger.info("热键监听已停止")

    def is_running(self) -> bool:
        """检查是否正在监听"""
        return self._running


# 全局单例
_hotkey_manager: Optional[HotkeyManager] = None


def get_hotkey_manager() -> HotkeyManager:
    """获取全局 HotkeyManager 实例"""
    global _hotkey_manager
    if _hotkey_manager is None:
        _hotkey_manager = HotkeyManager()
    return _hotkey_manager


def register_global_hotkey(key: Tuple, callback: Callable) -> bool:
    """
    注册全局快捷键的便捷函数

    Args:
        key: 快捷键元组，必须使用 pynput.Key 枚举
        callback: 回调函数

    Returns:
        注册是否成功
    """
    manager = get_hotkey_manager()
    if manager.register_hotkey(key, callback):
        return manager.start()
    return False


def unregister_global_hotkey() -> bool:
    """注销全局快捷键的便捷函数"""
    manager = get_hotkey_manager()
    return manager.unregister_hotkey()
