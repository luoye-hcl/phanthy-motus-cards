# hand_gesture —— Q5 预设手势(控制卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `hand_gesture` |
| 类型 | `actuator` |
| 控制等级 | `LOWLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已部署,待实机验收) |

## 能力

执行 XHand Lite 预设手势(10 种:张手、轻握、握拳、指向、捏取、胜利、点赞、OK、比三、摇滚)。内部委托 hand_control 下发,共享同一发布者与命令租约。

## 安全前置条件

直接控制接口,仅在机器人未处于保护/急停状态、`/xbot_state` 为 READY/ACTIVE、motion_manager 生命周期 active、且 `/joint_states` 新鲜时有效。动作有时限,到时自动停车/保持。

## 接口

- MCP 工具名:`hand_gesture`
- 调用:`{"action":"<动作>", ...入参}`
- 返回包络(成功):`{ok:true, card, action, state, command, timestamp_ms}`
- 返回包络(失败):`{ok:false, code, message, details, timestamp_ms}`
- 错误码:`INVALID_ARGUMENT` / `ROS_UNAVAILABLE` / `LIFECYCLE_NOT_ACTIVE` / `Q5_FSM_NOT_READY` / `LIMIT_EXCEEDED` / `MOTION_IN_PROGRESS`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `start` | 无 | 检查连接状态 |
| `open_hand` | side | 张手预设 |
| `light_grip` | side | 轻握预设 |
| `closed_fist` | side | 完全握拳预设 |
| `point` | side | 指向预设 |
| `pinch` | side | 捏取预设 |
| `victory` | side | 胜利手势预设 |
| `thumbs_up` | side | 点赞预设 |
| `ok_sign` | side | OK 手势预设 |
| `three` | side | 比三预设 |
| `rock` | side | 摇滚手势预设 |
| `cancel` | 无 | 取消手势,保持当前位置 |
| `info` | 无 | 查看状态 |

### 入参

| 参数 | 类型 | 单位 | 范围 | 说明 |
|---|---|---|---|---|
| `side` | string | - | left/right/both | 执行侧 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/hand_controller/commands` | `xbot_common_interfaces/msg/HybridJointCommand` |

### 返回示例

```json
{"ok":true,"card":"hand_gesture","action":"open_hand","state":"moving","command":{"side":"both","gesture":"open_hand"}}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`hand_gesture.py`  类:`Plugin`
- 依赖:`control_contract.py`(控制就绪校验 q5_is_control_ready)、`joint_limits.py`(URDF 关节限制)
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 驱动:`q5-driver-huang`(容器)已在 Jetson 192.168.8.40 运行,已注册到 Agent Core。
- 实机:待逐卡验收后升 `offline-green`。
