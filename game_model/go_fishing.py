import logging
import time
import threading
import config.config as config
from game_model import script
from game_model.racing_fishing import RacingFishing
from game_model.lure_fishing import LureFishing
from game_model.water_bottom_fishing import WaterBottomFishing
import game_model.tenkara_fishing as tenkara_fishing
from log.log_config import MyLogger
import operating_signal.keyboard_listener as keyboard_listener
from window.variables import FishingConfig

logger = logging.getLogger(__name__)

def _go_fishing_decorator(func):
    def wrapper(*args, **kwargs):
        # 启动键盘监听器
        listener_thread = threading.Thread(target=keyboard_listener.start_9_listener)
        listener_thread.start()
        
        for i in reversed(range(9)):
            MyLogger.print(logger,logging.info.__name__,'gaming_check',i+1)
            if config.stop_signal:
                break
            time.sleep(1)

        # 检查视角是否在游戏中
        while not script.base_check() and not config.stop_signal:
            MyLogger.print(logger,logging.info.__name__,'waiting_for_game_single')
            time.sleep(1)
        
        # 食物/饮品使用
        if config.eat_interval > 0:
            MyLogger.print(logger,logging.info.__name__,'key_4_start_listening',config.eat_interval)
            eat_thread = threading.Thread(target=script.loop_press_key,args=("4",config.eat_interval))
            eat_thread.start()
        if config.drink_interval > 0:
            drink_thread = threading.Thread(target=script.loop_press_key,args=("5",config.drink_interval))
            drink_thread.start()

        func(*args, **kwargs)

        if 'eat_thread' in locals():
            eat_thread.join()
        if 'drink_thread' in locals():
            drink_thread.join()
        listener_thread.join()
        # 恢复初始配置
        _reset_default_config()
        MyLogger.print(logger,logging.info.__name__,'script_quit')
    return wrapper

@_go_fishing_decorator
def go_fishing(fishing_config:FishingConfig,switch_button_state:callable):

    logger,logging.debug('fishing_config:\n{}'.format(fishing_config))

    # 开始执行操作
    if not config.stop_signal:
        # 监控钓竿状态
        rode_status_thread = threading.Thread(target=script.base_single_check)
        rode_status_thread.start()
    
        if fishing_config.rod_type == "lure":
            lure = LureFishing()
            lure.fishing(fishing_config.lure_config)
        elif fishing_config.rod_type == "water_bottom":
            WaterBottom = WaterBottomFishing()
            WaterBottom.fishing(fishing_config.water_bottom_config)
        elif fishing_config.rod_type == "racing_rod":
            # logger.info("赛竿/伯格尼亚钓组必须预先设定管轮卡！！！")
            MyLogger.print(logger,logging.info.__name__,'match_and_bolognese_notice')
            config.force_roll = True
            racing = RacingFishing()
            racing.fishing(fishing_config.water_bottom_config)
        elif fishing_config.rod_type == "tenkara_rod":
            config.force_roll = fishing_config.tenkara_config.t_check_racing_rod
            tenkara = tenkara_fishing.TenkaraFishing()
            tenkara.fishing(fishing_config.tenkara_config)
        else:
            MyLogger.print(logger,logging.error.__name__,'unknown_rod_type')
         #等待线程结束
        rode_status_thread.join()
    else:
        MyLogger.print(logger,logging.error.__name__,'acc_stop_singl')
    # 恢复按钮状态
    switch_button_state(True)

# 重置默认配置
def _reset_default_config():
    # 恢复启动状态
    config.stop_signal = False
    # 杆子装配状态
    config.rod_is_ready = True
    # 多竿装配状态
    config.rod_status = [False, False,False]
    # 多竿重新抛投计时
    config.re_throw = [-1.0,-1.0,-1.0]
    # 双杆跳底
    config.re_jump_shot = [-1.0,-1.0]
    # 双杆跳底轮子关闭情况
    config.jump_shot_wheel_closed = [False,False]
    # 多竿操作计时
    config.range_rods_expend = 0.0
    # 满户
    config.keepnet_100 = False
    # 鱼护容量预留
    config.keepnet_95 = False
    # 赛竿强力刺鱼
    config.force_roll = False