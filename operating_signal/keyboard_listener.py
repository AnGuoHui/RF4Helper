import logging
from pynput import keyboard
import config.config as config
import time

from log.log_config import MyLogger

logger = logging.getLogger(__name__)

def on_press(key):
    if key == keyboard.KeyCode.from_char('9') or key == keyboard.KeyCode.from_char('('):  # 如果按下 9 键则退出
        config.stop_signal = True  # 设置停止信号为 True
        MyLogger.print(logger,logging.info.__name__,'listen_stop_singl')
        return False  # 返回 False 会停止监听

# 启动键盘监听器的函数
def start_9_listener():
    MyLogger.print(logger,logging.info.__name__,'stop_singl_notice')
    with keyboard.Listener(on_press=on_press, on_release=None) as listener:
        # listener.join()  # 等待监听器结束
        while not config.stop_signal:  # 只要没有设置停止信号，就一直监听
            time.sleep(0.1)
        listener.stop()