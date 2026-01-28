# MVP3 - 桌面级文本润色验证工具
# 主入口文件

from gui import PolishWindow
from focus import FocusManager
from hotkey import register_hotkey
import logger

# # Task 4 测试用例：复杂文本（约 150 字）
# TEST_TEXT = """\
# # MVP3 文本润色工具 🚀
#
# ## 功能验证 ✅
#
# The quick brown fox jumps over the lazy dog.
# 敏捷的棕色狐狸跳过了懒惰的狗。🦊
#
# ### 测试项
#
# - **英文字符**: ABCDEFG abcdefg 0123456789
# - **中文字符**: 你好世界，这是一段测试文本
# - **特殊符号**: @#$%^&*() 【】「」
# - **Emoji**: 😀 🎉 💻 ❤️ 👍
#
# > 这是一段引用文字，用于测试多行场景。
#
# 完成！Done! 🎊"""

# 全局焦点管理器
focus_mgr = FocusManager()
window = None


def on_hotkey():
    """快捷键回调：唤起 GUI"""
    logger.info("快捷键触发: Alt+W")
    
    # 记录当前前台窗口（唤起前）
    hwnd = focus_mgr.save_current_focus()
    logger.debug(f"已记录原窗口句柄: {hwnd}")
    
    # 显示 GUI
    window.show()


def on_accept(text):
    """Accept 按钮回调：将右侧文本注入原窗口"""
    logger.info(f"Accept 点击，准备注入 {len(text)} 字符")
    
    # 检查是否有保存的窗口句柄
    if not focus_mgr.saved_hwnd:
        logger.warning("没有保存的窗口句柄，跳过注入")
        window.hide()
        return
    
    # 隐藏 GUI 并恢复焦点
    window.hide()
    logger.debug(f"恢复焦点到窗口: {focus_mgr.saved_hwnd}")
    focus_mgr.restore_focus(delay_ms=100)  # spec 建议 50-200ms
    
    # 注入 GUI 右侧文本到原窗口
    if text:
        focus_mgr.type_text(text)
        logger.info("文本注入完成")
    else:
        logger.debug("文本为空，跳过注入")


def main():
    global window
    
    logger.info("MVP3 启动")
    logger.info("按 Alt+W 唤起窗口")
    logger.info("流程：左侧输入原文 → 右侧编辑润色 → Accept 上屏")
    
    # 创建 GUI（但不显示）
    window = PolishWindow(on_accept_callback=on_accept)
    
    # 注册全局快捷键
    register_hotkey('alt+w', on_hotkey)
    
    # 启动时隐藏窗口
    window.hide()
    
    # 进入主循环
    window.run()


if __name__ == "__main__":
    main()
