# base_drive —— Q5 底盘速度控制(控制卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `base_drive` |
| 类型 | `actuator` |
| 控制等级 | `LOWLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已部署,待实机验收) |

## 能力

向底盘下发有限时长的速度指令,支持前进、后退、原地左转/右转,以及组合速度。每次动作到时自动发送零速度停车,杜绝无界持续运动。

## 安全前置条件

直接控制接口,仅在机器人未处于保护/急停状态、`/xbot_state` 为 READY/ACTIVE、motion_manager 生命周期 active、且 `/joint_states` 新鲜时有效。动作有时限,到时自动停车/保持。

## 接口

- MCP 工具名:`base_drive`
- 调用:`{"action":"<动作>", ...入参}`
- 返回包络(成功):`{ok:true, card, action, state, command, timestamp_ms}`
- 返回包络(失败):`{ok:false, code, message, details, timestamp_ms}`
- 错误码:`INVALID_ARGUMENT` / `ROS_UNAVAILABLE` / `LIFECYCLE_NOT_ACTIVE` / `Q5_FSM_NOT_READY` / `LIMIT_EXCEEDED` / `MOTION_IN_PROGRESS`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `start` | 无 | 检查控制条件(锁/发布者冲突/限制) |
| `forward` | speed_mps, duration_s | 直线前进,到时自动停车 |
| `backward` | speed_mps, duration_s | 直线后退,到时自动停车 |
| `turn_left` | turn_speed_radps, duration_s | 原地左转,到时自动停车 |
| `turn_right` | turn_speed_radps, duration_s | 原地右转,到时自动停车 |
| `move` | linear_x, angular_z, duration_s | 高级:组合速度 |
| `cancel` | 无 | 立即发送零速度 |
| `info` | 无 | 查看当前命令与安全条件 |

### 入参

| 参数 | 类型 | 单位 | 范围 | 说明 |
|---|---|---|---|---|
| `speed_mps` | number | m/s | [0.01, 0.2] | 直线移动速度 |
| `turn_speed_radps` | number | rad/s | [0.01, 0.4] | 原地转向速度 |
| `linear_x` | number | m/s | [-0.2, 0.2] | 前后线速度(正值前进) |
| `angular_z` | number | rad/s | [-0.4, 0.4] | 转向角速度(正值左转) |
| `duration_s` | number | s | [0.1, 2.0] | 动作持续时间 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/wr1_base_drive_controller/cmd_vel` | `geometry_msgs/msg/TwistStamped` |

### 返回示例

```json
{"ok":true,"card":"base_drive","action":"forward","state":"moving","command":{"linear_x":0.1,"angular_z":0.0,"duration_s":0.5},"stops_automatically":true}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`base_drive.py`  类:`Plugin`
- 依赖:`control_contract.py`(控制就绪校验 q5_is_control_ready)、`joint_limits.py`(URDF 关节限制)
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 驱动:`q5-driver-huang`(容器)已在 Jetson 192.168.8.40 运行,已注册到 Agent Core。
- 实机:待逐卡验收后升 `offline-green`。
