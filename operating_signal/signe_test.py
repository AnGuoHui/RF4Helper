
import time

import cv2
import numpy as np
import pyautogui



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
        # cv2.moveWindow('Matched Image', 500, 500)
        # cv2.waitKey(10000)  # 等待按键
        # cv2.destroyAllWindows()  # 关闭所有OpenCV窗口

        # 返回比对结果
        return True
    else:
        return False
    
time.sleep(3) # 等待1秒
res = match_result(r'C:\code\rf4helper\operating_signal\static\cn\rare_mark.png',0.96)
print(res)