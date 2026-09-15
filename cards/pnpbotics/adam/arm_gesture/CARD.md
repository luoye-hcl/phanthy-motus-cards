# arm_gesture —— Adam 手臂语义动作卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `pnpbotics-adam` |
| 卡片名 | `arm_gesture` |
| 类型 | `actuator` |
| 控制等级 | `HIGHLEVEL` |
| 状态 | `draft` |

## 能力

复用基础 `arm` 控制器执行 Adam 官方 SDK 单侧举手姿势。支持左臂或右臂，调用后持续发布目标，直到执行 `stop` 或其他上肢控制命令。

## 安全前置条件

机器人必须处于站立状态，并先通过手柄进入实时接收外部数据状态。执行前确认对应手臂活动范围内无人和障碍物；真实动作必须获得现场许可。

## 接口

- MCP 工具：`arm_gesture`
- 动作：`raise_hand`、`stop`
- 侧别：`side=left/right`
- 确认：`raise_hand` 必须传 `confirm=true`；该值表示现场人员已核实站立、实时接收模式和活动范围安全，driver 无法自行确认这些条件
- 共享控制：基础 `arm` 的 ROS2 `JointState` 发布器

## 数据来源

驱动文件：`pndbotics/adam/device.py`，类：`ArmGesturePlugin`。举手姿势来自 Adam 官方 SDK `open_arm.py` 示例。

## 验收状态

本地 schema 和分发测试已覆盖；新镜像中的 MCP 注册、画布显示和真实动作待部署后分步验证。
