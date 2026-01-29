"""
MVP3 - 桌面级文本润色验证工具
"""

import logging
import logger_config  # 只为触发全局日志配置，无变量冲突
import keyboard
from gui import WisadelWindow
from focus import FocusManager

logger = logging.getLogger(__name__)


def register_hotkey(hotkey, callback):
    """注册全局快捷键，suppress=True 阻止按键传递给其他应用"""
    keyboard.add_hotkey(hotkey, callback, suppress=True)


# 全局焦点管理器
focus_mgr = FocusManager()
window = None


def on_hotkey():
    """快捷键回调：唤起 GUI"""
    logger.debug("快捷键触发: Alt+W")
    
    # 记录当前前台窗口（唤起前）
    hwnd = focus_mgr.save_current_focus()
    logger.debug(f"已记录原窗口句柄: {hwnd}")
    
    # 显示 GUI
    window.show()


def on_accept(text):
    """Accept 按钮回调：将右侧文本注入原窗口"""
    logger.debug(f"Accept 点击，准备注入 {len(text)} 字符")

    # 检查是否有保存的窗口句柄
    if not focus_mgr.saved_window_handle:
        logger.warning("没有保存的窗口句柄，跳过注入")
        window.hide()
        return

    # 隐藏 GUI 并恢复焦点
    window.hide()
    logger.debug(f"恢复焦点到窗口: {focus_mgr.saved_window_handle}")
    # 延迟原因：GUI 隐藏和焦点转移需要时间，避免竞争条件导致焦点设置失败
    focus_mgr.restore_focus(delay_ms=100)
    
    # 注入 GUI 右侧文本到原窗口
    if text:
        focus_mgr.type_text(text)
        logger.debug("文本注入完成")
    else:
        logger.debug("文本为空，跳过注入")


def main():
    # 需要对全局变量 window 赋值，其他函数只读取
    global window
    
    logger.info("=" * 50)
    logger.info("  MVP3 - 桌面级文本润色验证工具")
    logger.info("=" * 50)
    logger.info("  快捷键: Alt+W")
    logger.info("  流程: 左侧输入原文 → 右侧编辑润色 → Accept 上屏")
    logger.info("=" * 50)
    
    # 创建 GUI（但不显示）
    window = WisadelWindow(on_accept_callback=on_accept)
    
    # 注册全局快捷键
    register_hotkey('alt+w', on_hotkey)
    
    # 启动时隐藏窗口
    window.hide()
    
    # 进入主循环
    window.run()


if __name__ == "__main__":
    main()
