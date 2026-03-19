"""
自定义 GUI 组件模块
提供可复用的 CustomTkinter 组件
"""

import customtkinter as ctk
import tkinterdnd2 as tkdnd
from tkinter import filedialog
from pathlib import Path
from typing import Optional, Callable


class FileDropArea(ctk.CTkFrame):
    """文件拖放区域组件"""

    def __init__(self, master, on_file_selected: Optional[Callable] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_file_selected = on_file_selected
        self.selected_file: Optional[Path] = None

        # 启用拖放
        self.drop_target_register(tkdnd.DND_FILES)

        # 标签
        self.label = ctk.CTkLabel(self, text="Drag & Drop Log File Here\nor Click to Browse")
        self.label.pack(expand=True, padx=20, pady=20)

        # 绑定事件
        self.dnd_bind('<<Drop>>', self.on_drop)
        self.bind("<Button-1>", self.on_click)

    def on_drop(self, event):
        """处理文件拖放事件"""
        files = self.tk.splitlist(event.data)
        if files:
            file_path = Path(files[0].replace("{", "").replace("}", ""))
            self.set_file(file_path)

    def on_click(self, event):
        """处理点击事件，打开文件选择器"""
        file_path = filedialog.askopenfilename(
            title="Select Log File",
            filetypes=[
                ("All Supported Files", "*.zip *.rar *.txt"),
                ("ZIP Files", "*.zip"),
                ("RAR Files", "*.rar"),
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.set_file(Path(file_path))

    def set_file(self, file_path: Path):
        """设置选中的文件"""
        self.selected_file = file_path
        self.label.configure(text=f"Selected: {file_path.name}")
        if self.on_file_selected:
            self.on_file_selected(file_path)

    def clear(self):
        """清除选中的文件"""
        self.selected_file = None
        self.label.configure(text="Drag & Drop Log File Here\nor Click to Browse")


class LogDisplay(ctk.CTkTextbox):
    """日志显示组件"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def append_log(self, text: str):
        """追加日志文本"""
        self.insert("end", text + "\n")
        self.see("end")


class ProgressBar(ctk.CTkProgressBar):
    """进度条组件"""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.set(0)

    def update_progress(self, value: float):
        """更新进度"""
        self.set(value)