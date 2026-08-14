# hand_control —— Q5 灵巧手关节控制(控制卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `hand_control` |
| 类型 | `actuator` |
| 控制等级 | `LOWLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已部署,待实机验收) |

## 能力

控制 XHand Lite 灵巧手(左右各 6 关节,共 12 关节),支持整手开合、整手弯曲、单指弯曲、拇指弯曲+旋转,以及高级 JSON 多关节目标。手关节位置范围 0~1 rad。

## 安全前置条件

直接控制接口,仅在机器人未处于保护/急停状态、`/xbot_state` 为 READY/ACTIVE、motion_manager 生命周期 active、且 `/joint_states` 新鲜时有效。动作有时限,到时自动停车/保持。

## 接口

- MCP 工具名:`hand_control`
- 调用:`{"action":"<动作>", ...入参}`
- 返回包络(成功):`{ok:true, card, action, state, command, timestamp_ms}`
- 返回包络(失败):`{ok:false, code, message, details, timestamp_ms}`
- 错误码:`INVALID_ARGUMENT` / `ROS_UNAVAILABLE` / `LIFECYCLE_NOT_ACTIVE` / `Q5_FSM_NOT_READY` / `LIMIT_EXCEEDED` / `MOTION_IN_PROGRESS`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `start` | 无 | 检查连接状态 |
| `open_hand` | side | 整手张开到 0 rad |
| `close_hand` | side | 整手合拢到 1 rad |
| `set_hand` | side, curl_rad | 整手统一弯曲程度 |
| `set_finger` | side, finger, curl_rad, rotation_rad | 单指弯曲(thumb 可加旋转) |
| `set` | targets | 高级:JSON 指定多关节绝对目标 |
| `cancel` | 无 | 取消插补,保持当前位置 |
| `info` | 无 | 查看运动状态与安全条件 |

### 入参

| 参数 | 类型 | 单位 | 范围 | 说明 |
|---|---|---|---|---|
| `side` | string | - | left/right/both | 执行侧 |
| `finger` | string | - | thumb/index/middle/ring/pinky | 手指 |
| `curl_rad` | number | rad | [0, 1] | 弯曲角度 |
| `rotation_rad` | number | rad | [0, 1] | 拇指旋转角度 |
| `targets` | array | - | 每项 {joint_name, position_rad} | 高级多关节目标 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/hand_controller/commands` | `xbot_common_interfaces/msg/HybridJointCommand` |

### 返回示例

```json
{"ok":true,"card":"hand_control","action":"open_hand","state":"moving","command":{"side":"both","target":0.0}}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`hand_control.py`  类:`Plugin`
- 依赖:`control_contract.py`(控制就绪校验 q5_is_control_ready)、`joint_limits.py`(URDF 关节限制)
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 驱动:`q5-driver-huang`(容器)已在 Jetson 192.168.8.40 运行,已注册到 Agent Core。
- 实机:待逐卡验收后升 `offline-green`。
