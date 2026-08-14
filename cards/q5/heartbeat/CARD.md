# heartbeat —— Q5 系统心跳(状态卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `heartbeat` |
| 类型 | `sensor`(只读) |
| 控制等级 | `HIGHLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(数据源已验证,驱动插件待实现) |

## 能力

订阅 `/system/heartbeat`(`std_msgs/msg/Header`),读取 Q5 系统心跳。数据经 q5_bus_bridge 桥接到 Agent Core topic `/{ns}/q5/heartbeat`(Domain 42 FastDDS)。

## 接口

- MCP 工具名:`heartbeat`
- 调用:`{"action":"info"}`(读当前值) / `{"action":"start"}` / `{"action":"stop"}`
- 返回包络(成功):`{ok:true, card, state, data:{...}, timestamp_ms}`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `info` | 无 | 读取当前 系统心跳 |
| `start` | 无 | 启动卡片发布 |
| `stop` | 无 | 停止卡片发布 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/system/heartbeat` | `std_msgs/msg/Header` |

### 返回字段

| 字段 | 类型 | 单位 | 说明 |
|---|---|---|---|
| `stamp_sec` | int | s | 时间戳秒 |
| `stamp_nanosec` | int | ns | 时间戳纳秒 |
| `frame_id` | string | - | 来源(dynamic_launch_manager) |

### 返回示例

```json
{"stamp":{"sec":1786618664,"nanosec":417291073},"frame_id":"dynamic_launch_manager"}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`heartbeat.py`  类:`Plugin`(**待实现**——数据源已验证,插件骨架见 impl/)
- 依赖:`q5_sdk_client.py`(需扩展订阅 `/system/heartbeat`)、`sensor_contract.py`
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 数据源:`/system/heartbeat` 真机已验证(✅ 有数据流(约 3.5Hz,动态启动管理器存活))。
- 驱动插件:待实现并合入 robotera-q5-driver,再在 config.yaml 启用。
