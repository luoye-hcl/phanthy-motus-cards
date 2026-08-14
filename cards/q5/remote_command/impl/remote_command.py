# -*- coding: utf-8 -*-
# remote_command —— Q5 遥控指令 (sensor_msgs/msg/Joy)
# 自建 ROS2 Node 订阅 /send_remote/command，解析 axes + buttons。
# 照 cpu_freq.py 模式：插件自己管 Node/订阅/发布，不依赖 q5_sdk_client。

from __future__ import annotations

import json
import time

from sensor_contract import topic_out

try:
    from rclpy.node import Node
    from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
    from sensor_msgs.msg import Joy
    from std_msgs.msg import String

    _HAS_ROS2 = True
    _QOS = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                      history=HistoryPolicy.KEEP_LAST, depth=1,
                      durability=DurabilityPolicy.VOLATILE)
except Exception:
    _HAS_ROS2 = False

CARD = "remote_command"
TYPE = "sensor"
SOURCE_TOPIC = "/send_remote/command"
TOPIC = "/{ns}/q5/remote_command"
FMT = "data/json"
HZ = 2.0
NODE = "q5_remote_command"
DESC = "Q5 遥控指令：手柄按键(buttons)与摇杆(axes)输入"


def build(msg, received_at_ms) -> dict:
    now_ms = int(time.time() * 1000)
    if msg is None:
        return {"timestamp_ms": now_ms, "received_at_ms": received_at_ms,
                "fresh": False, "available": False, "source_topic": SOURCE_TOPIC,
                "message": "未收到遥控指令消息"}
    age_ms = None if received_at_ms is None else now_ms - received_at_ms
    fresh = age_ms is not None and age_ms <= 5000
    return {"timestamp_ms": now_ms, "received_at_ms": received_at_ms,
            "age_ms": age_ms, "fresh": fresh,
            "available": True,
            "axes": [float(a) for a in (msg.axes or [])],
            "buttons": [int(b) for b in (msg.buttons or [])],
            "source_topic": SOURCE_TOPIC}


class Plugin:
    def __init__(self, plugin_config, namespace, executor, client):
        self._topic = TOPIC.format(ns=namespace)
        self._node = None
        self._pub = None
        self._last_msg = None
        self._received_at_ms = None
        if _HAS_ROS2 and executor is not None:
            try:
                self._node = Node(NODE)
                self._pub = self._node.create_publisher(String, self._topic, _QOS)
                self._node.create_subscription(Joy, SOURCE_TOPIC, self._on_msg, _QOS)
                self._node.create_timer(1.0 / HZ, self._tick)
                executor.add_node(self._node)
            except Exception as e:
                print(f"[{CARD}] ROS2 subscription unavailable: {e}", flush=True)
                self._node = None
                self._pub = None

    def _on_msg(self, msg):
        self._last_msg = msg
        self._received_at_ms = int(time.time() * 1000)

    def _data(self):
        return build(self._last_msg, self._received_at_ms)

    def _tick(self):
        if self._pub is None:
            return
        msg = String()
        msg.data = json.dumps(self._data(), ensure_ascii=False)
        self._pub.publish(msg)

    def get_tool(self):
        return {"name": CARD, "type": TYPE, "multiInstance": False,
                "description": DESC + f" ({SOURCE_TOPIC})",
                "inputSchema": {"type": "object", "properties": {"action": {"type": "string", "enum": ["info", "start", "stop"]}}, "required": ["action"], "additionalProperties": False},
                "topic_out": topic_out(self._topic, FMT)}

    def start(self):
        return {"state": "running" if self._pub else "unavailable"}

    def stop(self):
        return {"state": "idle"}

    def dispatch(self, action, args):
        if action == "start":
            return self.start()
        if action == "stop":
            return self.stop()
        if action in ("info", "read", "get", CARD):
            return {"state": "running" if self._pub else "unavailable", "data": self._data(),
                    "topic_out": topic_out(self._topic, FMT)}
        return None


def make_plugin(plugin_config, namespace, executor, client):
    return Plugin(plugin_config, namespace, executor, client)
