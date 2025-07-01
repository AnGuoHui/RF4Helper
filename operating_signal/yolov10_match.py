import logging
import pyautogui
from ultralytics import YOLO
import cv2
import numpy as np
import sys
import os

logger = logging.getLogger(__name__)

if getattr(sys, 'frozen', False):
    # pyinstaller --noconsole --onefile --add-data "operating_signal\img_dir;img_dir" --add-data "operating_signal\best.pt;." main.py 
    current_directory = sys._MEIPASS
else:
    current_directory = os.path.dirname(__file__)

model_path = os.path.join(current_directory, "best.pt")

# 加载模型
model = YOLO(model_path)

# 判定当前是否有浮标，暂时不考虑多个浮标类别的问题
def get_float_signal():

    # 截取全屏并获取图片对象
    screenshot = pyautogui.screenshot()

    # 将截图转换为 NumPy 数组
    image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 调整图片大小
    resized_image = cv2.resize(image, (640, 480))

    # 识别浮标
    results = model(resized_image)

    # 检查结果是否为空
    if len(results) == 0 or len(results[0].boxes.data) == 0:
        logger.debug("get zero target from input...")
        return False
    else:
        # 设置初始的置信度，如果检查到多个目标，则取置信度最高的目标,小于0.4的目标不计入
        conf = 0.4
        # 打印所有检测到的对象信息
        for result in results:
            for detection in result.boxes.data:  # 或者 result.xyxy[0] 依赖于具体的实现
                x1, y1, x2, y2, confresult, cls = detection  # 获取边界框和置信度confresult、类别cls
                if conf < confresult:
                    conf = confresult
                logger.debug(f"target box : ({x1}, {y1}), ({x2}, {y2}); confresult: {confresult}; cls: {cls}")
        if conf <= 0.4:
            logger.debug("to low conf,target may not exist...")
            return False
        else:
            logger.debug(f"get targrt with conf: {conf}")
            return True
        # results[0].show()

if __name__ == '__main__':
    get_float_signal()