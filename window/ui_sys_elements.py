import logging
from typing import Literal
from config import config
from log.log_config import TextHandler
from window.variables import Variables
import tkinter as tk

# 基础设置ui
class UiSysElements(Variables):
    def __init__(self):
        super().__init__()
        self.ui_sys_elements = self._create_ui_sys_elements(self.log_level_selection)
        # 初始化时更新标签
        self._update_log_level(self.log_level_selection.get(), "log_level")


    def _hide_ui_sys_elements(self):
        for element in self.ui_sys_elements.values():
            element.grid_remove()

    def _show_ui_sys_elements(self):
        for element in self.ui_sys_elements.values():
            element.grid()

    def _update_log_level(self,selection, group):
        if group == "log_level":
            if selection == "debug":
                config.log_level = logging.DEBUG
            elif selection == "info":
                config.log_level = logging.INFO
            elif selection == "error":
                config.log_level = logging.ERROR
            else:
                config.log_level = logging.INFO
            self.text_handler = TextHandler(self.log_text)
            self.text_handler.set_handler()

    def _vcmd_bigger_than_negative(self)  -> tuple[str, Literal['%P']]:
        # 使用 validate 命令限制输入
        return (self.register(self._validate_bigger_than_negative), '%P') 
    
    def _validate_bigger_than_negative(self,P) -> bool:
        # 验证输入，仅接受数字和小数点
        if P == "":  # 允许空输入
            return True
        if P.count('.') > 1:  # 只允许一个小数点
            return False
        return P.isdigit() or (P.count('.') == 1 and P.replace('.', '').isdigit())
    
    def _vcmd_validate_integer(self)  -> tuple[str, Literal['%P']]:
        # 使用 validate 命令限制输入
        return (self.register(self._validate_integer), '%P') 
    
    def _validate_integer(self,P) -> bool:
        if P.isdigit() and int(P) >= 0:
            return True
        return False

    def _create_ui_sys_elements(self,log_level_selection):
        log_level_choose = tk.Label(self, text="日志等级: ")
        log_level_choose.grid(row=2, column=0, padx=10, pady=5)

        choose_debug = tk.Radiobutton(self, text="Debug", variable=log_level_selection, value="debug",
                                command=lambda: self._update_log_level(log_level_selection.get(), "log_level"))
        choose_debug.grid(row=3, column=0, padx=10, pady=5)

        choose_info = tk.Radiobutton(self, text="Info", variable=log_level_selection, value="info",
                                command=lambda: self._update_log_level(log_level_selection.get(), "log_level"))
        choose_info.grid(row=3, column=1, padx=10, pady=5)

        choose_error = tk.Radiobutton(self, text="Error", variable=log_level_selection, value="error",
                                command=lambda: self._update_log_level(log_level_selection.get(), "log_level"))
        choose_error.grid(row=3, column=2, padx=10, pady=5)

        check_interval_label = tk.Label(self, text="基础信号检测间隔(秒):")
        check_interval_label.grid(row=4, column=0, padx=10, pady=5)
        check_interval_entry = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd_bigger_than_negative())
        check_interval_entry.insert(0, '0.2')
        check_interval_entry.grid(row=4, column=1, padx=10, pady=5)
        
        thornback_random_label = tk.Label(self, text="刺鱼频率(百分比):")
        thornback_random_label.grid(row=4, column=2, padx=10, pady=5)
        thornback_random_entry = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd_bigger_than_negative())
        thornback_random_entry.insert(0, '20')
        thornback_random_entry.grid(row=4, column=3, padx=10, pady=5)

        eat_label = tk.Label(self, text="食用食物间隔(按键4):")
        eat_label.grid(row=5, column=0, padx=10, pady=5)
        eat_entry = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd_bigger_than_negative())
        eat_entry.insert(0, '0')
        eat_entry.grid(row=5, column=1, padx=10, pady=5)

        drink_label = tk.Label(self, text="饮用饮品间隔(按键5):")
        drink_label.grid(row=5, column=2, padx=10, pady=5)
        drink_entry = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd_bigger_than_negative())
        drink_entry.insert(0, '0')
        drink_entry.grid(row=5, column=3, padx=10, pady=5)

        crafting_conf = tk.Label(self, text="制作配置:")
        crafting_conf.grid(row=6, column=0, padx=10, pady=5)
        crafting_label = tk.Label(self, text="制作总量:")
        crafting_label.grid(row=7, column=0, padx=10, pady=5)
        crafting_entry = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd_validate_integer())
        crafting_entry.insert(0, '0')
        crafting_entry.grid(row=7, column=1, padx=10, pady=5)
        crafting_button = tk.Button(self, text="开始制作", command=lambda: self._crafting_submit())
        crafting_button.grid(row=7, column=2, padx=10, pady=5)

        return {
            "log_level_choose": log_level_choose,
            "choose_debug": choose_debug,
            "choose_info": choose_info,
            "choose_error": choose_error,
            "check_interval_label": check_interval_label,
            "check_interval_entry": check_interval_entry,
            "thornback_random_label": thornback_random_label,
            "thornback_random_entry": thornback_random_entry,
            "eat_label": eat_label,
            "eat_entry": eat_entry,
            "drink_label": drink_label,
            "drink_entry": drink_entry,
            "crafting_conf": crafting_conf,
            "crafting_label": crafting_label,
            "crafting_entry": crafting_entry,
            "crafting_button": crafting_button
        }
    
    def _update_ui_sys_elements_text(self):
        if config.ui_language:
            self.ui_sys_elements["log_level_choose"].config(text="Log Level: ")
            self.ui_sys_elements["check_interval_label"].config(text="Base Signal Check Interval(s):")
            self.ui_sys_elements["thornback_random_label"].config(text="Thornback Frequency(%):")
            self.ui_sys_elements["eat_label"].config(text="Eat Food Interval(Key4):")
            self.ui_sys_elements["drink_label"].config(text="Drink Drink Interval(Key5):")
            self.ui_sys_elements["crafting_conf"].config(text="Crafting Config:")
            self.ui_sys_elements["crafting_label"].config(text="Crafting Total:")
            self.ui_sys_elements["crafting_button"].config(text="Go Crafting")
        else:
            self.ui_sys_elements["log_level_choose"].config(text="日志等级: ")
            self.ui_sys_elements["check_interval_label"].config(text="基础信号检测间隔(秒):")
            self.ui_sys_elements["thornback_random_label"].config(text="刺鱼频率(百分比):")
            self.ui_sys_elements["eat_label"].config(text="食用食物间隔(按键4):")
            self.ui_sys_elements["drink_label"].config(text="饮用饮品间隔(按键5):")
            self.ui_sys_elements["crafting_conf"].config(text="制作配置:")
            self.ui_sys_elements["crafting_label"].config(text="制作总量:")
            self.ui_sys_elements["crafting_button"].config(text="开始制作")


