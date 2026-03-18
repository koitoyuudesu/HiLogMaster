"""
文件处理器测试
"""

import unittest
import tempfile
import zipfile
import rarfile
from pathlib import Path
from src.core.file_handler import FileHandler


class TestFileHandler(unittest.TestCase):
    """文件处理器测试类"""

    def setUp(self):
        """测试前准备"""
        self.handler = FileHandler()
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """测试后清理"""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_detect_encoding_utf8(self):
        """测试 UTF-8 编码检测"""
        test_file = self.temp_dir / "test_utf8.txt"
        test_file.write_text("测试 UTF-8 编码", encoding='utf-8')

        encoding = self.handler.detect_encoding(test_file)
        self.assertIn('utf', encoding.lower())

    def test_is_zip_file(self):
        """测试 ZIP 文件识别"""
        # 创建测试 ZIP 文件
        zip_path = self.temp_dir / "test.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("test.txt", "test content")

        self.assertTrue(self.handler.is_zip_file(zip_path))

    def test_is_rar_file(self):
        """测试 RAR 文件识别"""
        # 注意：rarfile.is_rarfile() 需要真实的 RAR 文件
        # 这里只测试方法存在，实际测试需要真实 RAR 文件
        rar_path = self.temp_dir / "test.rar"
        # 创建一个空文件用于测试方法调用
        rar_path.touch()
        # 实际环境中需要真实的 RAR 文件才能返回 True
        result = self.handler.is_rar_file(rar_path)
        # 空文件不是有效的 RAR 文件，所以应该是 False
        self.assertFalse(result)

    def test_extract_zip(self):
        """测试 ZIP 解压"""
        # 创建包含 hilog 文件夹的 ZIP
        zip_path = self.temp_dir / "test.zip"
        extract_to = self.temp_dir / "extract"
        extract_to.mkdir()

        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.writestr("hilog/log1.txt", "log content 1")
            zf.writestr("hilog/log2.txt", "log content 2")

        hilog_path = self.handler.extract_zip(zip_path, extract_to)
        self.assertIsNotNone(hilog_path)
        self.assertTrue(hilog_path.exists())
        self.assertEqual(hilog_path.name, "hilog")

    def test_find_hilog_files(self):
        """测试查找 hilog 文件"""
        hilog_dir = self.temp_dir / "hilog"
        hilog_dir.mkdir()

        # 创建测试日志文件
        (hilog_dir / "log1.txt").write_text("log content 1")
        (hilog_dir / "log2.txt").write_text("log content 2")
        (hilog_dir / "readme.md").write_text("# Readme")

        files = self.handler.find_hilog_files(hilog_dir)
        self.assertEqual(len(files), 2)
        self.assertTrue(all(f.suffix == '.txt' for f in files))


if __name__ == '__main__':
    unittest.main()