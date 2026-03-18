"""
配置管理模块
集中管理 LogMaster AI 的所有配置项
"""

import os
from pathlib import Path
from typing import List


class Config:
    """配置管理类"""

    # 项目根目录
    ROOT_DIR = Path(__file__).parent

    # 数据目录
    DATA_DIR = ROOT_DIR / "data"
    LOGS_DIR = DATA_DIR / "logs"
    ARCHIVES_DIR = DATA_DIR / "archives"
    DB_DIR = DATA_DIR / "db"

    # LLM 配置
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "llama2")

    # 归档配置
    ARCHIVE_ROOT_DIR = ARCHIVES_DIR
    CONTEXT_LINES = 1  # 错误日志前后提取的上下文行数

    # 数据库配置
    SQLITE_DB_PATH = DB_DIR / "log_records.db"
    CHROMADB_PATH = DB_DIR / "chromadb_data"

    # 默认关键字列表
    DEFAULT_KEYWORDS: List[str] = [
        "com.example.app",
        "com.harmonyos.app",
        "com.huawei.app"
    ]

    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FILE_PATH = ROOT_DIR / "logmaster.log"

    # Hilog 日志格式配置
    HILOG_FOLDER = "hilog"
    ERROR_LEVEL = "E"
    LOG_PATTERN = r"(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{3})\s+(\d+)\s+(\d+)\s+([E|W|I|D|F])\s+([^:]+):\s+(.+)"

    @classmethod
    def ensure_directories(cls):
        """确保所有必要的目录存在"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        cls.ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)
        cls.DB_DIR.mkdir(parents=True, exist_ok=True)