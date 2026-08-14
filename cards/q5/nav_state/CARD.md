# nav_state —— Q5 导航状态(状态卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `nav_state` |
| 类型 | `sensor(只读)` |
| 控制等级 | `HIGHLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已部署,待正式验收) |

## 能力

订阅 `/era_nav/nav_status`(`std_msgs/msg/String`),读取 Q5 导航状态。数据经 q5_bus_bridge 桥接到 Agent Core topic `/{ns}/q5/nav_state`(Domain 42 FastDDS)。

## 接口

- MCP 工具名:`nav_state`
- 调用:`{"action":"info"}`(读当前值) / `{"action":"start"}` / `{"action":"stop"}`
- 返回包络(成功):`{ok:true, card, state, data:{...}, timestamp_ms}`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `info` | 无 | 读取当前 导航状态 |
| `start` | 无 | 启动卡片发布 |
| `stop` | 无 | 停止卡片发布 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/era_nav/nav_status` | `std_msgs/msg/String` |

### 返回字段

| 字段 | 类型 | 单位 | 说明 |
|---|---|---|---|
| `status` | string | - | 厂商导航状态文本 |
| `has_status` | bool | - | 是否有状态数据 |
| `source_topic` | string | - | 数据源 topic |
| `source_publisher_count` | int | - | 发布者数量 |
| `fresh` | bool | - | 数据是否新鲜 |

### 返回示例

```json
{"ok":true,"card":"nav_state","state":"running","data":{"status":"idle","has_status":true,"fresh":true}}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`nav_state.py`  类:`Plugin`
- 依赖:`q5_sdk_client.py`(只读 ROS2 客户端)、`sensor_contract.py`
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 驱动:`q5-driver-huang`(容器)已在 Jetson 192.168.8.40 运行,已注册到 Agent Core。
- 实机:待逐卡验收后升 `offline-green`。
