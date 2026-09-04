# joint_command 实现来源

- 运行时实现：`4paradigm/phanthymotus-driver:agibot/x2/device.py`。
- 通信栈：ROS 2 `rclpy` + `aimdk_msgs`；机器人域为 0，Core 域为 42，由 `DualDomainROS2` 桥接。
- MCP 定义：2026-09-04 从运行中驱动的 `tools/list` 获取。

## 输出语义

高风险直接关节控制。必须使用真实 URDF 关节名和机械限位，且仅在保护措施、正确模式和用户明确授权均具备时调用。

## 验收边界

只确认工具注册，或调用明确的只读 action；不执行会改变机器人状态的动作。
