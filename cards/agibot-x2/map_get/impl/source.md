# map_get 实现来源

- 运行时实现：`4paradigm/phanthymotus-driver:agibot/x2/device.py`。
- 通信栈：ROS 2 `rclpy` + `aimdk_msgs`；机器人域为 0，Core 域为 42，由 `DualDomainROS2` 桥接。
- MCP 定义：2026-09-04 从运行中驱动的 `tools/list` 获取。

## 输出语义

运行时 MCP 已注册，但 `config.yaml` 的 `slam.enabled` 为 false；以实际注册为准，数据待验收。

## 验收边界

仅做 schema、MCP 注册和数据可用性验证。
