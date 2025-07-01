
from enum import Enum
import logging
from window.base_app import BaseApp
import tkinter as tk

# 页面基础变量
class Variables(BaseApp):
    def __init__(self):
        super().__init__()
        # 创建变量以存储配置信息
        lure_config = LureConfig()
        water_bottom_config = WaterBottomConfig()
        tenkara_config = TenkaraConfig()
        self.fishing_config = FishingConfig(lure_config,water_bottom_config,tenkara_config)

        # 创建变量以存储复选框的状态
        # lure
        self.var_l_check_roll_last_line = tk.IntVar()
        self.var_l_check_isfull = tk.IntVar()
        self.var_l_check_keep_all_fish = tk.IntVar()
        self.var_l_check_fishon_whith_shift = tk.IntVar()

        # water_bottom
        self.var_w_check_isfull = tk.IntVar()
        self.var_w_check_keep_all_fish = tk.IntVar()
        self.var_w_check_fishon_whith_shift = tk.IntVar()

        # tenkara
        self.var_t_check_isfull = tk.IntVar()
        self.var_t_check_keep_all_fish = tk.IntVar()
        self.var_t_check_fishon_whith_shift = tk.IntVar()
        self.var_t_check_racing_rod = tk.IntVar()

        # 创建用于切换顶层ui的变量
        self.ui_selection = tk.StringVar(value="ui_rod")  # 钓具默认值

        # 创建用于钓具类型选择的变量
        self.rod_selection = tk.StringVar(value=self.fishing_config.rod_type)  # 钓具默认值
        self.roll_selection = tk.StringVar(value=self.fishing_config.lure_config.roll_type)  # 收线方式默认值
        self.jump_shot_selection = tk.IntVar(value=self.fishing_config.lure_config.l_jump_shot_type.value) #跳底设置
        self.water_bottom_selection = tk.StringVar(value=self.fishing_config.water_bottom_config.water_bottom_model)  # 水底操作类型默认值
        self.log_level_selection = tk.StringVar(value="info")  # 日志等级默认值

class JumpShotType(Enum):
    ROLL_RELEASE = 0 #收线跳底
    RAISE_ROD = 1 #抬竿跳底
    FORCE = 2 #强抽跳底

# 页面配置项接收
class LureConfig:
    def __init__(self):
        # lure_config start
        self.roll_type = "constant_roll"#收线方式
        self.l_rod_num = 1#路亚钓具数量
        self.l_strength = 0.8#路亚抛投力度
        self.l_throw_offset = 0#路亚抛投力度偏移量
        self.l_wait_time = 2#路亚等待饵到位时间
        self.l_wait_time_offset = 1#路亚等待饵到位时间偏移量
        self.l_check_isfull = False#路亚是否满力抛投
        self.l_check_keep_all_fish = False#路亚是否保留所有渔获
        self.l_check_fishon_whith_shift = False#路亚-中鱼是否加速收线
        # 抽停
        self.l_dog_walk_time = 0.3#路亚抽停时间
        self.l_dog_walk_time_offset = 0.2#路亚抽停时间偏移量
        self.l_dog_walk_wait_time = 0.3#路亚抽停等待时间
        self.l_dog_walk_wait_time_offset = 0.2#路亚抽停等待时间偏移量
        self.l_check_roll_last_line = False#路亚抽停模式下是否快速收完最后5米线
        # 跳底
        self.l_roll_line_time = 1#路亚跳底时间
        self.l_roll_line_time_offset = 0.2#路亚跳底时间偏移量
        self.l_roll_line_wait_time = 9#路亚跳底等待时间
        self.l_roll_line_wait_time_offset = 0.2#路亚跳底等待时间偏移量
        self.l_hold_rod_time = 3 #路亚持竿时间/切杆等待时长
        self.l_jump_shot_type = JumpShotType.ROLL_RELEASE#路亚跳底方式
        #顺水
        self.l_float_downstream_rethrow_time = 60 #重新抛投间隔时间
        self.l_float_downstream_rethrow_time_offset = 2 #间隔偏移量

    def __str__(self):
        return f"LureConfig(roll_type:{self.roll_type},l_rod_num:{self.l_rod_num},l_strength:{self.l_strength},l_throw_offset:{self.l_throw_offset},l_wait_time:{self.l_wait_time},l_wait_time_offset:{self.l_wait_time_offset},l_check_isfull:{self.l_check_isfull},l_check_keep_all_fish:{self.l_check_keep_all_fish},l_check_fishon_whith_shift:{self.l_check_fishon_whith_shift},l_dog_walk_time:{self.l_dog_walk_time},l_dog_walk_time_offset:{self.l_dog_walk_time_offset},l_dog_walk_wait_time:{self.l_dog_walk_wait_time},l_dog_walk_wait_time_offset:{self.l_dog_walk_wait_time_offset},l_check_roll_last_line:{self.l_check_roll_last_line},l_roll_line_time:{self.l_roll_line_time},l_roll_line_time_offset:{self.l_roll_line_time_offset},l_roll_line_wait_time:{self.l_roll_line_wait_time},l_roll_line_wait_time_offset:{self.l_roll_line_wait_time_offset},l_hold_rod_time:{self.l_hold_rod_time},l_jump_shot_type:{self.l_jump_shot_type},l_float_downstream_rethrow_time:{self.l_float_downstream_rethrow_time},l_float_downstream_rethrow_time_offset:{self.l_float_downstream_rethrow_time_offset})"

class WaterBottomConfig:
    def __init__(self):
         #水底
        self.water_bottom_model = "automatic"#水底做钓模式
        self.w_rod_num = 1#水底钓具数量
        self.w_strength = 0.8#水底钓具抛投力度
        self.w_throw_offset = 0#水底钓具投抛力度偏移量
        self.w_wait_line_fly = 1#等待钩饵入水时长
        self.w_wait_line_fly_offset = 1#等待钩饵入水时长偏移量
        self.w_polling_time = 100#水底钓具轮询时间
        self.r_rethrow_time = -1#赛竿/伯格尼亚重新抛投时间
        self.w_check_isfull = False#水底钓具是否满力抛投
        self.w_check_keep_all_fish = False#水底钓具是否保留所有渔获
        self.w_check_fishon_whith_shift = False#水底钓具-中鱼是否加速收线

    def __str__(self):
        return f"WaterBottomConfig(water_bottom_model:{self.water_bottom_model},w_rod_num:{self.w_rod_num},w_strength:{self.w_strength},w_throw_offset:{self.w_throw_offset},w_wait_line_fly:{self.w_wait_line_fly},w_wait_line_fly_offset:{self.w_wait_line_fly_offset},w_polling_time:{self.w_polling_time},r_rethrow_time:{self.r_rethrow_time},w_check_isfull:{self.w_check_isfull},w_check_keep_all_fish:{self.w_check_keep_all_fish},w_check_fishon_whith_shift:{self.w_check_fishon_whith_shift})"

class TenkaraConfig:
    def __init__(self):
        self.t_rod_num = 1#手竿数量
        self.t_strength = 0.8#手竿抛投力度
        self.t_throw_offset = 0#手竿抛投力度偏移量
        self.t_wait_time = 2#手竿等待浮子立直时间
        self.t_wait_time_offset = 1#手竿等待浮子立直时间偏移量
        self.t_rethrow_time = -1#手竿重新抛投时间
        self.t_check_isfull = False#手竿是否满力抛投
        self.t_check_keep_all_fish = False#手竿是否保留所有渔获
        self.t_check_fishon_whith_shift = False#手竿-中鱼是否加速收线
        self.t_check_racing_rod = False#手竿是否为赛竿/伯格尼亚

    def __str__(self):
        return f"TenkaraConfig(t_rod_num:{self.t_rod_num},t_strength:{self.t_strength},t_throw_offset:{self.t_throw_offset},t_wait_time:{self.t_wait_time},t_wait_time_offset:{self.t_wait_time_offset},t_rethrow_time:{self.t_rethrow_time},t_check_isfull:{self.t_check_isfull},t_check_keep_all_fish:{self.t_check_keep_all_fish},t_check_fishon_whith_shift:{self.t_check_fishon_whith_shift},t_check_racing_rod:{self.t_check_racing_rod})"

class FishingConfig:
    def __init__(self,lure_config:LureConfig,water_bottom_config:WaterBottomConfig,tenkara_config:TenkaraConfig):
        self.rod_type = "lure"
        self.lure_config = lure_config
        self.water_bottom_config = water_bottom_config
        self.tenkara_config = tenkara_config

    def __str__(self):
        return f"FishingConfig(rod_type:{self.rod_type},lure_config:{self.lure_config},water_bottom_config:{self.water_bottom_config},tenkara_config:{self.tenkara_config})"