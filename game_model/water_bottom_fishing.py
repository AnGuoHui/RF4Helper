import logging
from game_model.base_fishing import BaseFishing
import game_model.script  as script
import config.config as config
import time

from window.variables import WaterBottomConfig
from log.log_config import MyLogger

logger = logging.getLogger(__name__)

#########################################沉底渔具#######################################

class WaterBottomFishing(BaseFishing):

    def fishing(self,water_bottom_config:WaterBottomConfig) -> None:
        self._water_bottom_go(water_bottom_config)

    #水底钓鱼
    def _water_bottom_go(self,water_bottom_config:WaterBottomConfig) -> None:
        rod_staus = False
        if water_bottom_config.w_rod_num > 0:
            # 拿出杆子并抛投
            if water_bottom_config.water_bottom_model == "automatic":
                script.base_rods_step(water_bottom_config.w_rod_num,water_bottom_config.w_strength,water_bottom_config.w_check_isfull,True,water_bottom_config.w_wait_line_fly,water_bottom_config.w_wait_line_fly_offset,water_bottom_config.w_throw_offset)
                # 检查是否至少有一根杆子可用
                if config.rod_status[0] or config.rod_status[1] or config.rod_status[2]:
                    rod_staus = True
                else:
                    MyLogger.print(logger,logging.info.__name__,'rod_available_None')
            elif water_bottom_config.water_bottom_model == "monitor":
                for i in range(water_bottom_config.w_rod_num):
                    config.rod_status[i] = True
                rod_staus = True
            else:
                MyLogger.print(logger,logging.info.__name__,'unknown_operate_type')
                config.stop_signal = True
                return
        else:
            MyLogger.print(logger,logging.info.__name__,'rod_available_None')
        # 此时沉底渔具已在水中，等待中鱼，在上鱼时，沉底杆详细页列表处会有闪烁，获取到这个信号后在可用杆子里面进行提杆操作，并进行上鱼图标识别，进行后续操作
        # 经过测试，----在上鱼时，沉底杆详细页列表处会有闪烁----会有bug，闪烁情况不一定存在，直接在指定时间(提供可变参数)内执行遍历鱼竿，对上鱼图标进行判断即可
        # 遍历鱼竿状态会导致滑口问题，可以根据鱼口自行确定遍历时间
        while rod_staus and not config.stop_signal:
            # 可退出的阻塞操作
            start_time = time.time()
            while time.time() - start_time < water_bottom_config.w_polling_time-config.range_rods_expend and not config.stop_signal:
                continue
            # 遍历鱼竿上鱼情况
            rod_staus = self._range_rods(water_bottom_config)
        config.stop_signal = True

    # 遍历鱼竿上鱼情况
    def _range_rods(self,water_bottom_config:WaterBottomConfig):
        range_start_time = time.time()
        # 遍历鱼竿上鱼情况
        for i in range(water_bottom_config.w_rod_num):
            if config.stop_signal:
                return False
            if config.rod_status[i]:
                MyLogger.print(logger,logging.info.__name__,'range_rod_and_check',i+1)
                script.pick_rod_on_hand(i)
                # 可能滑口，等待1秒
                script.wait_random_time(2,0.5)
                if script.on_fish_check():
                    MyLogger.print(logger,logging.info.__name__,'range_rod_and_roll_line',i+1)
                    config.rod_status[i] = script.constant_roll(water_bottom_config.w_check_keep_all_fish,water_bottom_config.w_check_fishon_whith_shift,False)
                    MyLogger.print(logger,logging.info.__name__,'range_rod_and_roll_line_finish',i+1)
                    # 如果鱼竿状态正常，收完就进行下一次抛投
                    if config.rod_status[i] and not config.stop_signal:
                        script.wait_random_time(0.5,0.5)
                        config.rod_status[i] = script.base_rod_on_ground_throw(water_bottom_config.w_strength,water_bottom_config.w_check_isfull,water_bottom_config.w_throw_offset,True,water_bottom_config.w_wait_line_fly)
                MyLogger.print(logger,logging.info.__name__,'range_rod_and_put_on_ground',i+1)
                script.set_rod_on_ground()
                # 等待游戏反馈，避免过快的操作
                script.wait_random_time(1,0.5)
            else:
                MyLogger.print(logger,logging.info.__name__,'skip_erro_rod',i+1)
        config.range_rods_expend = time.time() - range_start_time
        # 遍历完毕，杆子状态可能更新，更新rod_staus
        # 检查是否至少有一根杆子可用
        if config.rod_status[0] or config.rod_status[1] or config.rod_status[2]:
            return True
        else:
            MyLogger.print(logger,logging.info.__name__,'rod_available_None')
            return False
                    


            
            