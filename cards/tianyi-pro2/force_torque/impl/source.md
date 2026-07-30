# 实现来源(source)—— force_torque

- **源仓库**:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 `unitree/tiangong_pro/` 代码)
- **文件路径**:`plugins/force_torque.py`(待实现)
- **类名**:`ForceTorqueStatePlugin`(待实现)
- **公共依赖**:`ros_bridge.py`(ROS2 订阅桥)、`geometry_msgs/msg/WrenchStamped`
- **注册位置**:`main.py` 插件聚合(待实现);驱动镜像/端口:待定
- **MCP 协议**:JSON-RPC 2.0 over HTTP,注册到 Agent Core

## 数据源 topic(来自天轶2.0 SDK 文档)

| ROS2 topic | 侧别 | 频率 |
|---|---|---|
| `/arm_6dof_left` | 左臂六维力 | 100 Hz |
| `/arm_6dof_right` | 右臂六维力 | 100 Hz |

## WrenchStamped.msg 定义

```
Header header
  uint32 seq          # 序列号
  time stamp          # 时间戳
  string frame_id     # 帧id
Wrench wrench
  Vector3 force       # 3个方向的力
  Vector3 torque      # 3个方向的力矩
```

## 整机坐标系(来自 SDK 文档"坐标系"节)

- X 轴(Roll):机器人前方为正
- Y 轴(Pitch):机器人左方为正
- Z 轴(Yaw):机器人上方为正

> 本目录为 `draft` 阶段,`impl/force_torque.py` 尚未提供。待驱动代码编写后,在此摘录 `ForceTorqueStatePlugin` 本体与关键依赖方法。
> 本目录不含任何口令/密钥。
