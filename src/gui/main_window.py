"""
主窗口模块
提供 LogMaster AI 的主 GUI 界面
"""

import customtkinter as ctk
import tkinterdnd2 as tkdnd
from pathlib import Path
from config import Config
from src.gui.widgets import FileDropArea, LogDisplay, ProgressBar


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
        """处理日志（占位符，待实现）"""
        if not self.selected_file:
            self.log_display.append_log("Error: No file selected!")
            return

        package_name = self.package_entry.get()
        if not package_name:
            self.log_display.append_log("Error: Please enter a package name or keyword!")
            return

        self.log_display.append_log(f"Processing file: {self.selected_file}")
        self.log_display.append_log(f"Package/Keyword: {package_name}")
        self.log_display.append_log("Processing... (Phase 1 implementation pending)")

    def run(self):
        """运行应用"""
        self.root.mainloop()