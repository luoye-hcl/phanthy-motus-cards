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

以 100Hz 发布 ROS2 `JointState`，控制腰部、双臂、腕部和机身高度，并支持归零。适配 Adam 的上肢实时姿态跟踪接口。

## 安全前置条件

机器人必须处于站立状态，并先通过手柄 `xx` 正键进入实时接收外部数据状态，再调用 `enable` 或发送姿态。角度单位为 `rad`，机身高度范围为 `0.6` 到 `1.0 m`。

## 接口

- MCP 工具：`arm`
- 动作：`enable`、`disable`、`set_joints`、`set_height`、`zero`
- 发布：`/{ns}/joint_states`，类型 `sensor_msgs/msg/JointState`

## 数据来源

驱动文件：`pnpbotics/adam/device.py`，类：`ArmPlugin`。上游接口为 Adam ROS2 `joint_states`。

## 验收状态

待镜像构建后先在画布确认工具注册和状态，再进行低风险上肢姿态验证。
