"""
LogMaster AI - 主入口文件
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from config import Config
from src.gui.main_window import LogMasterApp
from src.db.sqlite_manager import SQLiteManager
from src.db.vector_store import VectorStore


def main():
    """主函数"""
    # 确保必要的目录存在
    Config.ensure_directories()

    # 初始化数据库
    sqlite_manager = SQLiteManager()
    sqlite_manager.connect()

    # 初始化向量存储
    vector_store = VectorStore()

    # 启动 GUI 应用
    app = LogMasterApp()
    app.run()

    # 清理资源
    sqlite_manager.close()


if __name__ == "__main__":
    main()