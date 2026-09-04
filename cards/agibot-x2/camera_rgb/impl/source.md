# camera_rgb 实现来源

- 运行时实现：`4paradigm/phanthymotus-driver:agibot/x2/device.py`。
- 通信栈：ROS 2 `rclpy` + `aimdk_msgs`；机器人域为 0，Core 域为 42，由 `DualDomainROS2` 桥接。
- MCP 定义：2026-09-04 从运行中驱动的 `tools/list` 获取。

## 输出语义

真机 RGB 输入为 `/aima/hal/sensor/rgb_head_front_center/rgb_image/compressed`。

## 验收边界

仅做 schema、MCP 注册和数据可用性验证。
