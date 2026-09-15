# loco —— Adam 高层运动控制卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `pnpbotics-adam` |
| 卡片名 | `loco` |
| 类型 | `actuator` |
| 控制等级 | `HIGHLEVEL` |
| 状态 | `draft` |

## 能力

通过 gRPC 控制 Adam 的模式切换、站立、行走、转向、预置动作、动态姿态、提箱模式和错误清除，也可读取机器人状态与可用动作列表。

## 安全前置条件

运动操作只可在机器人处于可运动状态、急停已释放且周围无人时调用。`move` 的 `vx`、`vy` 单位为 `m/s`，`vyaw` 单位为 `rad/s`；`stand_dynamic.height` 范围为 `0.6` 到 `1.0 m`。

## 接口

- MCP 工具：`loco`
- 动作：`set_mode`、`move`、`stop`、`stand_motion`、`stand_action`、`stand_dynamic`、`get_state`、`list_actions`、`clear_error`、`carry_box`
- gRPC：`RobotControl`，默认端口 `6666`

## 数据来源

驱动文件：`pnpbotics/adam/device.py`，类：`LocoPlugin`；客户端：`pnpbotics/adam/grpc_client.py`。

## 验收状态

待镜像构建后仅先在画布读取 `get_state`，运动动作需人工确认后再做实机验证。
