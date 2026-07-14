# -*- coding: utf-8 -*-
# 摘录自 luoye-hcl/go1-driver:unitree/go1/plugins/mt_state.py
# 仅为审核理解 fall_alarm 卡如何产出返回值。以源仓库为准,不保证独立运行。

import math

from plugins.mt_base import MtStateCard


class FallAlarmCard(MtStateCard):
    """跌倒/侧翻告警(驱动增值卡,非 MT 14 卡之一):由 IMU 的 roll/pitch 幅度判定
    ok/tilted/fallen,给运动安全兜底。阈值可 config(tilt_warn_rad/fall_rad)。
    依赖 IMU 帧,连接后无新帧则按 NO_FEEDBACK 抑制(不误报)。"""
    CARD = "fall_alarm"; CONTROL_LEVEL = "ANY"
    TOPIC = "state/fall_alarm"; FMT = "data/json"; HZ = 10.0
    DESC = "Go1 跌倒/侧翻告警 —— 由 IMU 的 roll/pitch 幅度判定 ok/tilted/fallen + 倾角。10Hz。"

    def _payload(self):
        imu = self._ctrl.get_state().get("imu", {})
        rpy = imu.get("rpy_rad", [0.0, 0.0, 0.0]) or [0.0, 0.0, 0.0]
        roll = float(rpy[0]) if len(rpy) > 0 else 0.0
        pitch = float(rpy[1]) if len(rpy) > 1 else 0.0
        warn = float(self._cfg.get("tilt_warn_rad", 0.6))   # ≈34°
        fall = float(self._cfg.get("fall_rad", 1.2))        # ≈69°
        tilt = max(abs(roll), abs(pitch))
        if tilt >= fall:
            status, hint = "fallen", "已跌倒/翻倒 —— 立即停止运动,需人工扶正后再操作"
        elif tilt >= warn:
            status, hint = "tilted", "机身明显倾斜 —— 谨慎,可能即将失稳"
        else:
            status, hint = "ok", "姿态正常"
        return {"status": status, "roll_rad": round(roll, 4), "pitch_rad": round(pitch, 4),
                "roll_deg": round(math.degrees(roll), 1), "pitch_deg": round(math.degrees(pitch), 1),
                "tilt_warn_rad": warn, "fall_rad": fall, "hint": hint}

# 基类 _produce 会补 timestamp_ms / control_level,并在"连接但无新帧"时跳过发布(不伪造)。
# get_tool 声明 readOnly:true + topic_out /{ns}/state/fall_alarm → core 只出数据流、不给执行按钮。
