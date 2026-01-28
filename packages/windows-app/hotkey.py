# MVP3 - 全局快捷键模块
import keyboard


def register_hotkey(hotkey, callback):
    """注册全局快捷键，suppress=True 阻止按键传递给其他应用"""
    keyboard.add_hotkey(hotkey, callback, suppress=True)


def unregister_hotkey(hotkey):
    """注销全局快捷键"""
    keyboard.remove_hotkey(hotkey)
