# head_control —— Q5 头部控制(控制卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `head_control` |
| 类型 | `actuator` |
| 控制等级 | `LOWLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已部署,待实机验收) |

## 能力

控制头部两个关节:偏航(左右转头)与俯仰(抬头/低头)。目标角度基于 URDF 关节限制校验后插值下发。

## 安全前置条件

直接控制接口,仅在机器人未处于保护/急停状态、`/xbot_state` 为 READY/ACTIVE、motion_manager 生命周期 active、且 `/joint_states` 新鲜时有效。动作有时限,到时自动停车/保持。

## 接口

- MCP 工具名:`head_control`
- 调用:`{"action":"<动作>", ...入参}`
- 返回包络(成功):`{ok:true, card, action, state, command, timestamp_ms}`
- 返回包络(失败):`{ok:false, code, message, details, timestamp_ms}`
- 错误码:`INVALID_ARGUMENT` / `ROS_UNAVAILABLE` / `LIFECYCLE_NOT_ACTIVE` / `Q5_FSM_NOT_READY` / `LIMIT_EXCEEDED` / `MOTION_IN_PROGRESS`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `start` | 无 | 检查连接状态 |
| `neck_yaw` | neck_yaw_rad | 偏航:左右转头,范围[-0.79,0.79]rad |
| `neck_pitch` | neck_pitch_rad | 俯仰:抬头/低头,范围[-0.26,0.7]rad |
| `cancel` | 无 | 取消微调,保持当前位置 |
| `info` | 无 | 查看状态 |

### 入参

| 参数 | 类型 | 单位 | 范围 | 说明 |
|---|---|---|---|---|
| `neck_yaw_rad` | number | rad | [-0.79, 0.79] | 偏航角度,正负按坐标系 |
| `neck_pitch_rad` | number | rad | [-0.26, 0.7] | 俯仰角度,正抬头负低头 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/wr1_controller/commands` | `xbot_common_interfaces/msg/HybridJointCommand` |

### 返回示例

```json
{"ok":true,"card":"head_control","action":"neck_pitch","state":"moving","command":{"joint":"neck_pitch_joint","target_rad":0.3}}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`head_control.py`  类:`Plugin`
- 依赖:`control_contract.py`(控制就绪校验 q5_is_control_ready)、`joint_limits.py`(URDF 关节限制)
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 驱动:`q5-driver-huang`(容器)已在 Jetson 192.168.8.40 运行,已注册到 Agent Core。
- 实机:待逐卡验收后升 `offline-green`。
