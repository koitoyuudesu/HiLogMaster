"""
日志筛选器模块
筛选 Error 级别日志，提取上下文
"""

from typing import List, Optional
from src.core.log_parser import LogEntry, LogParser
from config import Config


class LogFilter:
    """日志筛选器"""

    def __init__(self, parser: LogParser):
        self.parser = parser
        self.context_lines = Config.CONTEXT_LINES

    def filter_by_level_and_keyword(
        self,
        entries: List[LogEntry],
        keyword: str
    ) -> List[LogEntry]:
        """
        筛选 Error 级别且包含关键字的日志

        Args:
            entries: 日志条目列表
            keyword: 关键字

        Returns:
            筛选后的日志条目列表
        """
        filtered = []
        for entry in entries:
            if self.parser.is_error_level(entry) and self.parser.contains_keyword(entry, keyword):
                filtered.append(entry)
        return filtered

    def extract_context(
        self,
        all_entries: List[LogEntry],
        target_entry: LogEntry
    ) -> List[LogEntry]:
        """
        提取目标日志条目的上下文

        Args:
            all_entries: 所有日志条目
            target_entry: 目标日志条目

        Returns:
            包含上下文的日志条目列表
        """
        try:
            index = all_entries.index(target_entry)
        except ValueError:
            return [target_entry]

        start = max(0, index - self.context_lines)
        end = min(len(all_entries), index + self.context_lines + 1)
        return all_entries[start:end]

    def filter_with_context(
        self,
        all_entries: List[LogEntry],
        keyword: str
    ) -> List[LogEntry]:
        """
        筛选日志并提取上下文

        Args:
            all_entries: 所有日志条目
            keyword: 关键字

        Returns:
            包含上下文的筛选结果
        """
        filtered_entries = self.filter_by_level_and_keyword(all_entries, keyword)
        result = []

        for entry in filtered_entries:
            context = self.extract_context(all_entries, entry)
            result.extend(context)

        return result