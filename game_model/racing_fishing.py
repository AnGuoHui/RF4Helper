# 赛竿/博格尼亚竿

import logging
import time
from config import config
from game_model.base_fishing import BaseFishing
import game_model.script  as script
from log.log_config import MyLogger
from window.variables import WaterBottomConfig

logger = logging.getLogger(__name__)

class RacingFishing(BaseFishing):
    
    def fishing(self,racing_config:WaterBottomConfig) -> None:
        self._racing_go(racing_config)

    #赛竿/博格尼亚竿钓鱼
    def _racing_go(self,racing_config:WaterBottomConfig) -> None:
        rod_staus = False
        if racing_config.w_rod_num > 0:
            # 拿出杆子并抛投
            if racing_config.water_bottom_model == "automatic":
                if racing_config.w_rod_num > 1:
                    script.base_rods_step(racing_config.w_rod_num,racing_config.w_strength,racing_config.w_check_isfull,False,racing_config.w_wait_line_fly,racing_config.w_wait_line_fly_offset,racing_config.w_throw_offset,racing_config.r_rethrow_time)
                else:
                    config.rod_status[0] = script.base_rod_single_step(racing_config.w_strength,racing_config.w_check_isfull,racing_config.w_throw_offset,racing_config.w_wait_line_fly,racing_config.w_wait_line_fly_offset)
                    config.re_throw[0] = time.time()
                # 检查是否至少有一根杆子可用
                if config.rod_status[0] or config.rod_status[1] or config.rod_status[2]:
                    rod_staus = True
                else:
                    MyLogger.print(logger,logging.error.__name__,'rod_available_None')
            elif racing_config.water_bottom_model == "monitor":
                for i in range(racing_config.w_rod_num):
                    config.rod_status[i] = True
                    if racing_config.r_rethrow_time > 0:
                        config.re_throw[i] = time.time()
                rod_staus = True
            else:
                MyLogger.print(logger,logging.error.__name__,'unknown_operate_type')
                config.stop_signal = True
                return
        else:
            MyLogger.print(logger,logging.error.__name__,'rod_num_error')
        # 遍历鱼竿状态会导致滑口问题，可以根据鱼口自行确定遍历时间
        while rod_staus and not config.stop_signal:
            if racing_config.w_rod_num > 1:
                # 可退出的阻塞操作
                start_time = time.time()
                while time.time() - start_time < racing_config.w_polling_time-config.range_rods_expend and not config.stop_signal:
                    continue
                # 遍历鱼竿上鱼情况
                if not config.stop_signal:
                    rod_staus = self._range_rods(racing_config)
            elif racing_config.w_rod_num == 1:
                # 单竿操作
                rod_staus = self._whatch_single_rod(racing_config)
            else:
                MyLogger.print(logger,logging.error.__name__,'rod_num_error')
                config.stop_signal = True
        config.stop_signal = True

    # 遍历鱼竿上鱼情况
    def _range_rods(self,racing_config:WaterBottomConfig):
        # 遍历鱼竿上鱼情况
        if not config.stop_signal:
            range_start_time = time.time()
            # 获取可用鱼竿信息
            for i in range(racing_config.w_rod_num):
                if config.stop_signal:
                    break
                else:
                    if config.rod_status[i]:
                        MyLogger.print(logger,logging.info.__name__,'range_rod_and_check',i+1)
                        script.pick_rod_on_hand(i)
                        # 等待画面加载
                        script.wait_random_time(0.8,0.2)
                        # 有管轮卡信号，或者超出重新抛投时间
                        if not script.racing_roll_check() or (racing_config.r_rethrow_time > 0 and time.time() - config.re_throw[i] > racing_config.r_rethrow_time):
                            MyLogger.print(logger,logging.info.__name__,'range_rod_and_roll_line',i+1)
                            config.rod_status[i] = script.constant_roll(racing_config.w_check_keep_all_fish,racing_config.w_check_fishon_whith_shift,False)
                            MyLogger.print(logger,logging.info.__name__,'range_rod_and_roll_line_finish',i+1)
                            # 如果鱼竿状态正常，收完就进行下一次抛投
                            if config.rod_status[i] and not config.stop_signal:
                                script.wait_random_time(0.5,0.2)
                                config.rod_status[i] = script.base_rod_on_hand_throw(racing_config.w_strength,racing_config.w_check_isfull,racing_config.w_throw_offset)
                                # 重置重新抛投时间
                                if config.rod_status[i] and racing_config.r_rethrow_time > 0:
                                    config.re_throw[i] = time.time()
                        script.set_rod_on_ground()
                        MyLogger.print(logger,logging.info.__name__,'range_rod_and_put_on_ground',i+1)
                        # 等待游戏反馈，避免过快的操作
                        script.wait_random_time(1,0.5)
            config.range_rods_expend = time.time() - range_start_time
            # 遍历完毕，杆子状态可能更新，更新rod_staus
            # 检查是否至少有一根杆子可用
            if config.rod_status[0] or config.rod_status[1] or config.rod_status[2]:
                return True
            else:
                MyLogger.print(logger,logging.error.__name__,'rod_available_None')
                return False
        else:
            return False
        
    # 遍历鱼竿上鱼情况
    def _whatch_single_rod(self,racing_config:WaterBottomConfig):
        # 有管轮卡信号，或者超出重新抛投时间
        if not script.racing_roll_check() or (racing_config.r_rethrow_time > 0 and time.time() - config.re_throw[0] > racing_config.r_rethrow_time):
            MyLogger.print(logger,logging.info.__name__,'single_rod_roll_line')
            config.rod_status[0] = script.constant_roll(racing_config.w_check_keep_all_fish,racing_config.w_check_fishon_whith_shift,False)
            MyLogger.print(logger,logging.info.__name__,'single_rod_finish_roll_line')
            # 如果鱼竿状态正常，收完就进行下一次抛投
            if config.rod_status[0] and not config.stop_signal:
                script.wait_random_time(0.5,0.2)
                # 去除光照影响导致的信号获取失败,确定有管轮卡信号再继续抛投
                while not script.racing_roll_check() and not config.stop_signal:
                    MyLogger.print(logger,logging.warning.__name__,'line_clip_not_found_and_waiting')
                    script.wait_random_time(0.5,0.2)
                config.rod_status[0] = script.base_rod_on_hand_throw(racing_config.w_strength,racing_config.w_check_isfull,racing_config.w_throw_offset,racing_config.w_wait_line_fly,racing_config.w_wait_line_fly_offset)
                # 重置重新抛投时间
                if config.rod_status[0] and racing_config.r_rethrow_time > 0:
                    config.re_throw[0] = time.time()
        # 检查是否至少有一根杆子可用
        if config.rod_status[0]:
            return True
        else:
            MyLogger.print(logger,logging.error.__name__,'rod_available_None')
            return False