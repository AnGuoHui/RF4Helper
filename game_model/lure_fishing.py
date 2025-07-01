import logging
from game_model.base_fishing import BaseFishing
import game_model.script  as script
import config.config as config
import time

from log.log_config import MyLogger
from window.variables import LureConfig

logger = logging.getLogger(__name__)

class LureFishing(BaseFishing):
    
    def fishing(self,lure_config:LureConfig) -> None:
        if lure_config.roll_type == "jump_shot":
            self._jump_shot_go(lure_config)
        elif lure_config.roll_type == "dog_walk" or lure_config.roll_type == "constant_roll":
            self._lure_go(lure_config)
        elif lure_config.roll_type == "float_downstream":
            self._float_downstream_go(lure_config)
        else:
            MyLogger.print(logger,logging.error.__name__,'unknown_roll_type')
            config.stop_signal = True
            return
            
    # 路亚抽停钓法 - 单杆操作
    # wait_time  抛投后到收线操作的间隔时间  
    # 抽停时间由dog_walk_time_start和dog_walk_time_end决定,在两个时间值区间中取随机数，dog_walk_time_start应当大于能够触发犬步的时间
    # 取随机数操作来达到拟人效果，dog_walk_time_end应当大于dog_walk_time_start但最好不要超过1秒
    # 抽停做钓采用高收线频率，当dog_walk_time_start过大时，会影响做钓效率（越长的抽停时间会减少单次抛投抽停次数）
    # dog_walk_wait_time_start/end抽停后的停顿时间，也可以用来控制jig类状态(下沉饵)。犬步（浮水饵），通过快速收线即可控制状态，jig类则需要抽停后饵的水层变化才会出状态
    def _lure_go(self,lure_config:LureConfig) -> None:
        rod_staus = False
        # 拿出杆子并抛投
        if not config.stop_signal:
            rod_staus =script.base_rod_single_step(lure_config.l_strength,lure_config.l_check_isfull,lure_config.l_throw_offset,lure_config.l_wait_time,lure_config.l_wait_time_offset)
        # 重复的丢  收操作
        while rod_staus and not config.stop_signal:
        # 抽停操作
            if lure_config.roll_type == "dog_walk":
                rod_staus = script.dog_walk_roll(lure_config.l_dog_walk_time,lure_config.l_dog_walk_time_offset,lure_config.l_check_keep_all_fish,lure_config.l_check_fishon_whith_shift,
                                                    lure_config.l_dog_walk_wait_time,lure_config.l_dog_walk_wait_time_offset,lure_config.l_check_roll_last_line)
                MyLogger.print(logger,logging.info.__name__,'single_rod_finish_once_roll_release')
            elif lure_config.roll_type == "constant_roll":
                rod_staus = script.constant_roll(lure_config.l_check_keep_all_fish,lure_config.l_check_fishon_whith_shift)
                MyLogger.print(logger,logging.info.__name__,'single_rod_finish_once_constant_roll')
            else:
                MyLogger.print(logger,logging.error.__name__,'unknown_roll_type')
                config.stop_signal = True
                return
            # 如果鱼竿状态正常，收完就进行下一次抛投
            if rod_staus and not config.stop_signal:
                script.wait_random_time(0.5,0.5)
                rod_staus = script.base_rod_on_hand_throw(lure_config.l_strength,lure_config.l_check_isfull,lure_config.l_throw_offset,lure_config.l_wait_time,lure_config.l_wait_time_offset)
        config.stop_signal = True

    def _jump_shot_go(self,lure_config:LureConfig) -> None:
        if lure_config.l_rod_num == 2:
            # 拿出杆子并抛投
            script.base_rods_step_on_boat(lure_config.l_rod_num,lure_config.l_strength,lure_config.l_check_isfull,False,lure_config.l_throw_offset)
            # 检查是否至少有一根杆子可用
            if config.rod_status[0] or config.rod_status[1]:
                MyLogger.print(logger,logging.info.__name__,'rod_available_conunt',config.rod_status[0] + config.rod_status[1])
            else:
                MyLogger.print(logger,logging.error.__name__,'rod_available_None')
                config.stop_signal = True
                return
        elif lure_config.l_rod_num == 1:
            config.rod_status[0] = script.base_rod_single_step(lure_config.l_strength,lure_config.l_check_isfull,lure_config.l_throw_offset)
            # 记录抛投时间
            config.re_throw[0] = time.time()
            # 检查是否至少有一根杆子可用
            if config.rod_status[0]:
                MyLogger.print(logger,logging.info.__name__,'rod_available_one')
            else:
                MyLogger.print(logger,logging.error.__name__,'rod_available_None')
                config.stop_signal = True
                return
        else:
            MyLogger.print(logger,logging.error.__name__,'rod_num_illegal')
            config.stop_signal = True
            return
        while not config.stop_signal:
            # 此时杆子已经入水，开始切换杆子，检查中鱼信号与跳底操作
            rod_staus_ok_num = config.rod_status[0]+config.rod_status[1]
            if rod_staus_ok_num > 0:
                # 双杆都在水中，检查是否有中鱼信号
                for i in range(rod_staus_ok_num):
                    script.pick_rod_on_hand(i)
                    # 等游戏取竿操作
                    script.wait_random_time(0.8,0.2)
                    config.rod_status[i] ,throw_flg = script.jump_shot_roll(lure_config.l_wait_time,lure_config.l_wait_time_offset
                                          ,lure_config.l_roll_line_time,lure_config.l_roll_line_time_offset,lure_config.l_roll_line_wait_time,lure_config.l_roll_line_wait_time_offset,lure_config.l_hold_rod_time,jump_shot_type = lure_config.l_jump_shot_type.value,keep_all_fish = lure_config.l_check_keep_all_fish,fishon_whith_shift = lure_config.l_check_fishon_whith_shift,rod_number=i)
                    if throw_flg and not config.stop_signal:
                        # 上鱼收线后重新抛投
                        config.rod_status[i] = script.base_rod_on_hand_throw(lure_config.l_strength,lure_config.l_check_isfull,lure_config.l_throw_offset)
                        if config.rod_status[i]:
                            script.wait_random_time(1.5,0.2)
                            config.re_throw[i] = time.time()
                            config.jump_shot_wheel_closed[i] = False
                        else:
                            MyLogger.print(logger,logging.info.__name__,'rod_throw_failed',i+1)
                    else:
                        # 正常切杆  等待游戏响应
                        script.wait_random_time(0.5,0.2)
            else:
                MyLogger.print(logger,logging.error.__name__,'rod_available_None')
                config.stop_signal = True
                        
    def _float_downstream_go(self,lure_config:LureConfig) -> None:
        rod_staus = False
        # 拿出杆子并抛投
        if not config.stop_signal:
            config.rod_status[0] = script.base_rod_single_step(lure_config.l_strength,lure_config.l_check_isfull,lure_config.l_throw_offset)
            # 记录抛投时间
            config.re_throw[0] = time.time()
            # 检查是否至少有一根杆子可用
            if config.rod_status[0]:
                MyLogger.print(logger,logging.info.__name__,'rod_available_one')
                rod_staus = True
            else:
                MyLogger.print(logger,logging.error.__name__,'rod_available_None')
                config.stop_signal = True
                return
        # 重复的丢  收操作
        while rod_staus and not config.stop_signal:
            # 漂钓操作
            rod_staus = script.float_downstream_roll(lure_config.l_float_downstream_rethrow_time,lure_config.l_float_downstream_rethrow_time_offset,lure_config.l_check_keep_all_fish,lure_config.l_check_fishon_whith_shift)
            MyLogger.print(logger,logging.error.__name__,'float_downstream_complet')
            # 如果鱼竿状态正常，收完就进行下一次抛投
            if rod_staus and not config.stop_signal:
                rod_staus = script.base_rod_on_hand_throw(lure_config.l_strength,lure_config.l_check_isfull,lure_config.l_throw_offset,lure_config.l_wait_time,lure_config.l_wait_time_offset)
                if rod_staus:
                    script.wait_random_time(1.5,0.2)
                    config.re_throw[0] = time.time()
                else:
                    MyLogger.print(logger,logging.info.__name__,'rod_throw_failed',1)
        config.stop_signal = True