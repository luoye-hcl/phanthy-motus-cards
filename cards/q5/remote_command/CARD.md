# remote_command —— Q5 遥控指令(状态卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `remote_command` |
| 类型 | `sensor`(只读) |
| 控制等级 | `HIGHLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动插件已实现,待部署验证) |

## 能力

订阅 `/send_remote/command`(`sensor_msgs/msg/Joy`),读取 Q5 遥控指令。数据经 q5_bus_bridge 桥接到 Agent Core topic `/{ns}/q5/remote_command`(Domain 42 FastDDS)。

## 接口

- MCP 工具名:`remote_command`
- 调用:`{"action":"info"}`(读当前值) / `{"action":"start"}` / `{"action":"stop"}`
- 返回包络(成功):`{ok:true, card, state, data:{...}, timestamp_ms}`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `info` | 无 | 读取当前 遥控指令 |
| `start` | 无 | 启动卡片发布 |
| `stop` | 无 | 停止卡片发布 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/send_remote/command` | `sensor_msgs/msg/Joy` |

### 返回字段

| 字段 | 类型 | 单位 | 说明 |
|---|---|---|---|
| `axes` | float64[] | - | 摇杆轴值(当前为空) |
| `buttons` | int32[] | - | 按键状态(按下=1) |

### 返回示例

```json
{"axes":[],"buttons":[2,0,0,0,0]}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`remote_command.py`  类:`Plugin`(**已实现**——自建 ROS2 Node 订阅 `/send_remote/command`)
- 依赖:`sensor_contract.py`、`sensor_msgs/msg/Joy`
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 数据源:`/send_remote/command` 真机已验证(✅ 有数据流)。
- 驱动插件:已实现,自建 Node 订阅 Joy 消息,解析 axes + buttons。待部署到 q5-driver-huang 验证。
