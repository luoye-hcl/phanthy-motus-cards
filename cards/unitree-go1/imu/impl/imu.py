# -*- coding: utf-8 -*-
# 摘录自 luoye-hcl/go1-driver:unitree/go1/plugins/mt_state.py
# 仅为审核理解 imu 卡如何产出返回值。以源仓库为准,不保证独立运行。

from plugins.mt_base import MtStateCard


class ImuCard(MtStateCard):
    CARD = "imu"; CONTROL_LEVEL = "ANY"
    TOPIC = "state/imu"; FMT = "data/json"; HZ = 20.0
    DESC = "Go1 IMU —— 四元数(wxyz)/角速度/加速度/欧拉角/温度。20Hz。"

    def _payload(self):
        imu = self._ctrl.get_state().get("imu", {})
        d = dict(imu)
        d["attitude_may_drift"] = True   # 加速运动时姿态漂移,提示上层(MT §6.2)
        return d

# 基类 _produce 会补 timestamp_ms / control_level,并在"连接但无新帧"时跳过发布(不伪造)。
# get_tool 声明 readOnly:true + topic_out /{ns}/state/imu → core 只出数据流、不给执行按钮。
