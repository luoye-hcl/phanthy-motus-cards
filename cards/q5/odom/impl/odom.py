# -*- coding: utf-8 -*-
# 参考实现骨架 —— odom
# 数据源 /wr1_base_drive_controller/odom（nav_msgs/msg/Odometry）已在真机验证有数据，但驱动 robotera-q5-driver
# 尚未实现本插件。此文件为照 battery.py 模式的参考实现，待合入驱动后以源仓库为准。
# 本目录不含任何口令/密钥。

CARD = "odom"
TYPE = "sensor"
TOPIC = "/{ns}/q5/odom"
FMT = "data/json"
HZ = 50.0
NODE = "q5_odom"
DESC = "Q5 里程计：底盘位置、姿态和速度"
SOURCE_TOPIC = "/wr1_base_drive_controller/odom"


def build(snap: dict) -> dict:
    """由 Q5SdkClient 的 snapshot 组装本卡返回字段。"""
    import time
    data = {
        "timestamp_ms": int(time.time() * 1000),
        "fresh": bool(snap.get("fresh", False)),
        "available": bool(snap.get("available", False)),
        "source_topic": SOURCE_TOPIC,
    }
    # TODO: 订阅 /wr1_base_drive_controller/odom 后解析 msg，填充下方字段
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
