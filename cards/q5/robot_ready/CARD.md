# robot_ready —— Q5 业务就绪状态(状态卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `robot_ready` |
| 类型 | `sensor(只读)` |
| 控制等级 | `HIGHLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已部署,待正式验收) |

## 能力

订阅 `/xbot_state`(`xbot_common_interfaces/msg/RobotStatus`),读取 Q5 业务就绪状态。数据经 q5_bus_bridge 桥接到 Agent Core topic `/{ns}/q5/robot_ready`(Domain 42 FastDDS)。

## 接口

- MCP 工具名:`robot_ready`
- 调用:`{"action":"info"}`(读当前值) / `{"action":"start"}` / `{"action":"stop"}`
- 返回包络(成功):`{ok:true, card, state, data:{...}, timestamp_ms}`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `info` | 无 | 读取当前 业务就绪状态 |
| `start` | 无 | 启动卡片发布 |
| `stop` | 无 | 停止卡片发布 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/xbot_state` | `xbot_common_interfaces/msg/RobotStatus` |

### 返回字段

| 字段 | 类型 | 单位 | 说明 |
|---|---|---|---|
| `robot_state` | string | - | 厂商状态标签(READY/ACTIVE/INIT/...) |
| `robot_status` | object | - | 状态详情(state/state_label/ready) |
| `motion_manager_lifecycle` | object | - | 运动管理器生命周期(active/...) |
| `motion_ready` | bool | - | 是否可运动 |
| `ready` | bool | - | 是否就绪(READY 或 ACTIVE) |
| `message` | string | - | 中文状态描述 |

### 返回示例

```json
{"ok":true,"card":"robot_ready","state":"running","data":{"robot_state":"READY","ready":true,"message":"机器人当前状态：READY；运动管理器生命周期：ACTIVE"}}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`robot_ready.py`  类:`Plugin`
- 依赖:`q5_sdk_client.py`(只读 ROS2 客户端)、`sensor_contract.py`
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 驱动:`q5-driver-huang`(容器)已在 Jetson 192.168.8.40 运行,已注册到 Agent Core。
- 实机:待逐卡验收后升 `offline-green`。
