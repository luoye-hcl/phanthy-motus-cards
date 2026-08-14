# end_effector_pose —— Q5 末端执行器位姿(状态卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `end_effector_pose` |
| 类型 | `sensor`(只读) |
| 控制等级 | `HIGHLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动插件已实现,待部署验证) |

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
- 文件:`end_effector_pose.py`  类:`Plugin`(**已实现**——自建 ROS2 Node 订阅 `/mobile_manipulator/end_effector_pose`)
- 依赖:`sensor_contract.py`、`std_msgs/msg/Float32MultiArray`
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 数据源:`/mobile_manipulator/end_effector_pose` 真机已验证(⚠️ 有 publisher 但数据稀疏,MPC 未激活时无数据)。
- 驱动插件:已实现,自建 Node 订阅 Float32MultiArray 消息。待部署到 q5-driver-huang 验证。
