"""
MVP3 - 日志模块（全局配置）
"""

import logging
import sys

# 清除 PyDev 可能已配置的 handlers
logging.root.handlers.clear()

# 直接添加 console handler 到根 logger
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s', datefmt='%H:%M:%S'))
logging.root.addHandler(console_handler)
logging.root.setLevel(logging.DEBUG)
