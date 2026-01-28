# MVP3 - 日志模块
import logging
import sys

# 创建 logger
logger = logging.getLogger("Wisadel")
logger.setLevel(logging.DEBUG)

# 控制台输出
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# 格式：时间 - 级别 - 消息
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


def debug(msg):
    logger.debug(msg)


def info(msg):
    logger.info(msg)


def warning(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)
