import tkinter as tk
from tkinter import ttk

class BaseApp(tk.Tk):
    def __init__(self):
        super().__init__()  # 调用父类的构造函数
        
        self.title("rf4helper")
        self.geometry("900x700")

        # 设置主题
        style = ttk.Style()
        style.configure("TButton", background="lightblue")
        style.configure("TLabel", background="lightblue")
        
        self._create_log_el()

    # 日志框
    def _create_log_el(self):
        # 创建文本区域用于显示日志
        self.log_text = tk.Text(self, height=15, width=100)
        self.log_text.grid(row=17, column=0, padx=10, pady=5, columnspan=3)  # 使用 grid 布局

        # 创建滚动条，方便查看日志
        self.scrollbar = tk.Scrollbar(self, command=self.log_text.yview)
        self.scrollbar.grid(row=17, column=3, sticky='ns')  # 使用 grid 布局并设置为垂直方向填充
        self.log_text.config(yscrollcommand=self.scrollbar.set)