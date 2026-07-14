# -*- coding: utf-8 -*-
# 摘录自 luoye-hcl/go1-driver:unitree/go1/plugins/mt_state.py
# 仅为审核理解 feet 卡如何产出返回值。以源仓库为准,不保证独立运行。

from plugins.mt_base import MtStateCard, now_ms
from go1_ctrl import FEET_ORDER   # ["FR", "FL", "RR", "RL"]


class FeetCard(MtStateCard):
    CARD = "feet"; CONTROL_LEVEL = "ANY"
    TOPIC = "state/feet"; FMT = "data/json"; HZ = 10.0
    DESC = "Go1 足端 —— 足底力原始值(高层控制时另有足端相对机身的位置/速度)。"

    def _payload(self):
        s = self._ctrl.get_state()
        out = {"order": FEET_ORDER, "foot_force_raw": s.get("foot_force_raw", [0, 0, 0, 0])}
        # 足端相对机身位置/速度仅高层提供(MT §6.4)
        if "foot_position_to_body" in s:
            out["position_to_body"] = s["foot_position_to_body"]
            out["speed_to_body"] = s.get("foot_speed_to_body", [])
        return out


# ── 依赖的基类关键方法(摘录自 plugins/mt_base.py:MtStateCard) ──────────────────
#
# def _produce(self):
#     # 连接态但无新包 → 不伪造时间戳,跳过本次发布(MT §3.2)
#     if self._ctrl.is_connected() and not self._ctrl.state_fresh():
#         return None
#     d = self._payload()
#     if d is None:
#         return None
#     d = dict(d)
#     d["timestamp_ms"] = now_ms()
#     d["control_level"] = self._ctrl.control_level
#     return d
#
# def get_tool(self):
#     # 纯状态卡:只出数据流(topic_out),不暴露可执行 action → core 不渲染"执行"按钮
#     return {
#         "name": self.CARD, "type": "sensor", "multiInstance": False,
#         "readOnly": True,
#         "description": self.DESC,
#         "inputSchema": {"type": "object", "properties": {}},
#         "topic_out": [{"topic": self._topic, "format": self.FMT}],
#     }
