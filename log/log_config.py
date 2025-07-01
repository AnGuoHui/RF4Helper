import logging
import tkinter as tk

from config import config

# 重定向logging输出
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + '\n')  # 将日志消息插入文本框
        self.text_widget.see(tk.END)

    def set_handler(self):
        # 日志配置初始化
        logger = logging.getLogger()
        logger.setLevel(config.log_level)  # 设置日志级别
        if config.log_level == logging.DEBUG:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        else:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.setFormatter(formatter)
        # 移除默认的处理器
        if logger.hasHandlers():
            logger.handlers.clear()  # 清空默认处理器
        logger.addHandler(self)

class MyLogger:
    
    messages = {
        1: {
            'script_quit': "本次操作结束。。。。。。",
            'key_4_start_listening': "开始循环按下4键进行食物/饮品使用，使用间隔{}秒",
            'gaming_check': "{}秒后开始检查是否进入游戏。。。",
            'waiting_for_game_single' : "等待视角进入游戏中(人物健康状态图标未检查到)...",
            'match_and_bolognese_notice': "赛竿/伯格尼亚钓组必须预先设定管轮卡！！！",

            'crafting_notice':"{}秒后开始检制作，请将鼠标移动到游戏内的制作按钮处...",
            'crafting_total_notice':"请将制作总量设置为大于0的整数",

            'unknown_roll_type':"未知的收线操作类型！！！,即将退出！！！",
            'single_rod_finish_once_roll_release':"路亚抽停钓法 - 单杆操作 完成一次....",
            'single_rod_finish_once_constant_roll':"路亚匀收钓法 - 单杆操作 完成一次....",
            'rod_available_conunt':"当前有{}根杆子可用",
            'rod_available_None':"没有可用杆子，无法进行抛投操作，即将退出！！！",
            'rod_available_one':"当前有1根杆子可用",
            'rod_num_illegal':"错误的鱼竿数量，当前只支持单竿/双竿操作，即将退出！！！",
            'rod_throw_failed':"杆子{} 抛投失败，已标记为不可用！！！",

            'unknown_operate_type':"未知的操作类型！！！,即将退出！！！",
            'rod_num_error':"错误的鱼竿数量，即将退出！！！",
            'range_rod_and_check':"遍历第{}根杆子，上鱼情况检查",
            'range_rod_and_roll_line':"第{}根杆子开始收线",
            'range_rod_and_roll_line_finish':"第{}根杆子完成收线",
            'range_rod_and_put_on_ground':"第{}根杆子插地",
            'single_rod_roll_line':"第1根杆子开始收线",
            'single_rod_finish_roll_line':"第1根杆子完成收线",
            'line_clip_not_found_and_waiting': "管轮卡信号检测失败，等待中。。。",
            'skip_erro_rod': "第{}根杆子状态异常，跳过",

            'handel_rod': "杆子{}已取出",
            'float_missing_wait': "浮标未检测到，等待中。。。",
            'float_found_continue': "浮标已检测到，进入监测中。。。",
            'rod_rethrow_out_of_missing_count': "浮标小信号计数器已到达阈值，重新抛投。。。",
            'rod_rethrow_out_of_wait_time': "浮标检测超时，重新抛投",
            'float_bite_wait': "浮标已检测到，等待咬口中。。。",
            'rod_rethrow_out_of_rethrow_conf': "重新抛投设置生效，重新抛投准备中。。",
            'float_missing_bite': "浮标信号已消失-咬口，开始准备收线。。。",
            'float_re_show': "浮标重新出现，等待下一次咬口。。。",
            'float_complete': "手竿钓具 - 单杆操作 完成一次。。。",

            'constant_roll_start': "匀收开始。。。",
            'constant_roll_finish': "匀收结束。。。",
            'constant_roll_continue': "匀收中。。。",
            'fish_on': "中鱼。。。",
            'roll_stop_start': "抽停开始。。。",
            'roll_stop_finish': "抽停结束。。。",
            'roll_stop_continue': "抽停中。。。",
            'roll_stop_wait_next_roll': "等待下一次抽停中。。。",

            'jump_shot_bite': "{}号竿，拟饵下沉中咬口。。。",
            "jump_shot_roll_start":"跳底动作开始。。。持杆时间：{}",
            "befor_jump_shot_bite":"{}号竿，拟饵跳底操作前咬口",
            "jump_shot_skip":"未到跳底操作时间，跳过。。。",
            "jump_shot_action_bite":"{}号竿，拟饵跳底中咬口",
            "jump_shot_type_erro":"跳底操作类型错误！！！,即将退出。。。",

            "float_downstream_bite":"漂钓咬口，开始收线。。。",
            "float_downstream_wait_bite":"漂钓,等待咬口中。。。",
            "float_downstream_complet":"路亚漂流钓法 - 单杆操作 完成一次。。。",

            "offset_over_strength":"offset偏移量绝对值大于strength,强制设定为0",

            "catch_fish_start":"抄鱼入户动作开始。。。",
            "catch_fish_end":"抄鱼动作结束。。。",
            "float_catch_fish_start":"手竿收线与抄鱼入户动作开始。。。",
            "float_catch_fish_end":"手竿收线与抄鱼动作结束。。。",
            "float_catch_fish_first_try":"第一次抄鱼完成。。。",
            "float_catch_fish_second_try":"尝试第二次抄鱼。。。",
            "float_catch_fish_miss_fish_on_singl":"未获取到中鱼信号，正在收线准备下一次抛投。。。",
            "float_catch_fish_first_try_fail":"多次抄鱼失败，尝试松线进行第二次抄鱼尝试",

            "catch_fish_judge":"收线结束后---有鱼判断。。。",
            "catch_fish_loding":"有加载画面，等待加载结束。。。",
            "catch_fish_miss_fish_on_singl":"抄鱼动作中脱钩或未识别到收线完成。。。",
            "catch_fish_miss_fish_on_singl_wait_roll_line_finish":"抄鱼动作中获取中鱼信号失败，等待收线完成。。。",
            "script_need_help":"长时间未获取到钓具完成准备信号，需要手动介入。。。",

            "continue_roll_line_with_fish":"中鱼后持续收线。。。",
            "quit_roll_line_with_zero_line_bite":"赛竿收线到5米内出现咬口,线杯显示为0米,退出收线。。。",
            "continue_roll_line_with_fish_finish":"中鱼后持续收线结束。。。",
            "catch_fish_by_hook_set":"刺鱼入户。。。",
            "fish_unhook":"脱钩。。。",

            "keep_fish_start":"入户动作开始。。。",
            "keepnet_full":"满户，放生所有钓获。。。",
            "keepnet_add_rare_fish":"只允许稀有钓获入户。。。",
            "relese_normal_fish":"放生非稀有钓获。。。",
            "keep_fish_end":"入户动作结束。。。",

            "rod_placement_check_start":"杆子{}插地检查开始。。。",
            "rod_number_erro":"杆子编号错误。。。",
            "rod_placement_fail_and_retry":"杆子{}插地失败,重试一次",
            "move_back":"向后移动",
            "rod_placement_fail_and_mark_notready":"杆子{}插地失败,已标记为不可用",
            "rod_placement_check_result":"杆子{}插地检查结束,placement_check_result={}",

            "fource_jump_shot_start":"杆子{}开始抽竿跳底动作。。。",
            "jump_shot_whith_whell_open":"杆子{}线杯是否关闭{}。。。",
            "wheel_close":"杆子{}关闭线杯。。。",
            "fource_jump_shot_end":"杆子{}结束抽竿跳底动作。。。",
            "gentle_jump_shot_start":"杆子{}开始抬竿跳底动作。。。",
            "gentle_jump_shot_end":"杆子{}结束抬竿跳底动作。。。",
            "roll_jump_shot_start":"杆子{}开始收线跳底动作。。。",
            "rool_jump_shot_end":"杆子{}结束收线跳底动作。。。",

            'rod_not_ready': "鱼竿状态异常，将鱼竿插地。。。",
            'game_disconnect': "检查到游戏断开连接，停止运行。。。",
            'choose_ticket': "检查到船票到期，停止运行。。。",
            'wait_roll_line_finsh': "等待收线完成。。。",
            'rod_not_ready_do_nothing': "鱼竿状态异常。。。",
            'rod_not_ready_do_check': "抛投准备状态异常，请检查。。。",

            'crafting_succ': "制作完成，已完成{}/{}个物品,失败{}次",
            'crafting_fail': "制作失败，已完成{}/{}个物品,失败{}次",
            'crafting_stop': "缺失材料，已完成{}/{}个物品,失败{}次，准备退出。。。",
            'crafting_end': "已完成所有制作：{}/{}个物品,失败{}次，准备退出。。。",
            'crafting_wait': "等待制作完成。。。",

            'unknown_rod_type': "未知的钓竿类型",
            'acc_stop_singl': "停止信号已收到，停止执行操作。。。",
            'listen_stop_singl': "监听到退出信号。。。",
            'stop_singl_notice': "使用9键退出程序。。。"
        },
        0: {
            'script_quit': "script quit...",
            'key_4_start_listening': "start thread for eat/drink(key 4),interval {} seconds",
            'gaming_check': "wati for {} seconds before start gaming check...",
            'waiting_for_game_single' : "waiting for game view(people helth icon not found)...",
            'match_and_bolognese_notice': "match rig and bolognese rig must set line clip before start fishing!!!",

            'crafting_notice':"please move mouse to Make button in game, {} seconds later starting...",
            'crafting_total_notice':"please set crafting total quantity greater than 0 integer",

            'unknown_roll_type':"unknown roll type, exit now!!!",
            'single_rod_finish_once_roll_release':"lure single rod roll-release operation finish once....",
            'single_rod_finish_once_constant_roll':"lure single rod constant-roll operation finish once....",
            'rod_available_conunt':"current rod available count is {}",
            'rod_available_None':"no rod available, cannot perform throw operation, exit now!!!",
            'rod_available_one':"current rod available count is 1",
            'rod_num_illegal':"illegal rod number, only support single/double rod operation, exit now!!!",
            'rod_throw_failed':"rod {} throw failed, mark as unavailable!!!",

            'unknown_operate_type':"unknown operate type, exit now!!!",
            'rod_num_error':"illegal rod number, exit now!!!",
            'range_rod_and_check':"range rod {} and check on fish icon",
            'range_rod_and_roll_line':"rod {} start roll line",
            'range_rod_and_roll_line_finish':"rod {} finish roll line",
            'range_rod_and_put_on_ground':"rod {} put on ground",
            'single_rod_roll_line':"single rod start roll line",
            'single_rod_finish_roll_line':"single rod finish roll line",
            'line_clip_not_found_and_waiting': "line clip not found, waiting...",
            'skip_erro_rod': "rod{} is not ready,skip...",

            'handel_rod': "rod {} take out",
            'float_missing_wait': "float not found, waiting...",
            'float_found_continue': "float found, continue monitoring...",
            'rod_rethrow_out_of_missing_count': "float signal counter reach threshold, rethrow...",
            'rod_rethrow_out_of_wait_time': "float detect timeout, rethrow...",
            'float_bite_wait': "float found, waiting for bite...",
            'rod_rethrow_out_of_rethrow_conf': "rethrow conf effective, rethrow prepare...",
            'float_missing_bite': "float signal disappear-bite, start roll line...",
            'float_re_show': "float reappear, waiting for next bite...",
            'float_complete': "telescopic signle rod finish once...",

            'constant_roll_start': "constant-roll start...",
            'constant_roll_finish': "constant-roll finish...",
            'constant_roll_continue': "constant-roll continue...",
            'fish_on': "fish on...",
            'roll_stop_start': "roll-stop start...",
            'roll_stop_finish': "roll-stop finish...",
            'roll_stop_continue': "roll-stop continue...",
            'roll_stop_wait_next_roll': "roll-stop wait for next roll...",

            'jump_shot_bite': "{} rod, baits sinking on bite...",
            "jump_shot_roll_start":"jump shot roll start... hold_time:{}",
            "befor_jump_shot_bite":"{} rod, befor jump shot action get bite...",
            "jump_shot_skip":"wait jump shot action,skip...",
            "jump_shot_action_bite":"{} rod, get bite at jump shot action",
            "jump_shot_type_erro":"jump shot type erro ,exit now!!!",

            "float_downstream_bite":"float downstream get bite,roll start...",
            "float_downstream_wait_bite":"float downstream wait bite...",
            "float_downstream_complet":"float downstream signle rod finish once...",

            "offset_over_strength":"offset absolute value  greater than strength,offset will be zero",

            "catch_fish_start":"catch fish action start...",
            "catch_fish_start":"catch fish action end...",
            "float_catch_fish_start":"float catch fish action start...",
            "float_catch_fish_end":"float catch fish action end...",
            "float_catch_fish_first_try":"float catch fish first try complete...",
            "float_catch_fish_second_try":"float catch fish second try start...",
            "float_catch_fish_miss_fish_on_singl":"float catch fish miss fish_on singl,roll line for next drop",
            "float_catch_fish_first_try_fail":"first try not catch fish in many times, try to release line and do second try ...",

            "catch_fish_judge":"roll line finish ,judge fish...",
            "catch_fish_loding":"wait loding finish ...",
            "catch_fish_miss_fish_on_singl":"catch fish miss fish_on singl,maby fish unhook",
            "catch_fish_miss_fish_on_singl_wait_roll_line_finish":"catch fish miss fish_on singl wait roll line finish",
            "script_need_help":"long time not get rod ready singl,script need help",

            "continue_roll_line_with_fish":"continue roll line with fish",
            "quit_roll_line_with_zero_line_bite":"match rod get bite at zeto line,quit roll line...",
            "continue_roll_line_with_fish_finish":"continue roll line with fish finish...",
            "catch_fish_by_hook_set":"catch fish by hook set...",
            "fish_unhook":"fish unhook...",

            "keep_fish_start":"keep fish start...",
            "keepnet_full":"keepnet full reles all fish...",
            "keepnet_add_rare_fish":"keepnet just keep trophy fish...",
            "relese_normal_fish":"reless normal fish...",
            "keep_fish_end":"keep fish end...",

            "rod_placement_check_start":"rod{}placement check start...",
            "rod_number_erro":"rod number erro",
            "rod_placement_fail_and_retry":"rod{}placement fail,start another try...",
            "move_back":"move back",
            "rod_placement_fail_and_mark_notready":"rod{}placement fail,mark rod as not useable...",
            "rod_placement_check_result":"rod{}placement check over,placement_check_result={}",

            "fource_jump_shot_start":"rod{}fource jump shot start...",
            "jump_shot_whith_whell_open":"rod{}reel is closed{}...",
            "wheel_close":"rod{}close reel...",
            "fource_jump_shot_end":"rod{}fource jump shot end...",
            "gentle_jump_shot_start":"rod{}gentle jump shot start...",
            "gentle_jump_shot_end":"rod{}gentle jump shot end...",
            "roll_jump_shot_start":"rod{}rool jump shot start...",
            "rool_jump_shot_end":"rod{}rool jump shot end...",

            'rod_not_ready': "Rod status abnormal, planting the rod...",
            'game_disconnect': "get disconnect signle,script stop...",
            'choose_ticket': "get choose ticket signle,script stop...",
            'wait_roll_line_finsh': "wait roll line finsh..",
            'rod_not_ready_do_nothing': "rod not ready...",
            'rod_not_ready_do_check': "rod not ready for casting,please check...",

            'crafting_succ': "crafting succ,complete :{}/{}items,fail{}",
            'crafting_fail': "crafting fail,complete :{}/{}items,fail{}",
            'crafting_stop': "need more materials,complete :{}/{}items,fail{},script quit...",
            'crafting_end': "complete :{}/{}items,fail{},script quit...",
            'crafting_wait': "wait for crafting complete",

            'unknown_rod_type': "unknown rod type...",
            'acc_stop_singl': "accept stop signl,script quit...",
            'listen_stop_singl': "listen stop singl...",
            'stop_singl_notice': "press keybord 9 to stop script!!!"
        }
    }

    @classmethod
    def print(cls, logger: logging.Logger,log_function_name:str, msg_key:str, *args):
        log_function = getattr(logger, log_function_name, logger.info)
        message_template  = cls.messages.get(config.ui_language, {}).get(msg_key, f"Unknown msg_key:{msg_key}")
        message = message_template.format(*args)
        log_function(message)