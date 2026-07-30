# force_torque —— 天轶2.0 Pro 双臂六维力(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `tianyi-pro2` |
| 卡片名(MCP 工具名) | `force_torque` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY`(高层/低层都出) |
| 作者 | `huangchanglong` |
| 状态 | `draft`(未实机验收) |

## 能力

读取天轶2.0 Pro 双臂末端六维力/力矩,左右臂各一路 ROS2 topic,100 Hz 高频。用于碰撞检测、力控反馈、拖动示教、接触式装配,供大模型或人监控机械臂与环境接触状态。

## 接口

- 输出 topic(2 路):
  - `/arm_6dof_left`   格式:`geometry_msgs/msg/WrenchStamped`  frame_id: `6dof_left_link`
  - `/arm_6dof_right`  格式:`geometry_msgs/msg/WrenchStamped`  frame_id: `6dof_right_link`
- 采样频率:`100` Hz(文档明确,2026-07-28 实测确认)
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`)

### 字段(每路 WrenchStamped)

| 字段 | 含义 | 单位 |
|---|---|---|
| `header.seq` | 序列号 | — |
| `header.stamp` | 时间戳 | ns |
| `header.frame_id` | 帧ID | — |
| `wrench.force.x` | X 方向力(机器人前方为正) | N |
| `wrench.force.y` | Y 方向力(机器人左方为正) | N |
| `wrench.force.z` | Z 方向力(机器人上方为正) | N |
| `wrench.torque.x` | 绕 X 轴力矩(Roll) | N·m |
| `wrench.torque.y` | 绕 Y 轴力矩(Pitch) | N·m |
| `wrench.torque.z` | 绕 Z 轴力矩(Yaw) | N·m |

> 坐标系:整机坐标系 X 轴前方为正、Y 轴左方为正、Z 轴上方为正(见 SDK 文档"坐标系"节)。

### 聚合后 JSON 输出结构

```json
{
  "left":  { "force": {"x":0.0,"y":0.0,"z":0.0}, "torque":{"x":0.0,"y":0.0,"z":0.0} },
  "right": { "force": {"x":0.0,"y":0.0,"z":0.0}, "torque":{"x":0.0,"y":0.0,"z":0.0} },
  "timestamp_ms": 1784025258226,
  "control_level": "ANY"
}
```

## 数据来源 / 实现位置

- 源仓库:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 tiangong_pro 代码)
- 文件:`plugins/force_torque.py`  类:`ForceTorqueStatePlugin`(待实现)
- 依赖:`ros_bridge.py`(ROS2 订阅桥)、`geometry_msgs/msg/WrenchStamped`
- 注册:`main.py` 插件聚合;驱动镜像/端口:待定(MCP HTTP server, JSON-RPC 2.0)

> 本卡为 `draft` 阶段,驱动代码尚未编写。接口字段以天轶2.0 SDK 文档(2026-05-21 版)为准。

## 状态说明

- 离线:未实现(驱动代码待写)。
- 实机:未验收。待真机 `ros2 topic echo /arm_6dof_left` 确认字段与坐标系方向后升 `offline-green`。
- 升 `accepted` 流程:见 `docs/WEBSITE_VERIFICATION.md`。
