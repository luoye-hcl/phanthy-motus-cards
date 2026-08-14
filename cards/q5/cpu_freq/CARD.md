# cpu_freq —— Q5 CPU 频率(状态卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `cpu_freq` |
| 类型 | `sensor`(只读) |
| 控制等级 | `HIGHLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动插件已实现并部署) |

## 能力

订阅 `/cpu_freq`(`std_msgs/msg/String`),读取 Q5 CPU 频率。数据经 q5_bus_bridge 桥接到 Agent Core topic `/{ns}/q5/cpu_freq`(Domain 42 FastDDS)。

## 接口

- MCP 工具名:`cpu_freq`
- 调用:`{"action":"info"}` / `{"action":"start"}` / `{"action":"stop"}`

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/cpu_freq` | `std_msgs/msg/String` |

### 返回字段

| 字段 | 类型 | 单位 | 说明 |
|---|---|---|---|
| `cpu_freq` | object | - | 各核心当前/平均/最大/最小频率(JSON) |
| `source_topic` | string | - | 数据源 topic |
| `fresh` | bool | - | 数据是否新鲜 |

### 返回示例

```json
{"cpu_freq":{"cpufreq_name_list":["cpu","cpu_max","cpu_min","cpu_avg","cpu_0","cpu_1","cpu_2","cpu_3","cpu_4","cpu_5","cpu_6","cpu_7","cpu_8","cpu_9","cpu_10"]}}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`cpu_freq.py`  类:`Plugin`(**已实现并部署到 q5-driver-huang**)
- 注册:`main.py` 插件聚合;MCP 端口 15794

## 状态说明

- 驱动插件:已实现、已部署、已注册。
- 实机:✅ 有数据流(CPU 各核心频率,JSON 格式)
