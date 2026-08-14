# system_health —— Q5 运行健康(状态卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `system_health` |
| 类型 | `sensor(只读)` |
| 控制等级 | `HIGHLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已部署,待正式验收) |

## 能力

订阅 `/motion_manager/motion_status`(`xbot_common_interfaces/msg/MotionStatus`),读取 Q5 运行健康。数据经 q5_bus_bridge 桥接到 Agent Core topic `/{ns}/q5/system_health`(Domain 42 FastDDS)。

## 接口

- MCP 工具名:`system_health`
- 调用:`{"action":"info"}`(读当前值) / `{"action":"start"}` / `{"action":"stop"}`
- 返回包络(成功):`{ok:true, card, state, data:{...}, timestamp_ms}`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `info` | 无 | 读取当前 运行健康 |
| `start` | 无 | 启动卡片发布 |
| `stop` | 无 | 停止卡片发布 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/motion_manager/motion_status` | `xbot_common_interfaces/msg/MotionStatus` |

### 返回字段

| 字段 | 类型 | 单位 | 说明 |
|---|---|---|---|
| `readings` | object | - | 各数据源最新读数 |
| `maximum_celsius` | float64 | ℃ | 最高温度 |
| `minimum_celsius` | float64 | ℃ | 最低温度 |
| `robot_active` | bool | - | 机器人是否 ACTIVE |
| `available_sources` | array | - | 可用数据源列表 |
| `all_required_sources_fresh` | bool | - | 必需源是否全部新鲜 |

### 返回示例

```json
{"ok":true,"card":"system_health","state":"running","data":{"robot_active":true,"maximum_celsius":38.0,"all_required_sources_fresh":true}}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`system_health.py`  类:`Plugin`
- 依赖:`q5_sdk_client.py`(只读 ROS2 客户端)、`sensor_contract.py`
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 驱动:`q5-driver-huang`(容器)已在 Jetson 192.168.8.40 运行,已注册到 Agent Core。
- 实机:待逐卡验收后升 `offline-green`。
