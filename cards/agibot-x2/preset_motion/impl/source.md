# preset_motion 实现来源

- 运行时实现：`4paradigm/phanthymotus-driver:agibot/x2/device.py`。
- 通信栈：ROS 2 `rclpy` + `aimdk_msgs`；机器人域为 0，Core 域为 42，由 `DualDomainROS2` 桥接。
- MCP 定义：2026-09-04 从运行中驱动的 `tools/list` 获取。

## 输出语义

会触发真实肢体动作。`raise_hand`、`wave_hand`、`shake_hand`、`flying_kiss_hand`、`clap_hand`、`clipfist`、`salute`、`turn_wave_hand` 必须传 `area=left_hand` 或 `right_hand`，否则 vendor 返回 `code=1`。

## 验收边界

只确认工具注册，或调用明确的只读 action；不执行会改变机器人状态的动作。
