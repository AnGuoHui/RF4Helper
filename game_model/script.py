###################################################################################
# 基础步骤 
# 1.使用几根杆子，开始时直接在默认按键下(1/2/3默认鱼竿存放位置，默认杆子已装备好，可使用状态,不会控制任务移动与视角转换)进行操作。
# 2.取出固定的杆子数量并丢出，插地。
###################################################################################

import logging
from typing import Tuple
import pyautogui
import time
from log.log_config import MyLogger
import operating_signal.operating_signal as op
import config.config as config
import random
import operating_signal.yolov10_match as float_signal

##########################################丢杆操作##################################

logger = logging.getLogger(__name__)

# 多杆初始操作--岸钓
def base_rods_step(rod_num=1,strength=0.8,isfull=False,close_wheel=True,wait_line_fly=1,wait_line_fly_offset=1,offset=0,r_rethrow_time=-1):
    for i in range(rod_num):
        can_throw_flg=True
        # 检查插地
        if rod_placement_check(i):
            if config.stop_signal:
                logger.debug("config.stop_signal has been updataed, func: base_rods_step stop")
                break
            # 再次拿出杆子
            pyautogui.press(str(i+1))
            MyLogger.print(logger,logging.info.__name__,'handel_rod',i+1)
            wait_random_time(1.5,0.2)
            # 按力度丢杆子  保存杆子状态
            can_throw_flg = base_throw_whith_rod_check(can_throw_flg,strength,isfull,offset,wait_line_fly,wait_line_fly_offset)
            config.rod_status[i] =can_throw_flg
            if r_rethrow_time > 0 and can_throw_flg:
                config.re_throw[i] = time.time()
            # 是否有线杯  关线杯
            if close_wheel and can_throw_flg:
                pyautogui.leftClick()
            # 插地
            pyautogui.press('0')
            time.sleep(0.5)
            # 向右移动,继续插后边的杆子
            if i!= rod_num-1:
                logger.debug("move right...")
                pyautogui.keyDown('d')
                time.sleep(0.3)
                pyautogui.keyUp('d')
                time.sleep(0.3)
        else:
            continue
    logger.debug("all rods have been thrown, rod_status:config.rod_status={}".format(config.rod_status))

# 多杆初始操作--船钓
def base_rods_step_on_boat(rod_num=1,strength=0.8,isfull=False,close_wheel=True,offset=0):
    for i in range(rod_num):
        can_throw_flg=True
        if config.stop_signal:
            logger.debug("config.stop_signal has been updataed, func: base_rods_step_on_boat stop")
            break
        # 拿出杆子
        pyautogui.press(str(i+1))
        MyLogger.print(logger,logging.info.__name__,'handel_rod',i+1)
        wait_random_time(1.5,0.2)
        # 按力度丢杆子  保存杆子状态
        can_throw_flg = base_throw_whith_rod_check(can_throw_flg,strength,isfull,offset)
        wait_random_time(1.5,0.2)
        config.rod_status[i] =can_throw_flg
        # 是否有线杯  关线杯
        if close_wheel and can_throw_flg:
            pyautogui.leftClick()
        # 插地
        pyautogui.press('0')
        # 记录抛投时间
        config.re_throw[i] = time.time()
        wait_random_time(1.5,0.2)
    logger.debug("all rods have been thrown, rod_status:config.rod_status={}".format(config.rod_status))


# 单杆初始操作  杆子不插地
def base_rod_single_step(strength=0.8,isfull=False,offset=0,wait_line_fly=0,wait_line_fly_offset=0):
    can_throw_flg=True
    pyautogui.press('1')
    wait_random_time(0.8,0.2)
    return base_throw_whith_rod_check(can_throw_flg,strength,isfull,offset,wait_line_fly,wait_line_fly_offset)

# 重复丢，杆子在手上
def base_rod_on_hand_throw(strength=0.8,isfull=False,offset=0,wait_line_fly=0,wait_line_fly_offset=0):
    can_throw_flg=True
    wait_random_time(0.1,0.2)
    return base_throw_whith_rod_check(can_throw_flg,strength,isfull,offset,wait_line_fly,wait_line_fly_offset)

# 重复丢，插地
def base_rod_on_ground_throw(strength=0.8,isfull=False,offset=0,close_wheel=True,wait_line_fly=0,wait_line_fly_offset=0):
    can_throw_flg=True
    wait_random_time(0.1,0.2)
    can_throw_flg = base_throw_whith_rod_check(can_throw_flg,strength,isfull,offset)
    # 等待饵入水
    wait_random_time(wait_line_fly,wait_line_fly_offset)
    # 是否有线杯  关线杯
    if close_wheel and can_throw_flg:
        pyautogui.leftClick()
    # 插地
    pyautogui.press('0')
    return can_throw_flg

##########################################收杆操作##################################
# 暂时不考率摩擦出线的问题  初始丢杆将摩擦开到理想位置  后续可以捕捉到出线动作和力度条状态再进行摩擦调整和锁轮操作

# 浮子钓具做钓与收线
def float_rod_roll(keep_all_fish=False,fishon_whith_shift=False,float_missing_count=3,rethrow_time = -1,is_racing_rod=False):
    # 这里浮标应该已经在水里了，在规定时间内检测浮标情况，确认浮标立直
    float_watched = True
    duration = 3
    start_time =time.time()
    while time.time() - start_time < duration and not config.stop_signal:
        if not float_signal.get_float_signal():
            MyLogger.print(logger,logging.info.__name__,'float_missing_wait')
            float_watched = False
        else:
            MyLogger.print(logger,logging.info.__name__,'float_found_continue')
            float_watched = True
            break
    # 在没超时的情况下监测到了浮标
    if not config.stop_signal and float_watched:
        # 忽略掉不重要的浮子信号
        time.sleep(1)
        # 对浮子消失的次数计数，超过计数重新抛投
        base_float_missing_count = 0
        rethrow_time_start = time.time()
        while base_float_missing_count<float_missing_count and not config.stop_signal:
            base_float_missing_count = float_moniter(keep_all_fish,fishon_whith_shift,base_float_missing_count,float_missing_count,rethrow_time,rethrow_time_start,is_racing_rod)
        # 当计数消耗完成时，准备下一次抛投，这里也有可能上鱼
        if not config.stop_signal and base_float_missing_count == float_missing_count:
            MyLogger.print(logger,logging.info.__name__,'rod_rethrow_out_of_missing_count')
            if is_racing_rod:
                    constant_roll(keep_all_fish,fishon_whith_shift,False)
            else:
                tenkara_roll_line_and_catch_fish(keep_all_fish,fishon_whith_shift)
        # 鱼杆状态检查  鱼竿异常  直接返回
        if not config.rod_is_ready or config.stop_signal:
            return False
        return True
    else:
        MyLogger.print(logger,logging.info.__name__,'rod_rethrow_out_of_wait_time')
        # 这里可能是未监测到浮标，也有可能是咬口，收线重抛
        if is_racing_rod:
            constant_roll(keep_all_fish,fishon_whith_shift,False)
        else:
            tenkara_roll_line_and_catch_fish(keep_all_fish,fishon_whith_shift)
         # 鱼杆状态检查  鱼竿异常  直接返回
        if not config.rod_is_ready or config.stop_signal:
            return False
        return True

# 浮子监控/收线/入户
def float_moniter(keep_all_fish=False,fishon_whith_shift=False,base_float_missing_count=0,float_missing_count=3,rethrow_time = -1,rethrow_time_start=0,is_racing_rod=False):
    base_float_missing_count += 1
    rethrow_flg = False
    # 等待浮标消失-咬口
    while float_signal.get_float_signal() and not config.stop_signal and not rethrow_flg:
        MyLogger.print(logger,logging.info.__name__,'float_bite_wait')
        if rethrow_time>0 and time.time()-rethrow_time_start>rethrow_time:
            MyLogger.print(logger,logging.info.__name__,'rod_rethrow_out_of_rethrow_conf')
            rethrow_flg = True
    # 退出以上循环的要求是咬口/手动停止/重新抛投定时到达
    if not config.stop_signal and not rethrow_flg:
        # 确认浮标消失，有真实的咬口情况发生
        wait_random_time(0.2,0.1)
        if not float_signal.get_float_signal():
            MyLogger.print(logger,logging.info.__name__,'float_missing_bite')
            # 确认浮标消失，收线并判断是否有鱼
            if is_racing_rod:
                constant_roll(keep_all_fish,fishon_whith_shift,False)
            else:
                tenkara_roll_line_and_catch_fish(keep_all_fish,fishon_whith_shift)
            # 开始下一次抛投，退出上层循环，避免收线之后base_float_missing_count与float_missing_count数一致，方便后续代码执行
            float_missing_count+=1
            return float_missing_count
        else:
            MyLogger.print(logger,logging.info.__name__,'float_re_show')
            return base_float_missing_count
    else:
        return float_missing_count

def mouse_control(func):
    def wrapper(*args, **kwargs):
        pyautogui.mouseDown(button='left')
        if config.force_roll:
            force_roll()
        rod_status = func(*args, **kwargs)
        pyautogui.mouseUp(button='left')
        return rod_status
    return wrapper

# 匀收/收线
@mouse_control
def constant_roll(keep_all_fish=False,fishon_whith_shift=False,is_lure = True):
    roll_flg=True
    has_keep_fish=False
    # 按下左键
    MyLogger.print(logger,logging.info.__name__,'constant_roll_start')
    # while循环来阻塞左键松开，持续收线
    while roll_flg and not config.stop_signal:
        MyLogger.print(logger,logging.info.__name__,'constant_roll_continue')
        # 完成收线/鱼竿状态变化  结束循环
        if op.get_rod_isok_signal() or not config.rod_is_ready:
            roll_flg=False
            break
        # 中鱼信号-刺鱼
        if op.get_onfish_signal():
            MyLogger.print(logger,logging.info.__name__,'fish_on')
            if fishon_whith_shift:
                # 加速收线
                pyautogui.keyDown('shift')
            # 阻塞  保持收线
            roll_flg,has_keep_fish = fishon_roll_monitor(keep_all_fish,fishon_whith_shift,is_lure)
            if fishon_whith_shift:
                # fishon_roll_monitor中收鱼需要放下shift键  这里取消重复操作
                if has_keep_fish:
                    break  
                # 加速收线结束
                pyautogui.keyUp('shift')
    MyLogger.print(logger,logging.info.__name__,'constant_roll_finish')
    # 鱼杆状态检查  鱼竿异常  直接返回
    if not config.rod_is_ready or config.stop_signal:
        return False
    # 在中鱼阶段把鱼刺上来了 直接返回
    if has_keep_fish:
        return True
    return roll_line_and_judge(keep_all_fish,False)

# 抽停收  todo 未考虑需要沉底的假饵抽停收的问题，如勺子沉底，软饵沉底情况
def dog_walk_roll(dog_walk_time=0.3,dog_walk_time_offset=0.2,keep_all_fish=False,fishon_whith_shift=False,dog_walk_wait_time = 0.3,dog_walk_wait_time_offset = 0.2,roll_last_line=False):
    roll_flg=True
    has_keep_fish=False
    # while循环来阻塞左键松开，持续收线
    MyLogger.print(logger,logging.info.__name__,'roll_stop_start')
    while roll_flg and not config.stop_signal:
        MyLogger.print(logger,logging.info.__name__,'roll_stop_continue')
        # 完成收线/鱼竿状态变化  结束循环
        if op.get_rod_isok_signal() or not config.rod_is_ready:
            roll_flg=False
            break
        # 中鱼信号-刺鱼并收线
        if op.get_onfish_signal():
            # 刺鱼
            # 收线 当鱼标志存在且线杯标志未归零之前，持续收线动作
            pyautogui.mouseDown(button='left')
            if fishon_whith_shift:
                # 加速收线
                pyautogui.keyDown('shift')
            # 阻塞  保持收线
            roll_flg,has_keep_fish = fishon_roll_monitor(keep_all_fish,True)
            pyautogui.mouseUp(button='left')
            if fishon_whith_shift:
                # fishon_roll_monitor中收鱼需要放下shift键  这里取消重复操作
                if has_keep_fish:
                    break
                pyautogui.keyUp('shift')
        else:
            # 抽停动作
            roll_line_with_shift(dog_walk_time,dog_walk_time_offset)
            # 抽停后监控中鱼情况  阻塞时长=time.time() - start_time < duration  监测not op.get_rod_isok_signal()信号避免抽停动作结束时正好收完线
            if dog_walk_wait_time_offset > 0:
                duration = random.uniform(dog_walk_wait_time,dog_walk_wait_time+dog_walk_wait_time_offset)
            else:
                duration = dog_walk_wait_time
            start_time = time.time()
            while time.time() - start_time < duration and not config.stop_signal and not op.get_onfish_signal() and not op.get_rod_isok_signal():
                MyLogger.print(logger,logging.info.__name__,'roll_stop_wait_next_roll')
            # 剩余线量不足，延长抽停时间，尽快完成收线
            if roll_last_line:
                if op.get_line_005_mark_signal() and not op.get_onfish_signal():
                    dog_walk_time *= 2
        # 在线杯容量不够的情况下可能会出现抽停后直接把小鱼收起来的情况，这里进行判断并进行处理
        # 在没有开启最后5米线检查的情况下，或者抽停时间设置过长，都有可能错过最后5米线的信号获取
        # 直接在整个抽停期间都进行入户判断
        if op.get_keepnet_mark_signal() and roll_flg:
            # 处理意外收起鱼的情况
            keep_fish_check(keep_all_fish)
            has_keep_fish = True
            roll_flg=False
    MyLogger.print(logger,logging.info.__name__,'roll_stop_finish')
    # 鱼杆状态检查
    if not config.rod_is_ready or config.stop_signal:
        return False
    # 在中鱼阶段把鱼刺上来了 直接返回
    if has_keep_fish:
        return True
    return roll_line_and_judge(keep_all_fish,True)

# 等待假饵到底，进行跳底前的准备动作
def wait_jump_shot_roll(func):
    def wrapper(wait_time = 1,wait_time_offset = 0.5,*args, **kwargs):
        # 等待假饵到底
        if time.time()-config.re_throw[kwargs.get('rod_number', 0)] > wait_time+wait_time_offset:
            # 开始跳底动作
            return func(*args, **kwargs)
        elif time.time()-config.re_throw[kwargs.get('rod_number', 0)] > wait_time and wait_time_offset > 0:
            # 添加偏移量后跳底
            time.sleep(random.uniform(0,wait_time_offset))
            return func(*args, **kwargs)
        else:
            watch = time.time()
            while time.time()-watch < 3 and not config.stop_signal:
                if op.get_onfish_signal():
                    MyLogger.print(logger,logging.info.__name__,'jump_shot_bite',kwargs.get('rod_number', 3))
                    # 饵下沉时中鱼
                    rod_status = constant_roll(kwargs.get('keep_all_fish', False),kwargs.get('fishon_whith_shift', False))
                    return rod_status,True
            return True,False
    return wrapper

# 跳底动作
@wait_jump_shot_roll
def jump_shot_roll(roll_line_time = 1,roll_line_time_offset = 0.5,roll_line_wait_time = 5,roll_line_wait_time_offset = 0.5,hold_time = 3,jump_shot_type = 0,keep_all_fish=False,fishon_whith_shift=False,rod_number = -1) -> Tuple[bool, bool]:
    MyLogger.print(logger,logging.info.__name__,'jump_shot_roll_start',hold_time)
    # 切杆等待时间
    hold_time_start = time.time()
    if rod_number >= 0:
        if jump_shot_type == 1 or jump_shot_type == 2:
            while time.time()-hold_time_start < hold_time and not config.stop_signal:
                # 跳底动作
                jump_shot(roll_line_time,roll_line_time_offset,jump_shot_type,rod_number)
                # 检测咬口情况
                whatch_time = time.time()
                while time.time()-hold_time_start < hold_time and time.time() - whatch_time  < random.uniform(roll_line_wait_time, roll_line_wait_time+roll_line_wait_time_offset) and not config.stop_signal:
                    if op.get_onfish_signal():
                        rod_status = constant_roll(keep_all_fish,fishon_whith_shift)
                        return rod_status,True
            return True,False
        elif jump_shot_type == 0:
            if op.get_onfish_signal():
                MyLogger.print(logger,logging.info.__name__,'befor_jump_shot_bite',rod_number+1)
                rod_status = constant_roll(keep_all_fish,fishon_whith_shift)
                return rod_status,True
            else:
                # 跳底动作        
                if time.time()-config.re_jump_shot[rod_number] > roll_line_wait_time+roll_line_wait_time_offset:
                    jump_shot(roll_line_time,roll_line_time_offset,jump_shot_type,rod_number)
                    # 记录跳底操作时间
                    config.re_jump_shot[rod_number] = time.time()
                else:
                    MyLogger.print(logger,logging.info.__name__,'jump_shot_skip')
                while time.time()-hold_time_start < hold_time and not config.stop_signal:
                    # 在饵下沉期间检测咬口情况
                    if op.get_onfish_signal():
                        MyLogger.print(logger,logging.info.__name__,'jump_shot_action_bite',rod_number+1)
                        rod_status = constant_roll(keep_all_fish,fishon_whith_shift)
                        return rod_status,True
            return True,False
        else:
            MyLogger.print(logger,logging.info.__name__,'jump_shot_type_erro')
            config.stop_signal = True
            return False,False
    else:
        MyLogger.print(logger,logging.info.__name__,'rod_available_None')
        config.stop_signal = True
        return False,False
            
def float_downstream_roll(rethrow_time,rethrow_time_offset,keep_all_fish=False,fishon_whith_shift=False) -> bool:
    while not config.stop_signal:
        if op.get_onfish_signal():
            MyLogger.print(logger,logging.info.__name__,'float_downstream_bite')
            return constant_roll(keep_all_fish,fishon_whith_shift)
        elif time.time()-config.re_throw[0] > rethrow_time+rethrow_time_offset:
            # 重新抛投
            MyLogger.print(logger,logging.info.__name__,'rod_rethrow_out_of_rethrow_conf')
            return constant_roll(keep_all_fish,fishon_whith_shift)
        else:
            # 等待下游浮标
            MyLogger.print(logger,logging.info.__name__,'float_downstream_wait_bite')
            time.sleep(random.uniform(0.5,0.5))
    return False


##########################################基础操作##################################

# 控制力度扔，左键按压持续时间来控制力度 offset偏移量控制可以为负数(左键按下持续时间偏移)，拟人操作，为0无偏移量
# 默认力度下，无偏移量设定，抛投力度51%  在饥饿状态也能达到此力度投掷
def mouse_click_and_hold(strength=0.8,offset=0):
    pyautogui.mouseDown(button='left')
    if offset > 0: 
        wait_random_time(strength,offset)
    elif offset < 0:
        if abs(offset) > strength:
            wait_random_time(strength,0)
            MyLogger.print(logger,logging.info.__name__,'offset_over_strength')
        else:
            wait_random_time(strength+offset,strength)
    else:
        time.sleep(strength)
    pyautogui.mouseUp(button='left')

# 全力扔
def full_strength_throw():
    pyautogui.keyDown('shift')
    pyautogui.mouseDown(button='left')
    wait_random_time(1,0.5)
    pyautogui.mouseUp(button='left')
    pyautogui.keyUp('shift')

# 刺鱼
def thornback():
    pyautogui.keyDown('ctrl')
    pyautogui.rightClick()
    pyautogui.keyUp('ctrl')

# 拿起指定的鱼竿
def pick_rod_on_hand(i):
    pyautogui.press(str(i+1))

# 插地
def set_rod_on_ground():
    pyautogui.press('0')

# 附带持续时间的加速收线-用于绞杆打状态-犬步或者其他抽停状态
def roll_line_with_shift(dog_walk_time=0.3,dog_walk_time_offset=0.2):
     pyautogui.keyDown('shift')
     pyautogui.mouseDown(button='left')
     if dog_walk_time_offset > 0:
        wait_random_time(dog_walk_time,dog_walk_time_offset)
     else:
         time.sleep(dog_walk_time)
     pyautogui.mouseUp(button='left')
     pyautogui.keyUp('shift')

# 非手竿抄鱼入户动作
def roll_line_and_catch_fish(keep_all_fish=False):
     MyLogger.print(logger,logging.info.__name__,'catch_fish_start')
     not_catch_fish=True
     delay_time = 1
    #  收线扬杆  直到鱼入户
     pyautogui.keyDown('shift')
     pyautogui.mouseDown(button='left')
     pyautogui.mouseDown(button='right')
     while not_catch_fish and not config.stop_signal:
        #  监测是否抄到鱼/鱼太小直接被收起来了
        if op.get_keepnet_mark_signal():
            not_catch_fish=False
            break
        #  伸出抄网
        pyautogui.press('space')
        # 尝试抄鱼，等待系统抄鱼响应。鱼的个体，杆子的角度，抬杆时鱼的动作，抄鱼时出线等都会影响抄鱼成功率，将抄鱼时长有限延长
        wait_random_time(delay_time,config.default_interval)
        #  收起抄网
        pyautogui.press('space')
        # 检查鱼竿状态  若鱼竿状态异常，则停止抄鱼动作
        if not config.rod_is_ready:
            not_catch_fish=False
        # 出现可抛投标志--脱钩  停止抄鱼动作
        if op.get_rod_isok_signal():
            not_catch_fish=False
        #  再次监测是否抄到鱼/鱼太小直接被收起来了
        if op.get_keepnet_mark_signal():
            not_catch_fish=False
            break
        # 等待下一次抄鱼尝试  保持收线--应对抄鱼时的出线，延后下一次伸抄网的时间，延长收线时间
        wait_random_time(delay_time,config.default_interval)
        if delay_time < 8:
            delay_time = delay_time*2
     pyautogui.mouseUp(button='left')
     pyautogui.mouseUp(button='right')
     pyautogui.keyUp('shift')
     MyLogger.print(logger,logging.info.__name__,'catch_fish_end')
    #  确实有入户信号
     if op.get_keepnet_mark_signal():
        keep_fish_check(keep_all_fish)

# 手竿收线与抄鱼入户动作
def tenkara_roll_line_and_catch_fish(keep_all_fish=False,fishon_whith_shift=False):
     MyLogger.print(logger,logging.info.__name__,'float_catch_fish_start')
     not_catch_fish=True
     delay_time = 1
    #  收线开始  直到鱼入户
    #  这里按shift是为了快速收线刺鱼-------
     pyautogui.keyDown('shift')
     pyautogui.mouseDown(button='left')
    #  阻塞一会，进行收线，判断有鱼信号，有鱼信号则开始抄鱼
     wait_random_time(0.5,0.3)
    #  这里按shift是为了快速收线刺鱼-------
     pyautogui.keyUp('shift')
     if fishon_whith_shift:
        pyautogui.keyDown('shift')
     if op.get_onfish_signal():
        first_try = True
        first_try = tenkara_try_catch_fish(not_catch_fish,delay_time,first_try)
        MyLogger.print(logger,logging.info.__name__,'float_catch_fish_first_try')
        if not first_try:
            # 尝试再次抄鱼
            MyLogger.print(logger,logging.info.__name__,'float_catch_fish_second_try')
            # 等待松线
            wait_random_time(0.8,0.2)
            pyautogui.mouseDown(button='left')
            tenkara_try_catch_fish(True,delay_time,first_try)
        if fishon_whith_shift:
            pyautogui.keyUp('shift')
        MyLogger.print(logger,logging.info.__name__,'float_catch_fish_end')
        #  确实有入户信号
        wait_random_time(0.5,0.3)
        if op.get_keepnet_mark_signal():
            keep_fish_check(keep_all_fish)
     else:
        MyLogger.print(logger,logging.info.__name__,'float_catch_fish_miss_fish_on_singl')
        #  收线
        while not op.get_rod_isok_signal() and not config.stop_signal:
            MyLogger.print(logger,logging.info.__name__,'wait_roll_line_finsh')
        pyautogui.mouseUp(button='left')
        if fishon_whith_shift:
            pyautogui.keyUp('shift')
        MyLogger.print(logger,logging.info.__name__,'float_catch_fish_end')

# 手竿提竿时，鱼太小，会出现抄不到鱼的情况，设置方法，放线再次尝试抄鱼
def tenkara_try_catch_fish(not_catch_fish = True,delay_time = 1,first_try = True):
    while not_catch_fish and not config.stop_signal:
            # 鱼竿状态变化  结束循环
            if op.get_rod_not_ready_signal():
                break
            #  监测是否抄到鱼/鱼太小直接被收起来了
            if op.get_keepnet_mark_signal():
                not_catch_fish=False
                break
            # 尝试抄鱼，等待系统抄鱼响应。鱼的个体，杆子的角度，抬杆时鱼的动作，抄鱼时出线等都会影响抄鱼成功率，将抄鱼时长有限延长
            if not_catch_fish:
                #  伸出抄网
                pyautogui.press('space')
                wait_random_time(delay_time,config.default_interval)
            # 检查鱼竿状态  若鱼竿状态异常，则停止抄鱼动作
            if not config.rod_is_ready:
                not_catch_fish=False
            # 出现可抛投标志--脱钩  停止抄鱼动作
            if op.get_rod_isok_signal():
                not_catch_fish=False
            #  再次监测是否抄到鱼/鱼太小直接被收起来了
            if op.get_keepnet_mark_signal():
                not_catch_fish=False
                break
            # 等待下一次抄鱼尝试  保持收线--应对抄鱼时的出线，延后下一次伸抄网的时间，延长收线时间
            if not_catch_fish:
                #  收起抄网
                pyautogui.press('space')
                wait_random_time(delay_time,config.default_interval)
                if delay_time < 8:
                    delay_time = delay_time*2
            # 多次抄鱼失败尝试之后，松线，再次尝试抄鱼,第二次抄鱼失败就阻塞在抄鱼循环里，等待手工介入
            if delay_time >= 8 and first_try and not_catch_fish:
                MyLogger.print(logger,logging.info.__name__,'float_catch_fish_first_try_fail')
                first_try=False
                not_catch_fish=False
                break
    pyautogui.mouseUp(button='left')
    return first_try       

# 完成收线时判断是否有鱼并进行后续操作
def roll_line_and_judge(keep_all_fish=False,press = False):
    MyLogger.print(logger,logging.info.__name__,'catch_fish_judge')
    # 意外把鱼收起来了，不进行阻塞会导致拿不到中鱼信号
    wait_random_time(0.2,0.1)
    # 检查有无加载画面
    while op.get_keepnet_loading_signal() and not config.stop_signal:
        MyLogger.print(logger,logging.info.__name__,'catch_fish_loding')
    # 判断是否有鱼
    if op.get_onfish_signal():
        # 收线拿抄网  鱼入户此次操作完成
        roll_line_and_catch_fish(keep_all_fish)
        return True
    elif op.get_keepnet_mark_signal():
        # 处理意外收起鱼的情况
        keep_fish_check(keep_all_fish)
        return True
    # 无鱼，结束
    # 所有的收线抄鱼动作已完成，检查鱼竿状态，状态正常则可以进行下一次丢操作，不正常，或者识别不到则将鱼竿插地
    elif op.get_rod_not_ready_signal():
        # 鱼竿状态异常,将鱼竿插地
        MyLogger.print(logger,logging.info.__name__,'rod_not_ready')
        pyautogui.press('0')
        return False
    # 无鱼且没有完成收线，也无异常状态，在沉底渔具/赛竿/博格尼亚收线完成准备抄鱼之前脱钩了，完成最后收线
    elif not op.get_rod_isok_signal():
        try_times = 1
        # 脱钩，继续收线
        MyLogger.print(logger,logging.info.__name__,'catch_fish_miss_fish_on_singl')
        # 按下右键确保抽停逻辑的异常退出能够完成最终收线
        if press:
            pyautogui.mouseDown(button='left')
        # 按下左键来确保中鱼信号因为光照意外丢失的情况下能获取到鱼
        pyautogui.mouseDown(button='right')
        while not op.get_rod_isok_signal() and not config.stop_signal:
            if op.get_keepnet_mark_signal():
                keep_fish_check(keep_all_fish)
            else:
                if try_times < 9:
                    MyLogger.print(logger,logging.info.__name__,'catch_fish_miss_fish_on_singl_wait_roll_line_finish')
                    wait_random_time(try_times,config.default_interval)
                    try_times += 1
                    # 尝试抄鱼
                    pyautogui.press('space')
                else:
                    MyLogger.print(logger,logging.info.__name__,'script_need_help')
                    wait_random_time(1,config.default_interval)              
        pyautogui.mouseUp(button='right')
        if press:
            pyautogui.mouseUp(button='left')
        wait_random_time(0.2,0.1)
        return True
    else:
        # 鱼竿状态正常，可以进行下一次丢操作,近距离脱钩可能导致丢操作获取鱼竿状态失败，这里阻塞一会
        wait_random_time(0.2,0.1)
        return True
    
# todo 断杆-渔轮损坏等情况暂未添加
def base_single_check():
    while not config.stop_signal:
        # 判断钓具是否完成组装-绞杆断线导致的饵丢失或者其他钓具未组装完成的情况
        if op.get_rod_not_ready_signal():
            config.rod_is_ready = False
        # 满护判断
        if not config.keepnet_100:
            config.keepnet_100 = op.get_keepnet_100_signal()
        # 鱼护容量预留判断
        if not config.keepnet_95:
            config.keepnet_95 = op.get_keepnet_95_signal()
        if op.get_disconnect_signal():
            MyLogger.print(logger,logging.info.__name__,'game_disconnect')
            config.stop_signal = True
        if op.get_choose_ticket_signal():
            MyLogger.print(logger,logging.info.__name__,'choose_ticket')
            config.stop_signal = True
        # 其他的情况待添加
        #########################
        time.sleep(config.check_interval)

# 检查最基础的元素，确认可以获取游戏画面截图
def base_check():
    return op.get_pople_helth_signal()

# 抛投前的检查，确认可以丢杆
def throw_check():
    return op.get_rod_isok_signal()

# 中鱼信号检查
def on_fish_check():
    return op.get_onfish_signal()

# 赛竿通过管轮卡信号检查来判断是否收线
def racing_roll_check():
    return op.get_line_limt_signal()

#中鱼之后的持续收线 
def fishon_roll_monitor(keep_all_fish = False,fishon_whith_shift = False,is_lure = True):
    # 阻塞  保持收线
    # get_onfish_signal上鱼信号  get_zero_line_with_fish_signal收线完成信号 config.stop_signal 手动介入信号
    # get_keepnet_mark_signal 入户信号(鱼太小，刺鱼刺上来了)  config.rod_is_ready  鱼竿状态（断线等鱼竿异常情况）
    # todo光照影响下的中鱼信号丢失，会导致外层循环退出，如果再次检查到有中鱼信号，会提前进入抄鱼步骤，暂未处理
    while op.get_onfish_signal() and not op.get_zero_line_with_fish_signal(is_lure) and not op.get_keepnet_mark_signal() and not config.stop_signal  and config.rod_is_ready:
        MyLogger.print(logger,logging.info.__name__,'continue_roll_line_with_fish')
        # 收线随机刺鱼
        if config.thornback_random > 0:
            if random.randint(1,100) < config.thornback_random:
                thornback()
        # 赛竿/伯格尼亚收线到5米内依然会有鱼咬口，线杯会显示为0米，循环退出失败，添加额外判断
        if not is_lure:
            if op.get_zero_line_with_fish_signal(not is_lure):
                MyLogger.print(logger,logging.info.__name__,'quit_roll_line_with_zero_line_bite')
                break
    MyLogger.print(logger,logging.info.__name__,'continue_roll_line_with_fish_finish')
    # 当退出中鱼后的收线阻塞，检查信号
    if not config.rod_is_ready:
         MyLogger.print(logger,logging.info.__name__,'rod_not_ready_do_nothing')
         return False,False
    elif not op.get_onfish_signal():
        #确认是否为脱钩
        # 等待游戏反馈-刺鱼上来了会有加载时间，游戏画面会模糊，网络差的情况会出线加载画面
        wait_random_time(1,0.1)
        # 检查有无加载画面
        while op.get_keepnet_loading_signal() and not config.stop_signal:
            MyLogger.print(logger,logging.info.__name__,'catch_fish_loding')
        if op.get_keepnet_mark_signal():
            MyLogger.print(logger,logging.info.__name__,'catch_fish_by_hook_set')
            # 松开shift
            if fishon_whith_shift:
                pyautogui.keyUp('shift')
            #  收鱼
            keep_fish_check(keep_all_fish)
            # 退出上层循环
            return False,True
        else:
            # 脱钩，继续收线
            MyLogger.print(logger,logging.info.__name__,'fish_unhook')
            return True,False
    else:
        # 当while循环结束时  一定在以上情况的发生下，应当退出上层循环
        return False,False

# 抛投基础检查
def base_throw_whith_rod_check(can_throw_flg,strength,isfull=False,offset=0,wait_line_fly=1,wait_line_fly_offset=0):
        # 检查抛投准备状态
    if not throw_check():
        MyLogger.print(logger,logging.info.__name__,'rod_not_ready_do_check')
        can_throw_flg = False
        return can_throw_flg
     # 按力度丢杆子
    if isfull:
        full_strength_throw()
    else:
        mouse_click_and_hold(strength,offset)
    wait_random_time(wait_line_fly,wait_line_fly_offset)
    return can_throw_flg

# 收鱼入户判断
def keep_fish_check(keep_all_fish = False):
    MyLogger.print(logger,logging.info.__name__,'keep_fish_start')
    # 满户判断
    if config.keepnet_100:
        pyautogui.press('backspace')
        MyLogger.print(logger,logging.info.__name__,'keepnet_full')
    else:
        if config.keepnet_95:
            # 判断渔获
            if op.get_rare_mark_signal() or op.get_rare_rare_mark_signal():
                pyautogui.press('space')
                MyLogger.print(logger,logging.info.__name__,'keepnet_add_rare_fish')
            else:
                pyautogui.press('backspace')
                MyLogger.print(logger,logging.info.__name__,'relese_normal_fish')
        else:
           keep_fish(keep_all_fish)
    MyLogger.print(logger,logging.info.__name__,'keep_fish_end')

# 收鱼入户动作
def keep_fish(keep_all_fish = False):
     # 入户或者丢弃
    if keep_all_fish:
        pyautogui.press('space')
    else:
        if op.get_qualified_mark_signal():
            pyautogui.press('space')
        else:
            pyautogui.press('backspace')

# 检查当前位置能否插地
def rod_placement_check(rodnum = -1):
    MyLogger.print(logger,logging.info.__name__,'rod_placement_check_start',rodnum+1)
    placement_check_result = True
    if rodnum >2 or rodnum < 0:
        MyLogger.print(logger,logging.info.__name__,'rod_number_erro')
        return not placement_check_result
    # 拿出杆子
    pyautogui.press(str(rodnum+1))
    wait_random_time(1,0.2)
    # 检查当前位置能否插地
    pyautogui.press('0')
    # 等待插地信号出现
    wait_random_time(1,0.2)
    if op.get_placement_erro_signal():
        # 再次拿出杆子
        pyautogui.press(str(rodnum+1))
        MyLogger.print(logger,logging.info.__name__,'rod_placement_fail_and_retry',rodnum+1)
        MyLogger.print(logger,logging.info.__name__,'move_back')
        pyautogui.keyDown('s')
        wait_random_time(0.2,0.1)
        pyautogui.keyUp('s')
        # 等待上次插地信号消失
        time.sleep(3)
        # 插地
        pyautogui.press('0')
        # 等待本次插地信号出现
        wait_random_time(1,0.2)
        if op.get_placement_erro_signal():
            MyLogger.print(logger,logging.info.__name__,'rod_placement_fail_and_mark_notready',rodnum+1)
            config.rod_status[rodnum] =False
            # 收起杆子  进行下一次循环
            pyautogui.press('backspace')
            placement_check_result = False
    MyLogger.print(logger,logging.info.__name__,'rod_placement_check_result',rodnum+1,placement_check_result)
    return placement_check_result

# 赛竿初始收线刺鱼动作
def force_roll() -> None:
    pyautogui.keyDown('shift')
    pyautogui.keyDown('ctrl')
    for i in range(3):
        pyautogui.click(button='right')
        if i == 2:
            pyautogui.keyUp('ctrl')
            pyautogui.keyUp('shift')
        time.sleep(0.5)
    
def jump_shot(roll_line_time = 1,roll_line_time_offset = 0.5,jump_shot_type = 0,rod_number = -1):
    if jump_shot_type == 2:
        MyLogger.print(logger,logging.info.__name__,'fource_jump_shot_start',rod_number)
        MyLogger.print(logger,logging.info.__name__,'jump_shot_whith_whell_open',rod_number,config.jump_shot_wheel_closed[rod_number])
        # 强抽跳底
        if not config.jump_shot_wheel_closed[rod_number]:
            MyLogger.print(logger,logging.info.__name__,'wheel_close',rod_number)
            time.sleep(0.2)
            pyautogui.click(button='left')
            config.jump_shot_wheel_closed[rod_number] = True
        pyautogui.keyDown('ctrl')
        time.sleep(0.2)
        pyautogui.click(button='right')
        pyautogui.keyUp('ctrl')
        MyLogger.print(logger,logging.info.__name__,'fource_jump_shot_end',rod_number)
    elif jump_shot_type == 1:
        MyLogger.print(logger,logging.info.__name__,'gentle_jump_shot_start',rod_number)
        MyLogger.print(logger,logging.info.__name__,'jump_shot_whith_whell_open',rod_number,config.jump_shot_wheel_closed[rod_number])
        # 抬杆跳底
        if not config.jump_shot_wheel_closed[rod_number]:
            MyLogger.print(logger,logging.info.__name__,'wheel_close',rod_number)
            time.sleep(0.2)
            pyautogui.click(button='left')
            config.jump_shot_wheel_closed[rod_number] = True
        time.sleep(0.2)
        pyautogui.mouseDown(button='right')
        wait_random_time(roll_line_time,roll_line_time_offset)
        pyautogui.mouseUp(button='right')
        MyLogger.print(logger,logging.info.__name__,'gentle_jump_shot_end',rod_number)
    elif jump_shot_type == 0:
        MyLogger.print(logger,logging.info.__name__,'roll_jump_shot_start',rod_number)
        # 收线跳底
        pyautogui.mouseDown(button='left')
        pyautogui.keyDown('shift')
        wait_random_time(roll_line_time,roll_line_time_offset)
        pyautogui.keyUp('shift')
        pyautogui.mouseUp(button='left') 
        # 打开线杯
        pyautogui.press('enter')
        MyLogger.print(logger,logging.info.__name__,'rool_jump_shot_end',rod_number)

# 循环单次按键操作--食物等
def loop_press_key(key,duration=100.0):
    now = time.time()
    while not config.stop_signal: 
        if time.time() - now > duration:
            pyautogui.press(key)
            now = time.time()
        else:
            time.sleep(2)

def do_crafting(crafting_total:int):
    has_crafted = 0
    crafting_fail = 0
    # 开始进行制作
    pyautogui.click(button='left')
    while not config.stop_signal:  
        if op.get_crafting_ok_signal():
            pyautogui.press('space')
            has_crafted += 1
            if crafting_total > has_crafted:
                MyLogger.print(logger,logging.info.__name__,'crafting_succ',has_crafted,crafting_total,crafting_fail)
                # 等待游戏响应,进行下一次制作
                wait_random_time(0.8,0.2)
                pyautogui.click(button='left')
            else:
                MyLogger.print(logger,logging.info.__name__,'crafting_end',has_crafted,crafting_total,crafting_fail)
                config.stop_signal = True
        elif op.get_crafting_fail_signal():
            pyautogui.press('space')
            has_crafted += 1
            crafting_fail += 1
            MyLogger.print(logger,logging.info.__name__,'crafting_fail',has_crafted,crafting_total,crafting_fail)
            # 等待游戏响应,进行下一次制作
            wait_random_time(0.8,0.2)
            pyautogui.click(button='left')
        elif op.get_crafting_missing_material_signal():
            MyLogger.print(logger,logging.info.__name__,'crafting_stop',has_crafted,crafting_total,crafting_fail)
            config.stop_signal = True
        else:
            MyLogger.print(logger,logging.info.__name__,'crafting_wait')
        wait_random_time(0.3,0.2)


#拟人/阻塞操作
def wait_random_time(start:float,offset:float) -> None:
    time.sleep(random.uniform(start, start+offset))