
import sys
import threading
from game_model.go_fishing import go_fishing
from game_model.go_crafting import go_crafting
from window.ui_rod_elements import UiRodElements
from window.ui_sys_elements import UiSysElements
import config.config as myconfig
import tkinter as tk
import operating_signal.operating_signal as op


class App(UiSysElements,UiRodElements):
    def __init__(self):
        super().__init__()
        # 创建基础按钮和日志框
        self.base_button = self._create_base_button()
        self.top_button = self._create_top_button()
        self._update_ui_selection(self.ui_selection.get())

    def _update_ui_selection(self, value):
        if value == "ui_rod":
            self._hide_ui_sys_elements()
            self._show_ui_rod_base()
            self._update_rod_radios(self.rod_selection.get(), "rod_type")
        elif value == "ui_sys":
            self._hide_ui_rod_elements()
            self._show_ui_sys_elements()

    def _hide_top_button(self) -> None:
        for element in self.top_button.values():
            element.grid_remove()

    def _show_top_button(self) -> None:
        for element in self.top_button.values():
            element.grid()
    
    def _hide_ui_rod_elements(self) -> None:
        for element in self.rod_base.values():
            element.grid_remove()
        for element in self.lure_roll_type.values():
            element.grid_remove()
        for element in self.water_bottom_model.values():
            element.grid_remove()
        for element in self.lure_conf.values():
            element.grid_remove()
        for element in self.lure_jerk_bait_conf.values():
            element.grid_remove()
        for element in self.lure_jump_shot_conf.values():
            element.grid_remove()
        for element in self.lure_float_downstream_conf.values():
            element.grid_remove()
        for element in self.water_bottom_conf.values():
            element.grid_remove()
        for element in self.tenkara_conf.values():
            element.grid_remove()

    def _show_ui_rod_base(self) -> None:
        for element in self.rod_base.values():
            element.grid()      
    
    def _create_top_button(self) -> dict[str, tk.Button]:
        # 钓具配置按钮
        rod_choose_button = tk.Button(self, text="钓具配置:", command=lambda: self._update_ui_selection("ui_rod"))
        rod_choose_button.grid(row=1, column=0, padx=10, pady=5)

        # 创建基础配置按钮
        sys_choose_button = tk.Button(self, text="基础配置:", command=lambda: self._update_ui_selection("ui_sys"))
        sys_choose_button.grid(row=1, column=1, padx=10, pady=5)

        # 创建ui语言切换按钮
        update_ui_language_button = tk.Button(self, text="switch to EN", command=self._update_ui_text)
        update_ui_language_button.grid(row=1, column=2, padx=10, pady=5)
        return {
            "rod_choose_button" : rod_choose_button,
            "sys_choose_button" : sys_choose_button,
            "update_ui_language_button" : update_ui_language_button
        }

        # 基础按钮
    def _create_base_button(self) -> dict[str, tk.Button]:
        # 创建提交按钮
        submit_button = tk.Button(self, text="开始钓鱼", command=self._submit)
        submit_button.grid(row=16, column=0, padx=10, pady=5)
        # 创建清空日志按钮
        clear_button = tk.Button(self, text="清空日志", command=self._clear_log)
        clear_button.grid(row=16, column=1, padx=10, pady=5)
        # 创建折叠按钮
        fold_ui_button = tk.Button(self, text="折叠/展开", command=self._fold_ui)
        fold_ui_button.grid(row=16, column=2, padx=10, pady=5)
        # 创建退出按钮
        close_button = tk.Button(self, text="退出程序", command=lambda: self._close())
        close_button.grid(row=16, column=3, padx=10, pady=5)

        return {
            "submit_button" : submit_button,
            "clear_button" : clear_button,
            "fold_ui_button" : fold_ui_button,
            "close_button" : close_button,
        }

    def _update_base_button_text(self):
        if myconfig.ui_language:
            # 更新base_button的内容
            self.base_button["submit_button"].config(text="Go Fishing")
            self.base_button["clear_button"].config(text="Clear Log")
            self.base_button["fold_ui_button"].config(text="fold/Expand")
            self.base_button["close_button"].config(text="Quit")

            self.top_button["rod_choose_button"].config(text="Rod Config")
            self.top_button["sys_choose_button"].config(text="SYS Config")
            self.top_button["update_ui_language_button"].config(text="切换至中文")
        else:
            # 更新base_button的内容
            self.base_button["submit_button"].config(text="开始钓鱼")
            self.base_button["clear_button"].config(text="清空日志")
            self.base_button["fold_ui_button"].config(text="折叠/展开")
            self.base_button["close_button"].config(text="退出程序")

            self.top_button["rod_choose_button"].config(text="钓具配置")
            self.top_button["sys_choose_button"].config(text="基础配置")
            self.top_button["update_ui_language_button"].config(text="Switch To EN")

    # 清空日志
    def _clear_log(self):
        self.log_text.delete('1.0', tk.END)

    # 折叠UI界面
    def _fold_ui(self):
        # 隐藏/展示配置项
        if myconfig.attributes:
            self._hide_ui_rod_elements()
            self._hide_ui_sys_elements()
            self._hide_top_button()
            self.geometry("800x249")
        else:
            self._show_top_button()
            self.geometry("900x700")
            self._update_ui_selection(self.ui_selection.get())
        self.attributes("-topmost", myconfig.attributes)  # 窗口置顶
        myconfig.attributes = not myconfig.attributes

    # 关闭程序
    def _close(self):
        # 向其他线程发送停止标志位
        myconfig.stop_signal = True
        # 关闭窗口
        self.destroy()
        sys.exit()

    def _update_ui_text(self):
        self._update_base_button_text()
        self._update_ui_sys_elements_text()
        self.update_rod_base_text()
        myconfig.ui_language = not myconfig.ui_language
        op.update_file_path()
        
        


    def _submit(self) -> None:
        # 路亚配置输入获取
        # ###############后续其他收线方式支持多竿再配置  l_rod_num###############
        # if len(self.lure_conf["l_rod_num"].get())>0:
        #     self.fishing_config.lure_config.l_rod_num = int(self.lure_conf["l_rod_num"].get())
        # else:
        #     self.fishing_config.lure_config.l_rod_num = 1
        if self.fishing_config.lure_config.roll_type == 'jump_shot':
            if len(self.lure_conf["l_rod_num_double"].get())>0:
                self.fishing_config.lure_config.l_rod_num = int(self.lure_conf["l_rod_num_double"].get())
            else:
                self.fishing_config.lure_config.l_rod_num = 1
        else:
            self.fishing_config.lure_config.l_rod_num = 1
        if len(self.lure_conf["l_strength"].get())>0:
            self.fishing_config.lure_config.l_strength = float(self.lure_conf["l_strength"].get())
        else:
            self.fishing_config.lure_config.l_strength = 0.8
        if len(self.lure_conf["l_throw_offset"].get())>0:
            self.fishing_config.lure_config.l_throw_offset = float(self.lure_conf["l_throw_offset"].get())
        else:
            self.fishing_config.lure_config.l_throw_offset = 0
        if len(self.lure_conf["l_wait_time"].get())>0:
            self.fishing_config.lure_config.l_wait_time = float(self.lure_conf["l_wait_time"].get())
        else:
            self.fishing_config.lure_config.l_wait_time = 2
        if len(self.lure_conf["l_wait_time_offset"].get())>0:
            self.fishing_config.lure_config.l_wait_time_offset = float(self.lure_conf["l_wait_time_offset"].get())
        else:
            self.fishing_config.lure_config.l_wait_time_offset = 1
        # 犬步/jig等抽停动作
        if len(self.lure_jerk_bait_conf["l_dog_walk_time"].get())>0:
            self.fishing_config.lure_config.l_dog_walk_time = float(self.lure_jerk_bait_conf["l_dog_walk_time"].get())
        else:
            self.fishing_config.lure_config.l_dog_walk_time = 0.3
        if len(self.lure_jerk_bait_conf["l_dog_walk_time_offset"].get())>0:
            self.fishing_config.lure_config.l_dog_walk_time_offset = float(self.lure_jerk_bait_conf["l_dog_walk_time_offset"].get())
        else:
            self.fishing_config.lure_config.l_dog_walk_time_offset = 0.2
        if len(self.lure_jerk_bait_conf["l_dog_walk_wait_time"].get())>0:
            self.fishing_config.lure_config.l_dog_walk_wait_time = float(self.lure_jerk_bait_conf["l_dog_walk_wait_time"].get())
        else:
            self.fishing_config.lure_config.l_dog_walk_wait_time = 0.3
        if len(self.lure_jerk_bait_conf["l_dog_walk_wait_time_offset"].get())>0:
            self.fishing_config.lure_config.l_dog_walk_wait_time_offset = float(self.lure_jerk_bait_conf["l_dog_walk_wait_time_offset"].get())
        else:
            self.fishing_config.lure_config.l_dog_walk_wait_time_offset = 0.2
        # 跳底动作
        if len(self.lure_jump_shot_conf["l_roll_line_time"].get())>0:
            self.fishing_config.lure_config.l_roll_line_time = float(self.lure_jump_shot_conf["l_roll_line_time"].get())
        else:
            self.fishing_config.lure_config.l_roll_line_time = 1
        if len(self.lure_jump_shot_conf["l_roll_line_time_offset"].get())>0:
            self.fishing_config.lure_config.l_roll_line_time_offset = float(self.lure_jump_shot_conf["l_roll_line_time_offset"].get())
        else:
            self.fishing_config.lure_config.l_roll_line_time_offset = 0.2
        if len(self.lure_jump_shot_conf["l_roll_line_wait_time"].get())>0:
            self.fishing_config.lure_config.l_roll_line_wait_time = float(self.lure_jump_shot_conf["l_roll_line_wait_time"].get())
        else:
            self.fishing_config.lure_config.l_roll_line_wait_time = 9
        if len(self.lure_jump_shot_conf["l_roll_line_wait_time_offset"].get())>0:
            self.fishing_config.lure_config.l_roll_line_wait_time_offset = float(self.lure_jump_shot_conf["l_roll_line_wait_time_offset"].get())
        else:
            self.fishing_config.lure_config.l_roll_line_wait_time_offset = 0.2
        if len(self.lure_jump_shot_conf["l_hold_rod_time"].get())>0:
            self.fishing_config.lure_config.l_hold_rod_time = float(self.lure_jump_shot_conf["l_hold_rod_time"].get())
        else:
            self.fishing_config.lure_config.l_hold_rod_time = 3
        # 漂钓动作
        if len(self.lure_float_downstream_conf["l_float_downstream_rethrow_time"].get())>0:
            self.fishing_config.lure_config.l_float_downstream_rethrow_time = float(self.lure_float_downstream_conf["l_float_downstream_rethrow_time"].get())
        else:
            self.fishing_config.lure_config.l_float_downstream_rethrow_time = 60
        if len(self.lure_float_downstream_conf["l_float_downstream_rethrow_time_offset"].get())>0:
            self.fishing_config.lure_config.l_float_downstream_rethrow_time_offset = float(self.lure_float_downstream_conf["l_float_downstream_rethrow_time_offset"].get())
        else:
            self.fishing_config.lure_config.l_float_downstream_rethrow_time_offset = 2

        # 水底配置输入获取
        if len(self.water_bottom_conf["w_rod_num"].get())>0:
            self.fishing_config.water_bottom_config.w_rod_num = int(self.water_bottom_conf["w_rod_num"].get())
        else:
            self.fishing_config.water_bottom_config.w_rod_num = 1
        if len(self.water_bottom_conf["w_strength"].get())>0:
            self.fishing_config.water_bottom_config.w_strength = float(self.water_bottom_conf["w_strength"].get())
        else:
            self.fishing_config.water_bottom_config.w_strength = 0.8
        if len(self.water_bottom_conf["w_throw_offset"].get())>0:
            self.fishing_config.water_bottom_config.w_throw_offset = float(self.water_bottom_conf["w_throw_offset"].get())
        else:
            self.fishing_config.water_bottom_config.w_throw_offset = 0
        if len(self.water_bottom_conf["w_wait_line_fly"].get())>0:
            self.fishing_config.water_bottom_config.w_wait_line_fly = float(self.water_bottom_conf["w_wait_line_fly"].get())
        else:
            self.fishing_config.water_bottom_config.w_wait_line_fly = 1
        if len(self.water_bottom_conf["w_wait_line_fly_offset"].get())>0:
            self.fishing_config.water_bottom_config.w_wait_line_fly_offset = float(self.water_bottom_conf["w_wait_line_fly_offset"].get())
        else:
            self.fishing_config.water_bottom_config.w_wait_line_fly_offset = 1
        if len(self.water_bottom_conf["w_polling_time"].get())>0:
            self.fishing_config.water_bottom_config.w_polling_time = float(self.water_bottom_conf["w_polling_time"].get())
        else:
            self.fishing_config.water_bottom_config.w_polling_time = 100
        if len(self.water_bottom_conf["r_rethrow_time"].get())>0:
            self.fishing_config.water_bottom_config.r_rethrow_time = float(self.water_bottom_conf["r_rethrow_time"].get())
        else:
            self.fishing_config.water_bottom_config.r_rethrow_time = -1

        # 手竿配置输入获取
        if len(self.tenkara_conf["t_rod_num"].get())>0:
            self.fishing_config.tenkara_config.t_rod_num = int(self.tenkara_conf["t_rod_num"].get())
        else:
            self.fishing_config.tenkara_config.t_rod_num = 1
        if len(self.tenkara_conf["t_strength"].get())>0:
            self.fishing_config.tenkara_config.t_strength = float(self.tenkara_conf["t_strength"].get())
        else:
            self.fishing_config.tenkara_config.t_strength = 0.8
        if len(self.tenkara_conf["t_throw_offset"].get())>0:
            self.fishing_config.tenkara_config.t_throw_offset = float(self.tenkara_conf["t_throw_offset"].get())
        else:
            self.fishing_config.tenkara_config.t_throw_offset = 0
        if len(self.tenkara_conf["t_wait_time"].get())>0:
            self.fishing_config.tenkara_config.t_wait_time = float(self.tenkara_conf["t_wait_time"].get())
        else:
            self.fishing_config.tenkara_config.t_wait_time = 2
        if len(self.tenkara_conf["t_wait_time_offset"].get())>0:
            self.fishing_config.tenkara_config.t_wait_time_offset = float(self.tenkara_conf["t_wait_time_offset"].get())
        else:
            self.fishing_config.tenkara_config.t_wait_time_offset = 1
        if len(self.tenkara_conf["t_rethrow_time"].get())>0:
            self.fishing_config.tenkara_config.t_rethrow_time = float(self.tenkara_conf["t_rethrow_time"].get())
        else:
            self.fishing_config.tenkara_config.t_rethrow_time = -1

        # 基础配置输入获取
        if len(self.ui_sys_elements["check_interval_entry"].get())>0:
            myconfig.check_interval = float(self.ui_sys_elements["check_interval_entry"].get())
        else:
            myconfig.check_interval = 0.2
        if len(self.ui_sys_elements["thornback_random_entry"].get())>0:
            myconfig.thornback_random = float(self.ui_sys_elements["thornback_random_entry"].get())
        else:
            myconfig.thornback_random = 20.0
        if len(self.ui_sys_elements["eat_entry"].get())>0:
            myconfig.eat_interval = float(self.ui_sys_elements["eat_entry"].get())
        else:
            myconfig.eat_interval = 0.0
        if len(self.ui_sys_elements["drink_entry"].get())>0:
            myconfig.drink_interval = float(self.ui_sys_elements["drink_entry"].get())
        else:
            myconfig.drink_interval = 0.0

        self._switch_button_state(False)  # 禁用按钮
        # 开始钓鱼
        thread = threading.Thread(target=go_fishing, args=(self.fishing_config, self._switch_button_state))
        thread.setDaemon(True)
        thread.start()

    def _crafting_submit(self) -> None:
        crafting_total = 0
        if len(self.ui_sys_elements["crafting_entry"].get())>0:
            crafting_total = int(self.ui_sys_elements["crafting_entry"].get())
        else:
            crafting_total = 0
        
        self._switch_button_state(False)  # 禁用按钮
        # 开始制作
        thread = threading.Thread(target=go_crafting, args=(crafting_total, self._switch_button_state))
        thread.setDaemon(True)
        thread.start()
        

    def _switch_button_state(self, switch_state: bool) -> None:
        if switch_state:
            self.base_button["submit_button"].config(state=tk.NORMAL)  # 切换按钮状态
            self.ui_sys_elements["crafting_button"].config(state=tk.NORMAL)
        else:
            self.base_button["submit_button"].config(state=tk.DISABLED)  # 切换按钮状态
            self.ui_sys_elements["crafting_button"].config(state=tk.DISABLED)
