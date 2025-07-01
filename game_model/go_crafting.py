import logging
import time
import threading
import config.config as config
from game_model import script
from log.log_config import MyLogger
from operating_signal import keyboard_listener

logger = logging.getLogger(__name__)

def _go_crafting_decorator(func):
    def wrapper(*args, **kwargs):
        # 启动键盘监听器
        listener_thread = threading.Thread(target=keyboard_listener.start_9_listener)
        listener_thread.start()
        
        for i in reversed(range(9)):
            MyLogger.print(logger,logging.info.__name__,'crafting_notice',i+1)
            if config.stop_signal:
                break
            time.sleep(1)

        func(*args, **kwargs)

        listener_thread.join()
        MyLogger.print(logger,logging.info.__name__,'script_quit')
    return wrapper

@_go_crafting_decorator
def go_crafting(crafting_total:int,switch_button_state:callable):
    if crafting_total > 0:
        script.do_crafting(crafting_total)
    else:
        MyLogger.print(logger,logging.error.__name__,'crafting_total_notice')

    # 恢复按钮状态
    switch_button_state(True)
    # 恢复启动状态
    config.stop_signal = False