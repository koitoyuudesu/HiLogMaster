"""
日志工具模块
提供统一的日志记录功能
"""

import logging
from pathlib import Path
from config import Config


def setup_logger(
    name: str = "logmaster",
    level: str = None,
    log_file: Path = None
) -> logging.Logger:
    """
    配置日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)

    if level is None:
        level = Config.LOG_LEVEL

    if log_file is None:
        log_file = Config.LOG_FILE_PATH

    logger.setLevel(getattr(logging, level.upper()))

    # 清除已有的处理器
    logger.handlers.clear()

    # 文件处理器
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger