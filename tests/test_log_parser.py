"""
日志解析器测试
"""

import unittest
from src.core.log_parser import LogParser, LogEntry


class TestLogParser(unittest.TestCase):
    """日志解析器测试类"""

    def setUp(self):
        """测试前准备"""
        self.parser = LogParser()

    def test_parse_valid_log_line(self):
        """测试解析有效的日志行"""
        log_line = "03-09 20:03:26.404 50989 50989 E A00901/ei.hmos.accountcontactsservice/ACCOUNT_CONTACTS: [PosterCloudService]: setPosterAuthorizationIncre failed"
        entry = self.parser.parse_line(log_line)

        self.assertIsNotNone(entry)
        self.assertEqual(entry.timestamp, "03-09 20:03:26.404")
        self.assertEqual(entry.pid, 50989)
        self.assertEqual(entry.tid, 50989)
        self.assertEqual(entry.level, "E")
        self.assertIn("ACCOUNT_CONTACTS", entry.tag)

    def test_parse_invalid_log_line(self):
        """测试解析无效的日志行"""
        log_line = "This is not a valid log line"
        entry = self.parser.parse_line(log_line)
        self.assertIsNone(entry)

    def test_is_error_level(self):
        """测试 Error 级别识别"""
        entry = LogEntry(
            timestamp="03-09 20:03:26.404",
            pid=50989,
            tid=50989,
            level="E",
            tag="TAG",
            content="error message",
            raw_line="raw line"
        )
        self.assertTrue(self.parser.is_error_level(entry))

    def test_contains_keyword(self):
        """测试关键字匹配"""
        entry = LogEntry(
            timestamp="03-09 20:03:26.404",
            pid=50989,
            tid=50989,
            level="E",
            tag="com.example.app",
            content="error message",
            raw_line="com.example.app error occurred"
        )
        self.assertTrue(self.parser.contains_keyword(entry, "com.example.app"))
        self.assertFalse(self.parser.contains_keyword(entry, "other.package"))


if __name__ == '__main__':
    unittest.main()