"""
SQLite 管理器模块
管理 SQLite 数据库操作
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from config import Config


class SQLiteManager:
    """SQLite 数据库管理器"""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Config.SQLITE_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self):
        """连接数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.init_db()

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

    def init_db(self):
        """初始化数据库表"""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS log_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_name TEXT,
                file_path TEXT,
                archive_name TEXT,
                summary TEXT,
                error_count INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def insert_record(
        self,
        package_name: str,
        file_path: str,
        archive_name: str,
        summary: str,
        error_count: int
    ) -> int:
        """
        插入归档记录

        Args:
            package_name: 包名/关键字
            file_path: 归档文件路径
            archive_name: 归档文件夹名称
            summary: 分析摘要
            error_count: 错误日志行数

        Returns:
            插入记录的 ID
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO log_records (
                package_name, file_path, archive_name, summary, error_count
            ) VALUES (?, ?, ?, ?, ?)
        """, (package_name, file_path, archive_name, summary, error_count))
        self.conn.commit()
        return cursor.lastrowid

    def query_by_package(self, package_name: str) -> List[Dict]:
        """
        根据包名查询记录

        Args:
            package_name: 包名/关键字

        Returns:
            记录列表
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM log_records WHERE package_name LIKE ?
        """, (f"%{package_name}%",))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    def query_all(self) -> List[Dict]:
        """
        查询所有记录

        Returns:
            记录列表
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM log_records")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]