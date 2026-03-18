"""
文件处理器模块
处理 ZIP/RAR 解压、编码检测、流式读取等文件操作
"""

import os
import zipfile
import rarfile
import chardet
from pathlib import Path
from typing import Iterator, Optional
from config import Config


class FileHandler:
    """文件处理器"""

    def __init__(self):
        self.hilog_folder = Config.HILOG_FOLDER

    def extract_zip(self, zip_path: Path, extract_to: Path) -> Optional[Path]:
        """
        解压 ZIP 文件，递归查找 hilog 文件夹

        Args:
            zip_path: ZIP 文件路径
            extract_to: 解压目标目录

        Returns:
            hilog 文件夹路径，如果未找到则返回 None
        """
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        # 递归查找 hilog 文件夹
        for root, dirs, files in os.walk(extract_to):
            if self.hilog_folder in dirs:
                return Path(root) / self.hilog_folder

        return None

    def detect_encoding(self, file_path: Path) -> str:
        """
        检测文件编码

        Args:
            file_path: 文件路径

        Returns:
            编码名称（如 'utf-8', 'gbk'）
        """
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # 读取前 10000 字节用于检测
            result = chardet.detect(raw_data)
            return result['encoding'] or 'utf-8'

    def read_lines_stream(self, file_path: Path) -> Iterator[str]:
        """
        流式读取文件行

        Args:
            file_path: 文件路径

        Yields:
            文件行
        """
        encoding = self.detect_encoding(file_path)
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            for line in f:
                yield line

    def find_hilog_files(self, directory: Path) -> list[Path]:
        """
        在目录中查找所有 .txt 日志文件

        Args:
            directory: 目录路径

        Returns:
            日志文件路径列表
        """
        return list(directory.glob("*.txt"))

    def is_zip_file(self, file_path: Path) -> bool:
        """
        判断是否为 ZIP 文件

        Args:
            file_path: 文件路径

        Returns:
            是否为 ZIP 文件
        """
        return zipfile.is_zipfile(file_path)

    def is_rar_file(self, file_path: Path) -> bool:
        """
        判断是否为 RAR 文件

        Args:
            file_path: 文件路径

        Returns:
            是否为 RAR 文件
        """
        return rarfile.is_rarfile(file_path)

    def extract_rar(self, rar_path: Path, extract_to: Path) -> Optional[Path]:
        """
        解压 RAR 文件，递归查找 hilog 文件夹

        Args:
            rar_path: RAR 文件路径
            extract_to: 解压目标目录

        Returns:
            hilog 文件夹路径，如果未找到则返回 None
        """
        with rarfile.RarFile(rar_path) as rar_ref:
            rar_ref.extractall(extract_to)

        # 递归查找 hilog 文件夹
        for root, dirs, files in os.walk(extract_to):
            if self.hilog_folder in dirs:
                return Path(root) / self.hilog_folder

        return None

    def extract_archive(self, archive_path: Path, extract_to: Path) -> Optional[Path]:
        """
        解压压缩文件（支持 ZIP 和 RAR），递归查找 hilog 文件夹

        Args:
            archive_path: 压缩文件路径
            extract_to: 解压目标目录

        Returns:
            hilog 文件夹路径，如果未找到则返回 None
        """
        if self.is_zip_file(archive_path):
            return self.extract_zip(archive_path, extract_to)
        elif self.is_rar_file(archive_path):
            return self.extract_rar(archive_path, extract_to)
        else:
            return None