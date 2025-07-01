import config.config as config
import tkinter as tk
from typing import Literal
from window.variables import JumpShotType, Variables


class UiRodElements(Variables):
    def __init__(self):
        super().__init__()
        # 初始化界面元素
        self.rod_base = self.create_rod_base(self.rod_selection)
        self.lure_roll_type = self.create_window_lure_roll_type(self.roll_selection)
        self.water_bottom_model = self.create_window_water_bottom_model(self.water_bottom_selection)
        self.lure_conf = self.create_window_lure_conf()
        self.lure_jerk_bait_conf = self.create_window_lure_jerk_bait_conf()
        self.lure_jump_shot_conf = self.create_window_lure_jump_shot_conf(self.jump_shot_selection)
        self.lure_float_downstream_conf = self.create_window_lure_float_downstream_conf()
        self.water_bottom_conf = self.create_window_water_bottom_conf()
        self.tenkara_conf = self.create_window_tenkara_conf()
        # 初始化时更新标签
        self._update_rod_radios(self.rod_selection.get(), "rod_type")
        

    def hide_lure_normal(self):
        for element in self.lure_roll_type.values():
            if isinstance(element, tk.Widget):
                element.grid_remove()
        for element in self.lure_conf.values():
            element.grid_remove()
        self.lure_conf['l_rod_num_double'].grid_remove()

    def show_lure_normal(self):
        for element in self.lure_roll_type.values():
            element.grid()
        for element in self.lure_conf.values():
            element.grid()
        self.lure_conf['l_rod_num_double'].grid_remove()
        
    def hide_lure_jerk_bait(self):
        for element in self.lure_jerk_bait_conf.values():
            element.grid_remove()

    def show_lure_jerk_bait(self):
        for element in self.lure_jerk_bait_conf.values():
            element.grid()

    def show_lure_roll_jump_shot(self):
        self.lure_jump_shot_conf['lure_roll_line_time'].grid()
        self.lure_jump_shot_conf['l_roll_line_time'].grid()
        self.lure_jump_shot_conf['lure_roll_line_time_offset'].grid()
        self.lure_jump_shot_conf['l_roll_line_time_offset'].grid()
        self.lure_jump_shot_conf['lure_roll_line_wait_time'].grid()
        self.lure_jump_shot_conf['l_roll_line_wait_time'].grid()
        self.lure_jump_shot_conf['lure_roll_line_wait_time_offset'].grid()
        self.lure_jump_shot_conf['l_roll_line_wait_time_offset'].grid()

    def hide_lure_roll_jump_shot(self):
        self.lure_jump_shot_conf['lure_roll_line_time'].grid_remove()
        self.lure_jump_shot_conf['l_roll_line_time'].grid_remove()
        self.lure_jump_shot_conf['lure_roll_line_time_offset'].grid_remove()
        self.lure_jump_shot_conf['l_roll_line_time_offset'].grid_remove()
        self.lure_jump_shot_conf['lure_roll_line_wait_time'].grid_remove()
        self.lure_jump_shot_conf['l_roll_line_wait_time'].grid_remove()
        self.lure_jump_shot_conf['lure_roll_line_wait_time_offset'].grid_remove()
        self.lure_jump_shot_conf['l_roll_line_wait_time_offset'].grid_remove()

    def hide_lure_jump_shot(self):
        for element in self.lure_jump_shot_conf.values():
            element.grid_remove()

    def show_lure_jump_shot(self):
        for element in self.lure_jump_shot_conf.values():
            element.grid()
        self.lure_conf['l_rod_num'].grid_remove()
        self.lure_conf['l_rod_num_double'].grid()

    def hide_lure_float_downstream(self):
        for element in self.lure_float_downstream_conf.values():
            element.grid_remove()

    def show_lure_float_downstream(self):
        for element in self.lure_float_downstream_conf.values():
            element.grid()
        self.lure_conf["lure_wait_time"].grid_remove()
        self.lure_conf["l_wait_time"].grid_remove()
        self.lure_conf["lure_wait_time_offset"].grid_remove()
        self.lure_conf["l_wait_time_offset"].grid_remove()

    def hide_water_bottom(self):
        for element in self.water_bottom_model.values():
            element.grid_remove()
        for element in self.water_bottom_conf.values():
            element.grid_remove()

    def show_water_bottom(self,is_racing_rod=False):
        for element in self.water_bottom_model.values():
            element.grid()
        for element in self.water_bottom_conf.values():
            element.grid()
        if is_racing_rod:
            self.water_bottom_conf["racing_rethrow_time"].grid()
            self.water_bottom_conf["r_rethrow_time"].grid()
        else:
            self.water_bottom_conf["racing_rethrow_time"].grid_remove()
            self.water_bottom_conf["r_rethrow_time"].grid_remove()

    def hide_tenkara(self):
        for element in self.tenkara_conf.values():
            element.grid_remove()

    def show_tenkara(self):
        for element in self.tenkara_conf.values():
            element.grid()

    def show_selection_lure(self):
        if self.var_l_check_isfull.get() == 1:
            self.fishing_config.lure_config.l_check_isfull =  True
        else:
            self.fishing_config.lure_config.l_check_isfull = False
        if self.var_l_check_keep_all_fish.get() == 1:
            self.fishing_config.lure_config.l_check_keep_all_fish = True
        else:
            self.fishing_config.lure_config.l_check_keep_all_fish = False
        if self.var_l_check_fishon_whith_shift.get() == 1:
            self.fishing_config.lure_config.l_check_fishon_whith_shift = True
        else:
            self.fishing_config.lure_config.l_check_fishon_whith_shift = False
        if self.var_l_check_roll_last_line.get() == 1:
            self.fishing_config.lure_config.l_check_roll_last_line = True
        else:
            self.fishing_config.lure_config.l_check_roll_last_line = False
    

    def show_selection_water_bottom(self):
        if self.var_w_check_isfull.get() == 1:
            self.fishing_config.water_bottom_config.w_check_isfull = True
        else:
            self.fishing_config.water_bottom_config.w_check_isfull = False
        if self.var_w_check_keep_all_fish.get() == 1:
            self.fishing_config.water_bottom_config.w_check_keep_all_fish = True
        else:
            self.fishing_config.water_bottom_config.w_check_keep_all_fish = False
        if self.var_w_check_fishon_whith_shift.get() == 1:
            self.fishing_config.water_bottom_config.w_check_fishon_whith_shift = True
        else:
            self.fishing_config.water_bottom_config.w_check_fishon_whith_shift = False

    def show_selection_tenkara(self):
        if self.var_t_check_isfull.get() == 1:
            self.fishing_config.tenkara_config.t_check_isfull = True
        else:
            self.fishing_config.tenkara_config.t_check_isfull = False
        if self.var_t_check_keep_all_fish.get() == 1:
            self.fishing_config.tenkara_config.t_check_keep_all_fish = True
        else:
            self.fishing_config.tenkara_config.t_check_keep_all_fish = False
        if self.var_t_check_fishon_whith_shift.get() == 1:
            self.fishing_config.tenkara_config.t_check_fishon_whith_shift = True
        else:
            self.fishing_config.tenkara_config.t_check_fishon_whith_shift = False
        if self.var_t_check_racing_rod.get() == 1:
            self.fishing_config.tenkara_config.t_check_racing_rod = True
        else:
            self.fishing_config.tenkara_config.t_check_racing_rod = False
    
    def _update_rod_radios(self,selection, group):
        if group == "rod_type":
            if selection == "lure":
                self.hide_water_bottom()
                self.hide_lure_jerk_bait()
                self.hide_lure_jump_shot()
                self.hide_lure_float_downstream()
                self.hide_tenkara()
                self.show_lure_normal()
                if self.fishing_config.lure_config.roll_type == "dog_walk":
                    self.show_lure_jerk_bait()
                elif self.fishing_config.lure_config.roll_type == "jump_shot":
                    self.show_lure_jump_shot()
                elif self.fishing_config.lure_config.roll_type == "float_downstream":
                    self.show_lure_float_downstream()
                self.fishing_config.rod_type = "lure"
            elif selection == "water_bottom":
                self.hide_lure_normal()  
                self.hide_lure_jerk_bait()
                self.hide_lure_jump_shot()
                self.hide_lure_float_downstream()  
                self.hide_tenkara()
                self.show_water_bottom()  
                self.fishing_config.rod_type = "water_bottom"
            elif selection == "racing_rod":
                self.hide_lure_normal()  
                self.hide_lure_jerk_bait()
                self.hide_lure_jump_shot()
                self.hide_lure_float_downstream()  
                self.hide_tenkara()
                self.show_water_bottom(True)  
                self.fishing_config.rod_type = "racing_rod"
            elif selection == "tenkara_rod":
                self.hide_lure_normal()  
                self.hide_lure_jerk_bait()
                self.hide_lure_jump_shot()
                self.hide_lure_float_downstream()  
                self.hide_water_bottom()
                self.show_tenkara()
                self.fishing_config.rod_type = "tenkara_rod"
        elif group == "roll_type":
            if selection == "constant_roll":
                self.hide_lure_jerk_bait()
                self.hide_lure_jump_shot()
                self.hide_lure_float_downstream()  
                self.show_lure_normal()
                self.fishing_config.lure_config.roll_type = "constant_roll"
            elif selection == "dog_walk":
                self.hide_lure_jump_shot()
                self.hide_lure_float_downstream()
                self.show_lure_normal()  
                self.show_lure_jerk_bait()
                self.fishing_config.lure_config.roll_type = "dog_walk"
            elif selection == "jump_shot":
                self.hide_lure_jerk_bait()  
                self.hide_lure_float_downstream()
                self.show_lure_normal()  
                self.show_lure_jump_shot()
                self.fishing_config.lure_config.roll_type = "jump_shot"
            elif selection == "float_downstream":
                self.hide_lure_jerk_bait()
                self.hide_lure_jump_shot()
                self.show_lure_float_downstream()
                self.fishing_config.lure_config.roll_type = "float_downstream"
        elif group == "water_bottom_model":
            if selection == "automatic":
                self.fishing_config.water_bottom_config.water_bottom_model = "automatic"
            elif selection == "monitor":
                self.fishing_config.water_bottom_config.water_bottom_model = "monitor"
        elif group == "jump_shot_model":
            if selection == 0:
                self.show_lure_roll_jump_shot()
                self.fishing_config.lure_config.l_jump_shot_type = JumpShotType.ROLL_RELEASE
            elif selection == 1:
                self.hide_lure_roll_jump_shot()
                self.fishing_config.lure_config.l_jump_shot_type = JumpShotType.RAISE_ROD
            elif selection == 2:
                self.hide_lure_roll_jump_shot()
                self.fishing_config.lure_config.l_jump_shot_type = JumpShotType.FORCE


    
    
    def _vcmd(self)  -> tuple[str, Literal['%P']]:
        # 使用 validate 命令限制输入
        return (self.register(self._validate_input), '%P')  # '%P' 是输入框当前内容的字符串表示形式

    def _validate_input(self,P) -> bool:
        # 验证输入，仅接受数字、负号和小数点
        if P == "":  # 允许空输入
            return True
        if P.count('-') > 1:  # 只允许一个负号
            return False
        if P.count('.') > 1:  # 只允许一个小数点
            return False
        if P[0] == '-':
            # 如果第一个字符是负号，后续必须是数字
            return P[1:].isdigit()  # 负号后必须是数字
        return P.isdigit() or (P.count('.') == 1 and P.replace('.', '').isdigit())
    
    def _vcmd_rod_num(self)  -> tuple[str, Literal['%P']]:
        # 使用 validate 命令限制输入
        return (self.register(self._validate_rod_num), '%P') 
    
    def _validate_rod_num(self,P) -> bool:
        if P == "" or P in {'1','2','3'}:
            return True
        else:
            return False
        
    def _vcmd_single_rod(self)  -> tuple[str, Literal['%P']]:
        # 使用 validate 命令限制输入
        return (self.register(self._validate_single_rod), '%P') 
    
    def _validate_single_rod(self,P) -> bool:
        if P in {'1'}:
            return True
        elif P == "":
            return True
        else:
            return False
        
    def _vcmd_double_rod(self)  -> tuple[str, Literal['%P']]:
        # 使用 validate 命令限制输入
        return (self.register(self._validate_double_rod), '%P') 
    
    def _validate_double_rod(self,P) -> bool:
        if P in {'1','2'}:
            return True
        elif P == "":
            return True
        else:
            return False
    
    def create_rod_base(self,rod_selection) -> dict[str,any]:

        choose_lure = tk.Radiobutton(self, text="路亚竿", variable=rod_selection, value="lure",
                                command=lambda: self._update_rod_radios(rod_selection.get(), "rod_type"))
        choose_lure.grid(row=2, column=0, padx=10, pady=5)

        choose_water_bottom = tk.Radiobutton(self, text="水底钓具", variable=rod_selection, value="water_bottom",
                                command=lambda: self._update_rod_radios(rod_selection.get(), "rod_type"))
        choose_water_bottom.grid(row=2, column=1, padx=10, pady=5)

        choose_racing_rod = tk.Radiobutton(self, text="赛竿/博格尼亚", variable=rod_selection, value="racing_rod",
                                command=lambda: self._update_rod_radios(rod_selection.get(), "rod_type"))
        choose_racing_rod.grid(row=2, column=2, padx=10, pady=5)

        choose_tenkara_rod = tk.Radiobutton(self, text="手竿", variable=rod_selection, value="tenkara_rod",
                                command=lambda: self._update_rod_radios(rod_selection.get(), "rod_type"))
        choose_tenkara_rod.grid(row=2, column=3, padx=10, pady=5)
        return {
            "choose_lure": choose_lure,
            "choose_water_bottom": choose_water_bottom,
            "choose_racing_rod": choose_racing_rod,
            "choose_tenkara_rod": choose_tenkara_rod
        }
    
    def create_window_lure_roll_type(self,roll_selection) ->dict[str,any]:
        # 收线方式类型的单选框
        roll_choose = tk.Label(self, text="收线方式: ")
        roll_choose.grid(row=3, column=0, padx=10, pady=5)

        choose_constant_roll = tk.Radiobutton(self, text="匀收", variable=roll_selection, value="constant_roll",
                                command=lambda: self._update_rod_radios(roll_selection.get(), "roll_type"))
        choose_constant_roll.grid(row=4, column=0, padx=10, pady=5)

        choose_dog_walk = tk.Radiobutton(self, text="抽停", variable=roll_selection, value="dog_walk",
                                command=lambda: self._update_rod_radios(roll_selection.get(), "roll_type"))
        choose_dog_walk.grid(row=4, column=1, padx=10, pady=5)

        choose_jump_shot = tk.Radiobutton(self, text="跳底", variable=roll_selection, value="jump_shot",
                                command=lambda: self._update_rod_radios(roll_selection.get(), "roll_type"))
        choose_jump_shot.grid(row=4, column=2, padx=10, pady=5)

        choose_float_downstream = tk.Radiobutton(self, text="顺水漂流", variable=roll_selection, value="float_downstream",
                                command=lambda: self._update_rod_radios(roll_selection.get(), "roll_type"))
        choose_float_downstream.grid(row=4, column=3, padx=10, pady=5)
        return {
            "roll_choose": roll_choose,
            "choose_constant_roll": choose_constant_roll,
            "choose_dog_walk": choose_dog_walk,
            "choose_jump_shot": choose_jump_shot,
            "choose_float_downstream": choose_float_downstream
        }
    
    def create_window_water_bottom_model(self,water_bottom_selection) ->dict[str,any]:
        # 路亚钓具模式单选框
        water_bottom_choose = tk.Label(self, text="所有钓具状态:")
        water_bottom_choose.grid(row=5, column=0, padx=10, pady=5)

        choose_automatic = tk.Radiobutton(self, text="未抛投", variable=water_bottom_selection, value="automatic",
                                command=lambda: self._update_rod_radios(water_bottom_selection.get(), "water_bottom_model"))
        choose_automatic.grid(row=6, column=0, padx=10, pady=5)

        choose_monitor = tk.Radiobutton(self, text="已抛投", variable=water_bottom_selection, value="monitor",
                                command=lambda: self._update_rod_radios(water_bottom_selection.get(), "water_bottom_model"))
        choose_monitor.grid(row=6, column=1, padx=10, pady=5)
        return {
            "water_bottom_choose": water_bottom_choose,
            "choose_automatic": choose_automatic,
            "choose_monitor": choose_monitor
        }

    ########################## 路亚配置开始###################
    def create_window_lure_conf(self) ->dict[str, any]:
        lure_conf_label = tk.Label(self, text="作钓配置:")
        lure_conf_label.grid(row=7, column=0, padx=10, pady=5)

        lure_rod_num = tk.Label(self, text="鱼竿数量:")
        lure_rod_num.grid(row=8, column=0, padx=10, pady=5)
        l_rod_num = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd_single_rod())
        l_rod_num.insert(0, '1')
        l_rod_num.grid(row=8, column=1, padx=10, pady=5)

        # 跳底允许双杆
        l_rod_num_double = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd_double_rod())
        l_rod_num_double.insert(0, '1')
        l_rod_num_double.grid(row=8, column=1, padx=10, pady=5)

        lure_strength = tk.Label(self, text="抛投力度(秒):")
        lure_strength.grid(row=8, column=2, padx=10, pady=5)
        l_strength = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_strength.insert(0, '0.8')
        l_strength.grid(row=8, column=3, padx=10, pady=5)

        lure_throw_offset = tk.Label(self, text="力度偏移量(秒):")
        lure_throw_offset.grid(row=9, column=0, padx=10, pady=5)
        l_throw_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_throw_offset.insert(0, '0')
        l_throw_offset.grid(row=9, column=1, padx=10, pady=5)

        lure_wait_time = tk.Label(self, text="等待拟饵到位(秒):")
        lure_wait_time.grid(row=9, column=2, padx=10, pady=5)
        l_wait_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_wait_time.insert(0, '2')
        l_wait_time.grid(row=9, column=3, padx=10, pady=5)

        lure_wait_time_offset = tk.Label(self, text="拟饵到位偏移量(秒):")
        lure_wait_time_offset.grid(row=10, column=0, padx=10, pady=5)
        l_wait_time_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_wait_time_offset.insert(0, '1')
        l_wait_time_offset.grid(row=10, column=1, padx=10, pady=5)

        # 创建复选框
        l_check_isfull = tk.Checkbutton(self, text="满力抛投", variable=self.var_l_check_isfull, command=self.show_selection_lure)
        l_check_isfull.grid(row=11, column=0, padx=10, pady=5)

        l_check_keep_all_fish = tk.Checkbutton(self, text="保留所有渔获", variable=self.var_l_check_keep_all_fish, command=self.show_selection_lure)
        l_check_keep_all_fish.grid(row=11, column=1, padx=10, pady=5)

        l_check_fishon_whith_shift = tk.Checkbutton(self, text="中鱼加速收线", variable=self.var_l_check_fishon_whith_shift, command=self.show_selection_lure)
        l_check_fishon_whith_shift.grid(row=11, column=2, padx=10, pady=5)
        return {
            "lure_conf_label" : lure_conf_label,
            "lure_rod_num" : lure_rod_num,
            "l_rod_num" : l_rod_num,
            "l_rod_num_double" : l_rod_num_double,
            "lure_strength" : lure_strength,
            "l_strength" : l_strength,
            "lure_throw_offset" : lure_throw_offset,
            "l_throw_offset" : l_throw_offset,
            "lure_wait_time" : lure_wait_time,
            "l_wait_time" : l_wait_time,
            "lure_wait_time_offset" : lure_wait_time_offset,
            "l_wait_time_offset" : l_wait_time_offset,
            "l_check_isfull" : l_check_isfull,
            "l_check_keep_all_fish" : l_check_keep_all_fish,
            "l_check_fishon_whith_shift" : l_check_fishon_whith_shift
        }

    def create_window_lure_jerk_bait_conf(self) -> dict[str, any]:
        # 抽停配置
        lure_jerk_bait_conf = tk.Label(self, text="抽停配置:")
        lure_jerk_bait_conf.grid(row=12, column=0, padx=10, pady=5)

        l_check_roll_last_line = tk.Checkbutton(self, text="快速收起余线", variable=self.var_l_check_roll_last_line, command=self.show_selection_lure)
        l_check_roll_last_line.grid(row=13, column=0, padx=10, pady=5)

        lure_dog_walk_time = tk.Label(self, text="抽停时长(秒):")
        lure_dog_walk_time.grid(row=14, column=0, padx=10, pady=5)
        l_dog_walk_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_dog_walk_time.insert(0, '0.3')
        l_dog_walk_time.grid(row=14, column=1, padx=10, pady=5)

        lure_dog_walk_time_offset = tk.Label(self, text="抽停偏移量(秒):")
        lure_dog_walk_time_offset.grid(row=14, column=2, padx=10, pady=5)
        l_dog_walk_time_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_dog_walk_time_offset.insert(0, '0.2')
        l_dog_walk_time_offset.grid(row=14, column=3, padx=10, pady=5)

        lure_dog_walk_wait_time = tk.Label(self, text="抽停间隔(秒):")
        lure_dog_walk_wait_time.grid(row=15, column=0, padx=10, pady=5)
        l_dog_walk_wait_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_dog_walk_wait_time.insert(0, '0.3')
        l_dog_walk_wait_time.grid(row=15, column=1, padx=10, pady=5)

        lure_dog_walk_wait_time_offset = tk.Label(self, text="间隔偏移量(秒):")
        lure_dog_walk_wait_time_offset.grid(row=15, column=2, padx=10, pady=5)
        l_dog_walk_wait_time_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_dog_walk_wait_time_offset.insert(0, '0.2')
        l_dog_walk_wait_time_offset.grid(row=15, column=3, padx=10, pady=5)
        return {
            "lure_jerk_bait_conf" : lure_jerk_bait_conf,
            "l_check_roll_last_line" : l_check_roll_last_line,
            "lure_dog_walk_time" : lure_dog_walk_time,
            "l_dog_walk_time" : l_dog_walk_time,
            "lure_dog_walk_time_offset" : lure_dog_walk_time_offset,
            "l_dog_walk_time_offset" : l_dog_walk_time_offset,
            "lure_dog_walk_wait_time" : lure_dog_walk_wait_time,
            "l_dog_walk_wait_time" : l_dog_walk_wait_time,
            "lure_dog_walk_wait_time_offset" : lure_dog_walk_wait_time_offset,
            "l_dog_walk_wait_time_offset" : l_dog_walk_wait_time_offset
        }
    
    def update_rod_base_text(self):
        if config.ui_language:
            # create_rod_base
            self.rod_base["choose_lure"].config(text="Spin Fishinng")
            self.rod_base["choose_water_bottom"].config(text="Bottom Fishinng")
            self.rod_base["choose_racing_rod"].config(text="Match/Bolognese")
            self.rod_base["choose_tenkara_rod"].config(text="Tenkara Fishinng")

            # create_window_lure_roll_type
            self.lure_roll_type["roll_choose"].config(text="Roll Type:")
            self.lure_roll_type["choose_constant_roll"].config(text="Constant Roll")
            self.lure_roll_type["choose_dog_walk"].config(text="Roll With Wait")
            self.lure_roll_type["choose_jump_shot"].config(text="Jump Roll")
            self.lure_roll_type["choose_float_downstream"].config(text="Throw And Wait")

            # create_window_water_bottom_model
            self.water_bottom_model["water_bottom_choose"].config(text="Rods Status:")
            self.water_bottom_model["choose_automatic"].config(text="Wait Throw")
            self.water_bottom_model["choose_monitor"].config(text="Throwed")

            # create_window_lure_conf
            self.lure_conf["lure_conf_label"].config(text="Spin Config:")
            self.lure_conf["lure_rod_num"].config(text="Rods Num:")
            self.lure_conf["lure_strength"].config(text="Throw Strength(s):")
            self.lure_conf["lure_throw_offset"].config(text="Throw Offset(s):")
            self.lure_conf["lure_wait_time"].config(text="Wait Lures In Place(s):")
            self.lure_conf["lure_wait_time_offset"].config(text="Wait Offset(s):")
            self.lure_conf["l_check_isfull"].config(text="Full Throw")
            self.lure_conf["l_check_keep_all_fish"].config(text="Keep All Fish")
            self.lure_conf["l_check_fishon_whith_shift"].config(text="Shift Roll On Fish")

            # create_window_lure_jerk_bait_conf
            self.lure_jerk_bait_conf["lure_jerk_bait_conf"].config(text="Roll Wait Config:")
            self.lure_jerk_bait_conf["l_check_roll_last_line"].config(text="Fast Roll Last Line:")
            self.lure_jerk_bait_conf["lure_dog_walk_time"].config(text="Roll Time(s):")
            self.lure_jerk_bait_conf["lure_dog_walk_time_offset"].config(text="Roll Time Offset(s):")
            self.lure_jerk_bait_conf["lure_dog_walk_wait_time"].config(text="Wait Time(s):")
            self.lure_jerk_bait_conf["lure_dog_walk_wait_time_offset"].config(text="Wait Time Offset(s):")

            # lure_jump_shot_conf
            self.lure_jump_shot_conf["lure_hold_rod_time"].config(text="Hold Rod Time(s):")
            self.lure_jump_shot_conf["lure_jump_shot_conf"].config(text="Jump Shot Conf:")
            self.lure_jump_shot_conf["l_coose_roll_release_jump_shot"].config(text="Roll line")
            self.lure_jump_shot_conf["l_coose_raise_rod_jump_shot"].config(text="Press RMB")
            self.lure_jump_shot_conf["l_coose_force_jump_shot"].config(text="Press Ctrl+RMB")
            self.lure_jump_shot_conf["lure_roll_line_time"].config(text="Roll Time(s):")
            self.lure_jump_shot_conf["lure_roll_line_time_offset"].config(text="Roll Time Offset(s):")
            self.lure_jump_shot_conf["lure_roll_line_wait_time"].config(text="Wait Time(s):")
            self.lure_jump_shot_conf["lure_roll_line_wait_time_offset"].config(text="Wait Time Offset(s):")

            # lure_float_downstream_conf
            self.lure_float_downstream_conf["lure_float_downstream_conf"].config(text="Float Downstream Conf:")
            self.lure_float_downstream_conf["lure_float_downstream_rethrow_time"].config(text="Rethrow Time(s):")
            self.lure_float_downstream_conf["lure_float_downstream_rethrow_time_offset"].config(text="Rethrow Time Offset(s):")

            # water_bottom_conf
            self.water_bottom_conf["water_bottom_conf_label"].config(text="Bottom Config:")
            self.water_bottom_conf["water_bottom_rod_num"].config(text="Rods Num:")
            self.water_bottom_conf["water_bottom_strength"].config(text="Throw Strength(s):")
            self.water_bottom_conf["water_bottom_throw_offset"].config(text="Throw Offset(s):")
            self.water_bottom_conf["water_bottom_wait_line_fly"].config(text="Wait Line Fly(s):")
            self.water_bottom_conf["water_bottom_wait_line_fly_offset"].config(text="Wait Line Fly Offset(s):")
            self.water_bottom_conf["water_bottom_polling_time"].config(text="Polling Rods Time(s):")
            self.water_bottom_conf["racing_rethrow_time"].config(text="Rethrow Time(s):")
            self.water_bottom_conf["w_check_isfull"].config(text="Full Throw:")
            self.water_bottom_conf["w_check_keep_all_fish"].config(text="Keep All Fish:")
            self.water_bottom_conf["w_check_fishon_whith_shift"].config(text="Shift Roll On Fish:")

            # tenkara_conf
            self.tenkara_conf["tenkara_conf_label"].config(text="Tenkara Conf:")
            self.tenkara_conf["tenkara_rod_num"].config(text="Rods Num:")
            self.tenkara_conf["tenkara_strength"].config(text="Throw Strength(s):")
            self.tenkara_conf["tenkara_throw_offset"].config(text="Throw Offset(s):")
            self.tenkara_conf["tenkara_wait_time"].config(text="Wait Float Appear(s):")
            self.tenkara_conf["tenkara_wait_time_offset"].config(text="Wait Float Offset(s):")
            self.tenkara_conf["tenkara_rethrow_time"].config(text="Rethrow Time(s):")
            self.tenkara_conf["t_check_isfull"].config(text="Full Throw")
            self.tenkara_conf["t_check_keep_all_fish"].config(text="Keep All Fish")
            self.tenkara_conf["t_check_fishon_whith_shift"].config(text="Shift Roll On Fish")
            self.tenkara_conf["t_check_racing_rod"].config(text="Match/Bolognese")
        else:
            self.rod_base["choose_lure"].config(text="路亚竿")
            self.rod_base["choose_water_bottom"].config(text="水底钓具")
            self.rod_base["choose_racing_rod"].config(text="赛竿/博格尼亚")
            self.rod_base["choose_tenkara_rod"].config(text="手竿")

            self.lure_roll_type["roll_choose"].config(text="收线方式:")
            self.lure_roll_type["choose_constant_roll"].config(text="匀收")
            self.lure_roll_type["choose_dog_walk"].config(text="抽停")
            self.lure_roll_type["choose_jump_shot"].config(text="跳底")
            self.lure_roll_type["choose_float_downstream"].config(text="顺水漂流")

            self.water_bottom_model["water_bottom_choose"].config(text="所有钓具状态:")
            self.water_bottom_model["choose_automatic"].config(text="未抛投")
            self.water_bottom_model["choose_monitor"].config(text="已抛投")

            self.lure_conf["lure_conf_label"].config(text="作钓配置:")
            self.lure_conf["lure_rod_num"].config(text="鱼竿数量:")
            self.lure_conf["lure_strength"].config(text="抛投力度(秒):")
            self.lure_conf["lure_throw_offset"].config(text="力度偏移量(秒):")
            self.lure_conf["lure_wait_time"].config(text="等待拟饵到位(秒):")
            self.lure_conf["lure_wait_time_offset"].config(text="拟饵到位偏移量(秒):")
            self.lure_conf["l_check_isfull"].config(text="满力抛投")
            self.lure_conf["l_check_keep_all_fish"].config(text="保留所有渔获")
            self.lure_conf["l_check_fishon_whith_shift"].config(text="中鱼加速收线")

            self.lure_jerk_bait_conf["lure_jerk_bait_conf"].config(text="抽停配置:")
            self.lure_jerk_bait_conf["l_check_roll_last_line"].config(text="快速收起余线")
            self.lure_jerk_bait_conf["lure_dog_walk_time"].config(text="抽停时长(秒):")
            self.lure_jerk_bait_conf["lure_dog_walk_time_offset"].config(text="抽停偏移量(秒):")
            self.lure_jerk_bait_conf["lure_dog_walk_wait_time"].config(text="抽停间隔(秒):")
            self.lure_jerk_bait_conf["lure_dog_walk_wait_time_offset"].config(text="间隔偏移量(秒):")

            self.lure_jump_shot_conf["lure_hold_rod_time"].config(text="持竿时长(秒):")
            self.lure_jump_shot_conf["lure_jump_shot_conf"].config(text="跳底配置:")
            self.lure_jump_shot_conf["l_coose_roll_release_jump_shot"].config(text="收线跳底")
            self.lure_jump_shot_conf["l_coose_raise_rod_jump_shot"].config(text="抬竿跳底")
            self.lure_jump_shot_conf["l_coose_force_jump_shot"].config(text="抽竿跳底")
            self.lure_jump_shot_conf["lure_roll_line_time"].config(text="收线时长(秒):")
            self.lure_jump_shot_conf["lure_roll_line_time_offset"].config(text="收线偏移量(秒):")
            self.lure_jump_shot_conf["lure_roll_line_wait_time"].config(text="收线间隔(秒):")
            self.lure_jump_shot_conf["lure_roll_line_wait_time_offset"].config(text="间隔偏移量(秒):")

            self.lure_float_downstream_conf["lure_float_downstream_conf"].config(text="顺水漂流配置:")
            self.lure_float_downstream_conf["lure_float_downstream_rethrow_time"].config(text="重新抛投间隔(秒):")
            self.lure_float_downstream_conf["lure_float_downstream_rethrow_time_offset"].config(text="间隔偏移量(秒):")

            self.water_bottom_conf["water_bottom_conf_label"].config(text="作钓配置:")
            self.water_bottom_conf["water_bottom_rod_num"].config(text="鱼竿数量:")
            self.water_bottom_conf["water_bottom_strength"].config(text="抛投力度(秒):")
            self.water_bottom_conf["water_bottom_throw_offset"].config(text="力度偏移量(秒):")
            self.water_bottom_conf["water_bottom_wait_line_fly"].config(text="等待钩饵入水(秒):")
            self.water_bottom_conf["water_bottom_wait_line_fly_offset"].config(text="钩饵入水偏移量(秒):")
            self.water_bottom_conf["water_bottom_polling_time"].config(text="监控间隔(秒):")
            self.water_bottom_conf["racing_rethrow_time"].config(text="重新抛投间隔(秒):")
            self.water_bottom_conf["w_check_isfull"].config(text="满力抛投")
            self.water_bottom_conf["w_check_keep_all_fish"].config(text="保留所有渔获")
            self.water_bottom_conf["w_check_fishon_whith_shift"].config(text="中鱼加速收线")

            self.tenkara_conf["tenkara_conf_label"].config(text="作钓配置:")
            self.tenkara_conf["tenkara_rod_num"].config(text="鱼竿数量:")
            self.tenkara_conf["tenkara_strength"].config(text="抛投力度(秒):")
            self.tenkara_conf["tenkara_throw_offset"].config(text="力度偏移量(秒):")
            self.tenkara_conf["tenkara_wait_time"].config(text="等待浮标立直(秒):")
            self.tenkara_conf["tenkara_wait_time_offset"].config(text="浮标入水偏移量(秒):")
            self.tenkara_conf["tenkara_rethrow_time"].config(text="重新抛投间隔(秒):")
            self.tenkara_conf["t_check_isfull"].config(text="满力抛投")
            self.tenkara_conf["t_check_keep_all_fish"].config(text="保留所有渔获")
            self.tenkara_conf["t_check_fishon_whith_shift"].config(text="中鱼加速收线")
            self.tenkara_conf["t_check_racing_rod"].config(text="赛竿/伯格尼亚")
    
    def create_window_lure_jump_shot_conf(self,jump_shot_selection) -> dict[str, any]:
        # 跳底配置
        lure_hold_rod_time = tk.Label(self, text="持竿时长(秒):")
        lure_hold_rod_time.grid(row=10, column=2, padx=10, pady=5)
        l_hold_rod_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_hold_rod_time.insert(0, '3')
        l_hold_rod_time.grid(row=10, column=3, padx=10, pady=5)
    
        lure_jump_shot_conf = tk.Label(self, text="跳底配置:")
        lure_jump_shot_conf.grid(row=12, column=0, padx=10, pady=5)

        l_coose_roll_release_jump_shot = tk.Radiobutton(self, text="收线跳底", variable=self.jump_shot_selection, value=JumpShotType.ROLL_RELEASE.value,
                                command=lambda: self._update_rod_radios(jump_shot_selection.get(), "jump_shot_model"))
        l_coose_roll_release_jump_shot.grid(row=13, column=0, padx=10, pady=5)

        l_coose_raise_rod_jump_shot = tk.Radiobutton(self, text="抬竿跳底", variable=self.jump_shot_selection, value=JumpShotType.RAISE_ROD.value,
                                command=lambda: self._update_rod_radios(jump_shot_selection.get(), "jump_shot_model"))
        l_coose_raise_rod_jump_shot.grid(row=13, column=1, padx=10, pady=5)

        l_coose_force_jump_shot = tk.Radiobutton(self, text="抽竿跳底", variable=self.jump_shot_selection, value=JumpShotType.FORCE.value,
                                command=lambda: self._update_rod_radios(jump_shot_selection.get(), "jump_shot_model"))
        l_coose_force_jump_shot.grid(row=13, column=2, padx=10, pady=5)

        lure_roll_line_time = tk.Label(self, text="收线时长(秒):")
        lure_roll_line_time.grid(row=14, column=0, padx=10, pady=5)
        l_roll_line_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_roll_line_time.insert(0, '1')
        l_roll_line_time.grid(row=14, column=1, padx=10, pady=5)

        lure_roll_line_time_offset = tk.Label(self, text="收线偏移量(秒):")
        lure_roll_line_time_offset.grid(row=14, column=2, padx=10, pady=5)
        l_roll_line_time_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_roll_line_time_offset.insert(0, '0.2')
        l_roll_line_time_offset.grid(row=14, column=3, padx=10, pady=5)

        lure_roll_line_wait_time = tk.Label(self, text="收线间隔(秒):")
        lure_roll_line_wait_time.grid(row=15, column=0, padx=10, pady=5)
        l_roll_line_wait_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_roll_line_wait_time.insert(0, '9')
        l_roll_line_wait_time.grid(row=15, column=1, padx=10, pady=5)

        lure_roll_line_wait_time_offset = tk.Label(self, text="间隔偏移量(秒):")
        lure_roll_line_wait_time_offset.grid(row=15, column=2, padx=10, pady=5)
        l_roll_line_wait_time_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_roll_line_wait_time_offset.insert(0, '0.2')
        l_roll_line_wait_time_offset.grid(row=15, column=3, padx=10, pady=5)
        return{
            "lure_hold_rod_time" : lure_hold_rod_time,
            "l_hold_rod_time" : l_hold_rod_time,
            "lure_jump_shot_conf" : lure_jump_shot_conf,
            "l_coose_roll_release_jump_shot" : l_coose_roll_release_jump_shot,
            "l_coose_raise_rod_jump_shot" : l_coose_raise_rod_jump_shot,
            "l_coose_force_jump_shot" : l_coose_force_jump_shot,
            "lure_roll_line_time" : lure_roll_line_time,
            "l_roll_line_time" : l_roll_line_time,
            "lure_roll_line_time_offset" : lure_roll_line_time_offset,
            "l_roll_line_time_offset" : l_roll_line_time_offset,
            "lure_roll_line_wait_time" : lure_roll_line_wait_time,
            "l_roll_line_wait_time" : l_roll_line_wait_time,
            "lure_roll_line_wait_time_offset" : lure_roll_line_wait_time_offset,
            "l_roll_line_wait_time_offset" : l_roll_line_wait_time_offset
        }
    
    def create_window_lure_float_downstream_conf(self) -> dict[str, any]:
        # 顺水漂流配置
        lure_float_downstream_conf = tk.Label(self, text="顺水漂流配置:")
        lure_float_downstream_conf.grid(row=12, column=0, padx=10, pady=5)

        lure_float_downstream_rethrow_time = tk.Label(self, text="重新抛投间隔(秒):")
        lure_float_downstream_rethrow_time.grid(row=13, column=0, padx=10, pady=5)
        l_float_downstream_rethrow_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_float_downstream_rethrow_time.insert(0, '60')
        l_float_downstream_rethrow_time.grid(row=13, column=1, padx=10, pady=5)

        lure_float_downstream_rethrow_time_offset = tk.Label(self, text="间隔偏移量(秒):")
        lure_float_downstream_rethrow_time_offset.grid(row=13, column=2, padx=10, pady=5)
        l_float_downstream_rethrow_time_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        l_float_downstream_rethrow_time_offset.insert(0, '2')
        l_float_downstream_rethrow_time_offset.grid(row=13, column=3, padx=10, pady=5)
        return{
            "lure_float_downstream_conf" : lure_float_downstream_conf,
            "lure_float_downstream_rethrow_time" : lure_float_downstream_rethrow_time,
            "l_float_downstream_rethrow_time" : l_float_downstream_rethrow_time,
            "lure_float_downstream_rethrow_time_offset" : lure_float_downstream_rethrow_time_offset,
            "l_float_downstream_rethrow_time_offset" : l_float_downstream_rethrow_time_offset
        }



    ########################## 路亚配置结束###################

    ########################## 水底/赛竿/博格尼亚配置开始###################
    def create_window_water_bottom_conf(self) -> dict[str, any]:
        water_bottom_conf_label = tk.Label(self, text="作钓配置:")
        water_bottom_conf_label.grid(row=7, column=0, padx=10, pady=5)

        water_bottom_rod_num = tk.Label(self, text="鱼竿数量:")
        water_bottom_rod_num.grid(row=8, column=0, padx=10, pady=5)
        w_rod_num = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd_rod_num())
        w_rod_num.insert(0, '1')
        w_rod_num.grid(row=8, column=1, padx=10, pady=5)

        water_bottom_strength = tk.Label(self, text="抛投力度(秒):")
        water_bottom_strength.grid(row=8, column=2, padx=10, pady=5)
        w_strength = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        w_strength.insert(0, '0.8')
        w_strength.grid(row=8, column=3, padx=10, pady=5)

        water_bottom_throw_offset = tk.Label(self, text="力度偏移量(秒):")
        water_bottom_throw_offset.grid(row=9, column=0, padx=10, pady=5)
        w_throw_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        w_throw_offset.insert(0, '0')
        w_throw_offset.grid(row=9, column=1, padx=10, pady=5)

        water_bottom_wait_line_fly = tk.Label(self, text="等待钩饵入水(秒):")
        water_bottom_wait_line_fly.grid(row=9, column=2, padx=10, pady=5)
        w_wait_line_fly = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        w_wait_line_fly.insert(0, '1')
        w_wait_line_fly.grid(row=9, column=3, padx=10, pady=5)

        water_bottom_wait_line_fly_offset = tk.Label(self, text="钩饵入水偏移量(秒):")
        water_bottom_wait_line_fly_offset.grid(row=10, column=0, padx=10, pady=5)
        w_wait_line_fly_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        w_wait_line_fly_offset.insert(0, '1')
        w_wait_line_fly_offset.grid(row=10, column=1, padx=10, pady=5)

        water_bottom_polling_time = tk.Label(self, text="监控间隔(秒)")
        water_bottom_polling_time.grid(row=10, column=2, padx=10, pady=5)
        w_polling_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        w_polling_time.insert(0, '100')
        w_polling_time.grid(row=10, column=3, padx=10, pady=5)

        racing_rethrow_time = tk.Label(self, text="重新抛投间隔(秒):")
        racing_rethrow_time.grid(row=11, column=0, padx=10, pady=5)
        r_rethrow_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        r_rethrow_time.insert(0, '-1')
        r_rethrow_time.grid(row=11, column=1, padx=10, pady=5)

        # 创建复选框
        w_check_isfull = tk.Checkbutton(self, text="满力抛投", variable=self.var_w_check_isfull, command=self.show_selection_water_bottom)
        w_check_isfull.grid(row=12, column=0, padx=10, pady=5)

        w_check_keep_all_fish = tk.Checkbutton(self, text="保留所有渔获", variable=self.var_w_check_keep_all_fish, command=self.show_selection_water_bottom)
        w_check_keep_all_fish.grid(row=12, column=1, padx=10, pady=5)

        w_check_fishon_whith_shift = tk.Checkbutton(self, text="中鱼加速收线", variable=self.var_w_check_fishon_whith_shift, command=self.show_selection_water_bottom)
        w_check_fishon_whith_shift.grid(row=12, column=2, padx=10, pady=5)
        return {
            "water_bottom_conf_label" : water_bottom_conf_label,
            "water_bottom_rod_num" : water_bottom_rod_num,
            "w_rod_num" : w_rod_num,
            "water_bottom_strength" : water_bottom_strength,
            "w_strength" : w_strength,
            "water_bottom_throw_offset" : water_bottom_throw_offset,
            "w_throw_offset" : w_throw_offset,
            "water_bottom_wait_line_fly" : water_bottom_wait_line_fly,
            "w_wait_line_fly" : w_wait_line_fly,
            "water_bottom_wait_line_fly_offset" : water_bottom_wait_line_fly_offset,
            "w_wait_line_fly_offset" : w_wait_line_fly_offset,
            "water_bottom_polling_time" : water_bottom_polling_time,
            "w_polling_time" : w_polling_time,
            "racing_rethrow_time" : racing_rethrow_time,
            "r_rethrow_time" : r_rethrow_time,
            "w_check_isfull" : w_check_isfull,
            "w_check_keep_all_fish" : w_check_keep_all_fish,
            "w_check_fishon_whith_shift" : w_check_fishon_whith_shift
        }


    ########################## 水底/赛竿/博格尼亚配置结束###################

    ########################## 手竿配置结束###################
    def create_window_tenkara_conf(self) -> dict[str, any]:
        tenkara_conf_label = tk.Label(self, text="作钓配置:")
        tenkara_conf_label.grid(row=7, column=0, padx=10, pady=5)

        tenkara_rod_num = tk.Label(self, text="鱼竿数量:")
        tenkara_rod_num.grid(row=8, column=0, padx=10, pady=5)
        t_rod_num = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd_single_rod())
        t_rod_num.insert(0, '1')
        t_rod_num.grid(row=8, column=1, padx=10, pady=5)

        tenkara_strength = tk.Label(self, text="抛投力度(秒):")
        tenkara_strength.grid(row=8, column=2, padx=10, pady=5)
        t_strength = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        t_strength.insert(0, '0.8')
        t_strength.grid(row=8, column=3, padx=10, pady=5)

        tenkara_throw_offset = tk.Label(self, text="力度偏移量(秒):")
        tenkara_throw_offset.grid(row=9, column=0, padx=10, pady=5)
        t_throw_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        t_throw_offset.insert(0, '0')
        t_throw_offset.grid(row=9, column=1, padx=10, pady=5)

        tenkara_wait_time = tk.Label(self, text="等待浮标立直(秒):")
        tenkara_wait_time.grid(row=9, column=2, padx=10, pady=5)
        t_wait_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        t_wait_time.insert(0, '2')
        t_wait_time.grid(row=9, column=3, padx=10, pady=5)

        tenkara_wait_time_offset = tk.Label(self, text="浮标入水偏移量(秒):")
        tenkara_wait_time_offset.grid(row=10, column=0, padx=10, pady=5)
        t_wait_time_offset = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        t_wait_time_offset.insert(0, '1')
        t_wait_time_offset.grid(row=10, column=1, padx=10, pady=5)

        tenkara_rethrow_time = tk.Label(self, text="重新抛投间隔(秒):")
        tenkara_rethrow_time.grid(row=10, column=2, padx=10, pady=5)
        t_rethrow_time = tk.Entry(self, width=3, validate='key', validatecommand=self._vcmd())
        t_rethrow_time.insert(0, '-1')
        t_rethrow_time.grid(row=10, column=3, padx=10, pady=5)

        # 创建复选框
        t_check_isfull = tk.Checkbutton(self, text="满力抛投", variable=self.var_t_check_isfull, command=self.show_selection_tenkara)
        t_check_isfull.grid(row=11, column=0, padx=10, pady=5)

        t_check_keep_all_fish = tk.Checkbutton(self, text="保留所有渔获", variable=self.var_t_check_keep_all_fish, command=self.show_selection_tenkara)
        t_check_keep_all_fish.grid(row=11, column=1, padx=10, pady=5)

        t_check_fishon_whith_shift = tk.Checkbutton(self, text="中鱼加速收线", variable=self.var_t_check_fishon_whith_shift, command=self.show_selection_tenkara)
        t_check_fishon_whith_shift.grid(row=11, column=2, padx=10, pady=5)

        t_check_racing_rod = tk.Checkbutton(self, text="赛竿/伯格尼亚", variable=self.var_t_check_racing_rod, command=self.show_selection_tenkara)
        t_check_racing_rod.grid(row=11, column=3, padx=10, pady=5)
        return {
            "tenkara_conf_label" : tenkara_conf_label,
            "tenkara_rod_num" : tenkara_rod_num,
            "t_rod_num" : t_rod_num,
            "tenkara_strength" : tenkara_strength,
            "t_strength" : t_strength,
            "tenkara_throw_offset" : tenkara_throw_offset,
            "t_throw_offset" : t_throw_offset,
            "tenkara_wait_time" : tenkara_wait_time,
            "t_wait_time" : t_wait_time,
            "tenkara_wait_time_offset" : tenkara_wait_time_offset,
            "t_wait_time_offset" : t_wait_time_offset,
            "tenkara_rethrow_time" : tenkara_rethrow_time,
            "t_rethrow_time" : t_rethrow_time,
            "t_check_isfull" : t_check_isfull,
            "t_check_keep_all_fish" : t_check_keep_all_fish,
            "t_check_fishon_whith_shift" : t_check_fishon_whith_shift,
            "t_check_racing_rod" : t_check_racing_rod
        }

    ########################## 手竿配置结束###################
