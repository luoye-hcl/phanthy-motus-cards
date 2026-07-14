# -*- coding: utf-8 -*-
# 摘录自 luoye-hcl/go1-driver:unitree/go1/plugins/mt_state.py
# 仅为审核理解 loco_state 卡如何产出返回值。以源仓库为准,不保证独立运行。

from plugins.mt_base import MtStateCard
from go1_ctrl import MODE_NAMES, GAIT_NAMES


class LocoStateCard(MtStateCard):
    CARD = "loco_state"; CONTROL_LEVEL = "HIGHLEVEL"
    TOPIC = "loco/state"; FMT = "data/json"; HZ = 10.0
    DESC = "Go1 运动状态 —— 模式/步态/里程/速度/机身高度。10Hz。"

    def _payload(self):
        s = self._ctrl.get_high_state()
        vel = s.get("velocity", [0.0, 0.0, 0.0])
        return {
            "mode": s.get("mode", 0), "mode_name": MODE_NAMES.get(s.get("mode", 0), "unknown"),
            "gait_type": s.get("gait_type", 0), "gait_name": GAIT_NAMES.get(s.get("gait_type", 0), "unknown"),
            "foot_raise_height_m": s.get("foot_raise_height_m", 0.0),
            "position_m": s.get("position_m", [0.0, 0.0, 0.0]),
            "body_height_m": s.get("body_height_m", 0.0),
            "velocity_body_mps": {"forward": vel[0] if len(vel) > 0 else 0.0,
                                  "lateral": vel[1] if len(vel) > 1 else 0.0},
            # 官方 velocity[2] 语义与独立 yawSpeed 冲突 → 只保留原始值,不命名(MT §6.1)
            "velocity_index_2_raw": vel[2] if len(vel) > 2 else 0.0,
            "yaw_speed_rad_s": s.get("yaw_speed_rad_s", 0.0),
        }

# 基类 _produce 补 timestamp_ms / control_level,并在"连接但无新帧"时跳过发布(不伪造)。
# get_tool 声明 readOnly:true + topic_out /{ns}/loco/state → core 只出数据流、不给执行按钮。
