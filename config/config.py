import logging

# 启停信号  
stop_signal = False
# 杆子装配状态,断线/断杆都会导致杆子状态异常,需要进行监控已中断正在执行的操作
rod_is_ready = True
# 多杆装配状态
rod_status = [False, False,False]
# 多竿重新抛投
re_throw = [-1.0,-1.0,-1.0]
# 双竿跳底
re_jump_shot = [-1.0,-1.0]
# 双杆跳底轮子关闭情况
jump_shot_wheel_closed = [False,False]
# 多竿操作消耗时间
range_rods_expend = 0.0
# 满户
keepnet_100 = False
# 鱼护容量预留，后续只入户稀有鱼
keepnet_95 = False
# 赛竿强力刺鱼
force_roll = False
# 状态检查间隔 默认0.2秒检查一次,重设时应>0
check_interval = 0.2
# 食用间隔
eat_interval = 0.0
# 饮用间隔
drink_interval = 0.0
# 随机刺鱼参数，范围为1-100，越大刺鱼越多，0为不刺鱼
thornback_random = 20.0
# 默认获取屏幕截图时间间隔，单位秒,重设时应>0
default_interval = 0.2
# 日志输出等级
log_level = logging.DEBUG
# ui界面语言 1-CN(default) 0-EN
ui_language = 1
# 折叠ui界面
attributes = True