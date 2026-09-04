# mic_source 实现来源

- 运行时实现：`4paradigm/phanthymotus-driver:agibot/x2/device.py`。
- 通信栈：ROS 2 `rclpy` + `aimdk_msgs`；机器人域为 0，Core 域为 42，由 `DualDomainROS2` 桥接。
- MCP 定义：2026-09-04 从运行中驱动的 `tools/list` 获取。

## 输出语义

`get` 为只读查询；`set` 改变硬件输入配置，需额外授权。

## 验收边界

只确认工具注册，或调用明确的只读 action；不执行会改变机器人状态的动作。
