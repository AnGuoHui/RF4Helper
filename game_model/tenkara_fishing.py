import logging
from game_model.base_fishing import BaseFishing
import game_model.script  as script
import config.config as config

from window.variables import TenkaraConfig
from log.log_config import MyLogger

logger = logging.getLogger(__name__)

class TenkaraFishing(BaseFishing):

    def fishing(self,tenkara_conf:TenkaraConfig) -> None:
        self._tenkara_fishing(tenkara_conf)

    # 手竿  当前只支持单竿
    def _tenkara_fishing(self,tenkara_conf:TenkaraConfig) -> None:
        rod_staus = False
        # 拿出杆子并抛投
        if not config.stop_signal:
            rod_staus =script.base_rod_single_step(tenkara_conf.t_strength,tenkara_conf.t_check_isfull,tenkara_conf.t_throw_offset,tenkara_conf.t_wait_time,tenkara_conf.t_wait_time_offset)
        # 重复的丢  收操作
        while rod_staus and not config.stop_signal:
            rod_staus = script.float_rod_roll(tenkara_conf.t_check_keep_all_fish,tenkara_conf.t_check_fishon_whith_shift,5,tenkara_conf.t_rethrow_time,tenkara_conf.t_check_racing_rod)
            MyLogger.print(logger,logging.info.__name__,'float_complete')
            # 如果鱼竿状态正常，收完就进行下一次抛投
            if rod_staus and not config.stop_signal:
                script.wait_random_time(0.5,0.5)
                rod_staus = script.base_rod_on_hand_throw(tenkara_conf.t_strength,tenkara_conf.t_check_isfull,tenkara_conf.t_throw_offset,tenkara_conf.t_wait_time,tenkara_conf.t_wait_time_offset)
        config.stop_signal = True