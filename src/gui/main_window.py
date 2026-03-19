"""
主窗口模块
提供 LogMaster AI 的主 GUI 界面
"""

import customtkinter as ctk
import tkinterdnd2 as tkdnd
import tempfile
import shutil
from pathlib import Path
from typing import List
from config import Config
from src.gui.widgets import FileDropArea, LogDisplay, ProgressBar
from src.core.file_handler import FileHandler
from src.core.log_parser import LogParser, LogEntry
from src.core.log_filter import LogFilter


class LogMasterApp:
    """LogMaster AI 主应用类"""

    def __init__(self):
        # 创建支持拖放的根窗口
        self.root = tkdnd.TkinterDnD.Tk()
        self.root.title("LogMaster AI")
        self.root.geometry("800x600")

        # 存储选中的文件
        self.selected_file: Path = None

        # Setup GUI
        self.setup_ui()

    def setup_ui(self):
        """设置用户界面"""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Package name input
        package_label = ctk.CTkLabel(main_frame, text="Target Package Name/Keyword:")
        package_label.pack(pady=(10, 0))

        self.package_entry = ctk.CTkEntry(main_frame, width=400)
        self.package_entry.pack(pady=(0, 10))

        # File drag and drop area
        self.drop_area = FileDropArea(
            main_frame,
            on_file_selected=self.on_file_selected,
            height=150
        )
        self.drop_area.pack(fill="x", pady=10)

        # Process button
        process_btn = ctk.CTkButton(main_frame, text="Process Logs", command=self.process_logs)
        process_btn.pack(pady=10)

        # Progress bar
        self.progress_bar = ProgressBar(main_frame)
        self.progress_bar.pack(fill="x", padx=20, pady=(10, 0))

        # Log display area
        log_label = ctk.CTkLabel(main_frame, text="Log Output:")
        log_label.pack(pady=(20, 5))

        self.log_display = LogDisplay(main_frame, height=200)
        self.log_display.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def on_file_selected(self, file_path: Path):
        """文件选中回调"""
        self.selected_file = file_path
        self.log_display.append_log(f"File selected: {file_path}")

    def process_logs(self):
        """处理日志"""
        if not self.selected_file:
            self.log_display.append_log("Error: No file selected!")
            return

        package_name = self.package_entry.get()
        if not package_name:
            self.log_display.append_log("Error: Please enter a package name or keyword!")
            return

        self.log_display.append_log(f"Processing file: {self.selected_file}")
        self.log_display.append_log(f"Package/Keyword: {package_name}")
        self.log_display.append_log("=" * 50)

        # 创建临时目录用于解压
        temp_dir = None
        try:
            temp_dir = Path(tempfile.mkdtemp(prefix="logmaster_"))
            file_handler = FileHandler()
            log_parser = LogParser()
            log_filter = LogFilter(log_parser)

            # 根据文件类型处理
            hilog_dir = None
            if file_handler.is_zip_file(self.selected_file) or file_handler.is_rar_file(self.selected_file):
                self.log_display.append_log("Extracting archive file...")
                hilog_dir = file_handler.extract_archive(self.selected_file, temp_dir)
                if not hilog_dir:
                    self.log_display.append_log("Error: 'hilog' folder not found in archive!")
                    return
                self.log_display.append_log(f"Found hilog folder: {hilog_dir}")
            elif self.selected_file.suffix.lower() == '.txt':
                self.log_display.append_log("Processing text file directly...")
                hilog_dir = self.selected_file.parent
            else:
                self.log_display.append_log("Error: Unsupported file format! Please use ZIP, RAR, or TXT.")
                return

            # 查找所有日志文件
            if self.selected_file.suffix.lower() == '.txt':
                log_files = [self.selected_file]
            else:
                log_files = file_handler.find_hilog_files(hilog_dir)

            if not log_files:
                self.log_display.append_log("Error: No log files found!")
                return

            self.log_display.append_log(f"Found {len(log_files)} log file(s)")

            # 流式读取并处理所有日志文件
            all_entries: List[LogEntry] = []
            total_lines = 0

            for log_file in log_files:
                self.log_display.append_log(f"Reading: {log_file.name}")
                self.progress_bar.update_progress(0.1)

                for line in file_handler.read_lines_stream(log_file):
                    total_lines += 1
                    entry = log_parser.parse_line(line)
                    if entry:
                        all_entries.append(entry)

                self.progress_bar.update_progress(0.5)

            self.log_display.append_log(f"Parsed {len(all_entries)} valid log entries from {total_lines} lines")

            # 筛选日志
            self.log_display.append_log("Filtering logs...")
            filtered_entries = log_filter.filter_with_context(all_entries, package_name)

            if not filtered_entries:
                self.log_display.append_log("No matching error logs found!")
                return

            self.log_display.append_log(f"Found {len(filtered_entries)} matching log entries (with context)")
            self.log_display.append_log("=" * 50)

            # 显示筛选结果
            self.log_display.append_log("FILTERED LOGS:")
            self.log_display.append_log("-" * 50)

            for entry in filtered_entries[:100]:  # 限制显示前100条
                self.log_display.append_log(entry.raw_line.strip())

            if len(filtered_entries) > 100:
                self.log_display.append_log(f"... and {len(filtered_entries) - 100} more entries")

            self.log_display.append_log("=" * 50)
            self.log_display.append_log(f"Phase 1 processing completed successfully!")
            self.log_display.append_log(f"Total filtered entries: {len(filtered_entries)}")

            self.progress_bar.update_progress(1.0)

        except Exception as e:
            self.log_display.append_log(f"Error during processing: {str(e)}")
            import traceback
            self.log_display.append_log(traceback.format_exc())
        finally:
            # 清理临时目录
            if temp_dir and temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir)
                    self.log_display.append_log("Cleaned up temporary files")
                except Exception as e:
                    self.log_display.append_log(f"Warning: Failed to cleanup temp dir: {str(e)}")

    def run(self):
        """运行应用"""
        self.root.mainloop()