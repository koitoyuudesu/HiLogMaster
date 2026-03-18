"""
日志解析器模块
解析 Hilog 日志行格式，提取关键字段
"""

import re
from dataclasses import dataclass
from typing import Optional
from config import Config


@dataclass
class LogEntry:
    """日志条目数据类"""
    timestamp: str
    pid: int
    tid: int
    level: str
    tag: str
    content: str
    raw_line: str


class LogParser:
    """Hilog 日志解析器"""

    def __init__(self):
        self.pattern = re.compile(Config.LOG_PATTERN)

    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        解析单行日志

        Args:
            line: 日志行文本

        Returns:
            LogEntry 对象，如果解析失败则返回 None
        """
        match = self.pattern.match(line.strip())
        if not match:
            return None

        timestamp, pid, tid, level, tag, content = match.groups()
        return LogEntry(
            timestamp=timestamp,
            pid=int(pid),
            tid=int(tid),
            level=level,
            tag=tag,
            content=content,
            raw_line=line
        )

    def is_error_level(self, entry: LogEntry) -> bool:
        """
        判断是否为 Error 级别

        Args:
            entry: 日志条目

        Returns:
            是否为 Error 级别
        """
        return entry.level == Config.ERROR_LEVEL

    def contains_keyword(self, entry: LogEntry, keyword: str) -> bool:
        """
        判断日志是否包含关键字

        Args:
            entry: 日志条目
            keyword: 关键字

        Returns:
            是否包含关键字
        """
        return keyword.lower() in entry.raw_line.lower()