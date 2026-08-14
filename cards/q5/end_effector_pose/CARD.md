# end_effector_pose —— Q5 末端执行器位姿(状态卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `end_effector_pose` |
| 类型 | `sensor`(只读) |
| 控制等级 | `HIGHLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(数据源已验证,驱动插件待实现) |

## 能力

订阅 `/mobile_manipulator/end_effector_pose`(`std_msgs/msg/Float32MultiArray`),读取 Q5 末端执行器位姿。数据经 q5_bus_bridge 桥接到 Agent Core topic `/{ns}/q5/end_effector_pose`(Domain 42 FastDDS)。

## 接口

- MCP 工具名:`end_effector_pose`
- 调用:`{"action":"info"}`(读当前值) / `{"action":"start"}` / `{"action":"stop"}`
- 返回包络(成功):`{ok:true, card, state, data:{...}, timestamp_ms}`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `info` | 无 | 读取当前 末端执行器位姿 |
| `start` | 无 | 启动卡片发布 |
| `stop` | 无 | 停止卡片发布 |

### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/mobile_manipulator/end_effector_pose` | `std_msgs/msg/Float32MultiArray` |

### 返回字段

| 字段 | 类型 | 单位 | 说明 |
|---|---|---|---|
| `data` | float32[] | - | [x,y,z,qx,qy,qz,qw] 末端位置与姿态四元数 |

### 返回示例

```json
{"data":[]}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`end_effector_pose.py`  类:`Plugin`(**待实现**——数据源已验证,插件骨架见 impl/)
- 依赖:`q5_sdk_client.py`(需扩展订阅 `/mobile_manipulator/end_effector_pose`)、`sensor_contract.py`
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 数据源:`/mobile_manipulator/end_effector_pose` 真机已验证(⚠️ 有 1 个 publisher 但当前无数据流(仅移动操作模式发布,数据稀疏))。
- 驱动插件:待实现并合入 robotera-q5-driver,再在 config.yaml 启用。
