# -*- coding: utf-8 -*-
# 摘录自 luoye-hcl/go1-driver:unitree/go1/plugins/mt_state.py
# 仅为审核理解 odometry 卡如何产出返回值。以源仓库为准,不保证独立运行。

import math

from plugins.mt_base import MtStateCard


class OdometryCard(MtStateCard):
    """里程计(驱动增值卡):当前 position/yaw + 累计总路程 + 相对起点位移。
    起点默认取首帧,可用 reset_origin 动作重置。仅高层有 position(HIGHLEVEL)。"""
    CARD = "odometry"; CONTROL_LEVEL = "HIGHLEVEL"
    TOPIC = "state/odometry"; FMT = "data/json"; HZ = 5.0
    DESC = ("Go1 里程计 —— 当前 position/yaw、累计总路程 total_distance_m、相对起点位移 displacement"
            "(read 读取;reset_origin 重置起点)。让高层规划知道'走了多远/在哪'。")

    def __init__(self, cfg, namespace, bridge, ctrl):
        super().__init__(cfg, namespace, bridge, ctrl)
        self._origin = None    # [x, y] 起点;首次读或 reset_origin 时设

    # get_tool 用基类(只读、无执行按钮,与其它状态卡一致;reset_origin 仍可经 MCP 调用)

    def _payload(self):
        odo = self._ctrl.get_odometry()
        pos = odo.get("position_m", [0.0, 0.0, 0.0])
        if self._origin is None:
            self._origin = [pos[0], pos[1]]
        dx = pos[0] - self._origin[0]
        dy = pos[1] - self._origin[1]
        return {"position_m": pos, "yaw_rad": odo.get("yaw_rad", 0.0),
                "total_distance_m": odo.get("total_distance_m", 0.0),
                "origin_m": list(self._origin),
                "displacement_m": {"dx": round(dx, 3), "dy": round(dy, 3),
                                   "distance": round(math.hypot(dx, dy), 3)},
                "offline": odo.get("offline", False)}

    def dispatch(self, action, args):
        if action == "reset_origin":
            pos = self._ctrl.get_odometry().get("position_m", [0.0, 0.0, 0.0])
            self._origin = [pos[0], pos[1]]
            return self._ok("reset_origin", {"origin_m": list(self._origin)})
        return super().dispatch(action, args)

# 基类 _produce 会补 timestamp_ms / control_level,并在"连接但无新帧"时跳过发布(不伪造)。
# get_tool 声明 readOnly:true + topic_out /{ns}/state/odometry → core 只出数据流、不给执行按钮。
