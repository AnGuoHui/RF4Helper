# 操作信号，通过游戏画面的反馈来判断如何操作，画面截图不进行是否为最新判定

import logging
import sys
import cv2
import numpy as np
import os
import pyautogui
import config.config as config

logger = logging.getLogger(__name__)

if getattr(sys, 'frozen', False):
    # pyinstaller --noconsole --onefile --add-data "operating_signal\img_dir;img_dir" main.py 
    current_directory = sys._MEIPASS
else:
    current_directory = os.path.dirname(__file__)

def get_current_directory_by_language() -> str:
    if config.ui_language:
        return 'static\cn'
    else:
        return 'static\en'
    
# 中鱼标志
fishon = os.path.join(current_directory, 'static\common', 'fishon.png')
# 管轮卡标志
line_limt = os.path.join(current_directory, 'static\common', 'line_limt.png')
# 收完线杯标志
zero_line = os.path.join(current_directory, 'static\common', 'zero_line.png')
# 有鱼收完线杯标志
zero_line_with_fish = os.path.join(current_directory, 'static\common', 'zero_line_with_fish.png')
# 线杯外剩余线量5米标志
line_005 = os.path.join(current_directory, 'static\common', 'line_005.png')
# 可抛投标志
rod_isok = os.path.join(current_directory, get_current_directory_by_language(), 'rod_isok.png')
# 达标标志
qualified_mark = os.path.join(current_directory, 'static\common', 'qualified_mark.png')
# 入户标志
keepnet_mark = os.path.join(current_directory, get_current_directory_by_language(), 'keepnet_mark.png')
# 入户加载-网络情况差的时候会出现
keepnet_loading = os.path.join(current_directory, get_current_directory_by_language(), 'keepnet_loading.png')
# 设备未组装标志
rod_not_ready = os.path.join(current_directory, get_current_directory_by_language(), 'rod_not_ready.png')
# 人物健康状态标志，用来确定视角在游戏中
pople_helth  = os.path.join(current_directory, 'static\common', 'pople_helth.png')
# 满户标志
keepnet_100 = os.path.join(current_directory, 'static\common', 'keepnet_100.png')
# 满户预留标志
keepnet_95 = os.path.join(current_directory, 'static\common', 'keepnet_95.png')
# 普通稀有标志
rare_mark = os.path.join(current_directory, 'static\common', 'rare_mark.png')
# 普通稀有标志
rare_rare_mark = os.path.join(current_directory, 'static\common', 'rare_rare_mark.png')
# 插地失败标志
placement_erro_0 = os.path.join(current_directory, get_current_directory_by_language(), 'placement_erro_0.png')
placement_erro_1 = os.path.join(current_directory, get_current_directory_by_language(), 'placement_erro_1.png')
# 断开连接标志
disconnect_mark = os.path.join(current_directory, get_current_directory_by_language(), 'disconnect_mark.png')
# 选择船票
choose_ticket = os.path.join(current_directory, get_current_directory_by_language(), 'choose_ticket.png')
# 制作完成标志
crafting_ok = os.path.join(current_directory, get_current_directory_by_language(), 'crafting_ok.png')
# 制作失败标志
crafting_fail = os.path.join(current_directory, get_current_directory_by_language(), 'crafting_fail.png')
# 制作缺失材料标志
crafting_missing_material = os.path.join(current_directory, get_current_directory_by_language(), 'crafting_missing_material.png')

change_path_with_language = {
    'rod_isok':rod_isok,
    'keepnet_mark':keepnet_mark,
    'keepnet_loading':keepnet_loading,
    'rod_not_ready':rod_not_ready,
    'placement_erro_0':placement_erro_0,
    'placement_erro_1':placement_erro_1,
    'disconnect_mark':disconnect_mark,
    'choose_ticket':choose_ticket,
    'crafting_ok':crafting_ok,
    'crafting_fail':crafting_fail,
    'crafting_missing_material':crafting_missing_material,
}

def update_file_path():
    change_path_with_language['rod_isok'] = os.path.join(current_directory, get_current_directory_by_language(), 'rod_isok.png')
    change_path_with_language['keepnet_mark'] = os.path.join(current_directory, get_current_directory_by_language(), 'keepnet_mark.png')
    change_path_with_language['keepnet_loading'] = os.path.join(current_directory, get_current_directory_by_language(), 'keepnet_loading.png')
    change_path_with_language['rod_not_ready'] = os.path.join(current_directory, get_current_directory_by_language(), 'rod_not_ready.png')
    change_path_with_language['placement_erro_0'] = os.path.join(current_directory, get_current_directory_by_language(), 'placement_erro_0.png')
    change_path_with_language['placement_erro_1'] = os.path.join(current_directory, get_current_directory_by_language(), 'placement_erro_1.png')
    change_path_with_language['disconnect_mark'] = os.path.join(current_directory, get_current_directory_by_language(), 'disconnect_mark.png')
    change_path_with_language['choose_ticket'] = os.path.join(current_directory, get_current_directory_by_language(), 'choose_ticket.png')
    change_path_with_language['crafting_ok'] = os.path.join(current_directory, get_current_directory_by_language(), 'crafting_ok.png')
    change_path_with_language['crafting_fail'] = os.path.join(current_directory, get_current_directory_by_language(), 'crafting_fail.png')
    change_path_with_language['crafting_missing_material'] = os.path.join(current_directory, get_current_directory_by_language(), 'crafting_missing_material.png')

# 画面反馈匹配 默认匹配阈值0.8 比对中鱼等画面状态变化
def match_result(template_path, threshold=0.8):
    # 读取待检测的图片和模板
    # image = cv2.imread(os.getcwd()+'\\img_dir\\screeshot\\screenshot.png')#屏幕截图

    # 截取全屏并获取图片对象
    screenshot = pyautogui.screenshot()
    # 将 screenshot 转换为 NumPy 数组 (可选)
    screenshot_np = np.array(screenshot)
    # 转换为 BGR 格式（OpenCV 默认的颜色格式）
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    template = cv2.imread(template_path)

    # 转换为灰度图
    image_gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 执行模板匹配
    # result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    result = cv2.matchTemplate(image_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= threshold)

    if loc[0].size > 0:
        # 返回比对结果
        return True
    else:
        return False
    
def match_result_binary(template_path, threshold=0.8 ,thresh = 230):
    # 截取全屏并获取图片对象
    screenshot = pyautogui.screenshot()
    # 将 screenshot 转换为 NumPy 数组 (可选)
    screenshot_np = np.array(screenshot)
    # 转换为 BGR 格式（OpenCV 默认的颜色格式）
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    template = cv2.imread(template_path)

    # 转换为灰度图
    image_gray = cv2.cvtColor(screenshot_bgr, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    
    # 二值化图像
    _, image_binary = cv2.threshold(image_gray, thresh, 255, cv2.THRESH_BINARY)
    _, template_binary = cv2.threshold(template_gray, thresh, 255, cv2.THRESH_BINARY)

    # 执行模板匹配
    result = cv2.matchTemplate(image_binary, template_binary, cv2.TM_CCOEFF_NORMED)

    loc = np.where(result >= threshold)

    

    if loc[0].size > 0:
        # h, w = template_binary.shape
        # for pt in zip(*loc[::-1]):  # 将匹配位置转为(x, y)格式
        #     cv2.rectangle(screenshot_bgr, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)  # 绘制绿色矩形框
        
        # cv2.imshow('Matched Image', screenshot_bgr)
        # # cv2.moveWindow('Matched Image', 500, 500)
        # cv2.waitKey(0)  # 等待按键
        # cv2.destroyAllWindows()  # 关闭所有OpenCV窗口

        # 返回比对结果
        return True
    else:
        return False
    
    

# 上鱼/脱钩信号
def get_onfish_signal():
    result = match_result(fishon)
    logger.debug('get_onfish_signal=%s',result)
    return result

# 管轮卡信号
def get_line_limt_signal():
    result = match_result_binary(line_limt,0.8,128)
    logger.debug('get_line_limt_signal=%s',result)
    return result

# 收线信号
def get_zero_line_signal():
    is_zero_line = match_result_binary(zero_line,0.99)
    logger.debug('is_zero_line=%s',is_zero_line)
    return is_zero_line

def get_zero_line_with_fish_signal(is_lure = True):
    if is_lure:
        is_zero_line_with_fish = match_result_binary(zero_line_with_fish,0.987)
        logger.debug('lure---zero_line_with_fish=%s',is_zero_line_with_fish)
    else:
        is_zero_line_with_fish = match_result_binary(line_005,0.987)
        logger.debug('bottom---zero_line_with_fish=%s',is_zero_line_with_fish)
    return is_zero_line_with_fish

# 可抛投信号
def get_rod_isok_signal():
    result = match_result(change_path_with_language['rod_isok'])
    logger.debug('get_rod_isok_signal=%s',result)
    return result

# 达标信号
def get_qualified_mark_signal():
    result = match_result(qualified_mark,0.91)
    logger.debug('get_qualified_mark_signal=%s',result)
    return result

# 抄到鱼信号
def get_keepnet_mark_signal():
    result = match_result(change_path_with_language['keepnet_mark'])
    logger.debug('get_keepnet_mark_signal=%s',result)
    return result

# 设备未组装信号
def get_rod_not_ready_signal():
    result = match_result(change_path_with_language['rod_not_ready'])
    logger.debug('get_rod_not_ready_signal=%s',result)
    return result

# 检查人物健康状态-确认存在游戏画面
def get_pople_helth_signal():
    result = match_result(pople_helth)
    logger.debug('get_pople_helth_signal=%s',result)
    return result

# 满户标志  后续钓获全部放生
def get_keepnet_100_signal():
    result = match_result(keepnet_100,0.96)
    logger.debug('get_keepnet_100_signal=%s',result)
    return result

# 满户预留标志  后续渔获只保留稀有鱼超级稀有鱼
def get_keepnet_95_signal():
    result = match_result(keepnet_95,0.96)
    logger.debug('get_keepnet_95_signal=%s',result)
    return result

# 稀有鱼标志
def get_rare_mark_signal():
    result = match_result(rare_mark,0.95)
    logger.debug('get_rare_mark_signal=%s',result)
    return result

# 超级稀有鱼标志
def get_rare_rare_mark_signal():
    result = match_result(rare_rare_mark,0.95)
    logger.debug('get_rare_rare_mark_signal=%s',result)
    return result

# 线杯外剩余线量5米标志
def get_line_005_mark_signal():
    result = match_result(line_005,0.9)
    logger.debug('get_line_005_mark_signal=%s',result)
    return result

# 插地失败标志
def get_placement_erro_signal():
    result_0 = match_result(change_path_with_language['placement_erro_0'])
    logger.debug('get_placement_erro_signal result_0=%s',result_0)
    result_1 = match_result(change_path_with_language['placement_erro_1'])
    logger.debug('get_placement_erro_signal result_1=%s',result_1)
    return result_0 and result_1

# 加载图标
def get_keepnet_loading_signal():
    result = match_result(change_path_with_language['keepnet_loading'])
    logger.debug('get_keepnet_loading_signal=%s',result)
    return result

#断开连接信号 
def get_disconnect_signal():
    result = match_result(change_path_with_language['disconnect_mark'])
    logger.debug('get_disconnect_signal=%s',result)
    return result

#船票到期 
def get_choose_ticket_signal():
    result = match_result(change_path_with_language['choose_ticket'])
    logger.debug('get_choose_ticket_signal=%s',result)
    return result

# 制作完成
def get_crafting_ok_signal():
    result = match_result(change_path_with_language['crafting_ok'])
    logger.debug('get_crafting_ok_signal=%s',result)
    return result

# 制作失败
def get_crafting_fail_signal():
    result = match_result(change_path_with_language['crafting_fail'])
    logger.debug('get_crafting_fail_signal=%s',result)
    return result

# 制作缺失材料
def get_crafting_missing_material_signal():
    result = match_result(change_path_with_language['crafting_missing_material'])
    logger.debug('get_crafting_missing_material_signal=%s',result)
    return result 