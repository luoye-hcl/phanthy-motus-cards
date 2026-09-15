# 实现来源 —— arm_gesture

- 源仓库：`4paradigm/phanthymotus-driver`
- 文件：`pndbotics/adam/device.py`
- 类：`ArmGesturePlugin`
- 控制接口：共享 `ArmPlugin` 的 ROS2 `sensor_msgs/msg/JointState`
- 发布频率：约 `100Hz`
- 姿势来源：Adam 官方 SDK `open_arm.py`
