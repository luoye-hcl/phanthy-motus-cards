# arm —— Adam 上肢控制卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `pnpbotics-adam` |
| 卡片名 | `arm` |
| 类型 | `actuator` |
| 控制等级 | `HIGHLEVEL` |
| 状态 | `draft` |

## 能力

以 100Hz 发布 ROS2 `JointState`，控制腰部、双臂、腕部和机身高度。单侧举手动作已移至独立的 `arm_gesture` 卡。

## 安全前置条件

机器人必须处于站立状态，并先通过手柄进入实时接收外部数据状态。调用上肢控制前确认对应手臂活动范围内无人和障碍物；真实动作必须获得现场许可。

## 接口

- MCP 工具：`arm`
- 基础动作：`enable`、`disable`、`set_joints`、`set_height`、`zero`
- 发布：`/{ns}/joint_states`，类型 `sensor_msgs/msg/JointState`

## 数据来源

驱动文件：`pndbotics/adam/device.py`，类：`ArmPlugin`，对应 driver commit `bc12e3f`。

## 验收状态

MCP `tools/list` 已在 Adam Jetson 镜像 `release.260914.bc12e3f` 验证包含基础 `arm` 控制动作；真实上肢控制仍待现场授权后验证。
