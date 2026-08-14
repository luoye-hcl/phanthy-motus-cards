# -*- coding: utf-8 -*-
# 参考实现骨架 —— end_effector_pose
# 数据源 /mobile_manipulator/end_effector_pose（std_msgs/msg/Float32MultiArray）已在真机验证有数据，但驱动 robotera-q5-driver
# 尚未实现本插件。此文件为照 battery.py 模式的参考实现，待合入驱动后以源仓库为准。
# 本目录不含任何口令/密钥。

CARD = "end_effector_pose"
TYPE = "sensor"
TOPIC = "/{ns}/q5/end_effector_pose"
FMT = "data/json"
HZ = 1.0
NODE = "q5_end_effector_pose"
DESC = "Q5 末端执行器位姿：机械臂末端位置与姿态"
SOURCE_TOPIC = "/mobile_manipulator/end_effector_pose"


def build(snap: dict) -> dict:
    """由 Q5SdkClient 的 snapshot 组装本卡返回字段。"""
    import time
    data = {
        "timestamp_ms": int(time.time() * 1000),
        "fresh": bool(snap.get("fresh", False)),
        "available": bool(snap.get("available", False)),
        "source_topic": SOURCE_TOPIC,
    }
    # TODO: 订阅 /mobile_manipulator/end_effector_pose 后解析 msg，填充下方字段
    # data.update(...)
    return data


class Plugin:
    def __init__(self, plugin_config, namespace, executor, client):
        self._client = client
        self._topic = TOPIC.format(ns=namespace)

    def get_tool(self):
        return {
            "name": CARD, "type": TYPE, "multiInstance": False, "description": DESC,
            "inputSchema": {"type": "object", "properties": {
                "action": {"type": "string", "enum": ["info", "start", "stop"]},
            }, "required": ["action"], "additionalProperties": False},
        }

    def dispatch(self, action, args):
        if action in ("info", "read", "get", CARD):
            return {"state": "running", "data": build(self._client.snapshot())}
        if action == "start":
            return {"state": "running"}
        if action == "stop":
            return {"state": "idle"}
        return None


def make_plugin(plugin_config, namespace, executor, client):
    return Plugin(plugin_config, namespace, executor, client)
