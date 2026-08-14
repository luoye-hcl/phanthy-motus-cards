# hand_state —— Q5 左右手关节状态(状态卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `hand_state` |
| 类型 | `sensor(只读)` |
| 控制等级 | `HIGHLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已部署,待正式验收) |

## 能力

订阅 `/joint_states`(`sensor_msgs/msg/JointState`),读取 Q5 左右手关节状态。数据经 q5_bus_bridge 桥接到 Agent Core topic `/{ns}/q5/hand_state`(Domain 42 FastDDS)。

## 接口

- MCP 工具名:`hand_state`
- 调用:`{"action":"info"}`(读当前值) / `{"action":"start"}` / `{"action":"stop"}`
- 返回包络(成功):`{ok:true, card, state, data:{...}, timestamp_ms}`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `info` | 无 | 读取当前 左右手关节状态 |
| `start` | 无 | 启动卡片发布 |
| `stop` | 无 | 停止卡片发布 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/joint_states` | `sensor_msgs/msg/JointState` |

### 返回字段

| 字段 | 类型 | 单位 | 说明 |
|---|---|---|---|
| `joint_names` | array | - | 手关节名(12 个) |
| `joint_count` | int | - | 手关节数 |
| `positions` | object | rad | 各关节位置 |
| `velocities` | object | rad/s | 各关节速度 |
| `efforts` | object | N·m | 各关节力矩 |
| `complete` | bool | - | 12 关节是否完整 |
| `hand_model` | string | - | XHand Lite |

### 返回示例

```json
{"ok":true,"card":"hand_state","state":"running","data":{"joint_count":12,"complete":true,"hand_model":"XHand Lite"}}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`hand_state.py`  类:`Plugin`
- 依赖:`q5_sdk_client.py`(只读 ROS2 客户端)、`sensor_contract.py`
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 驱动:`q5-driver-huang`(容器)已在 Jetson 192.168.8.40 运行,已注册到 Agent Core。
- 实机:待逐卡验收后升 `offline-green`。
