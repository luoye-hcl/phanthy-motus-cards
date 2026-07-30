# 实现来源(source)—— hand

- **源仓库**:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 `unitree/tiangong_pro/` 代码)
- **文件路径**:`plugins/hand.py`(待实现)
- **类名**:`HandStatePlugin`(待实现)
- **公共依赖**:`ros_bridge.py`(ROS2 订阅桥)、`sensor_msgs/msg/JointState`
- **注册位置**:`main.py` 插件聚合(待实现);驱动镜像/端口:待定
- **MCP 协议**:JSON-RPC 2.0 over HTTP,注册到 Agent Core

## 数据源 topic(来自天轶2.0 SDK 文档)

| ROS2 topic | 侧别 | 说明 |
|---|---|---|
| `/inspire_hand/state/left_hand` | 左手 | 6 DOF 位置/速度/力(百分比) |
| `/inspire_hand/state/right_hand` | 右手 | 6 DOF 位置/速度/力(百分比) |

## JointState.msg 定义

```
std_msgs/Header header
string[] name          # 说明,id=1为小指,id=6为大拇指旋转
float64[] position     # 百分比
float64[] velocity     # 百分比
float64[] effort       # 百分比
```

## 手指关节ID定义(来自天轶2.0 SDK"手部关节-全局值说明")

```
uint16 MOTOR_FINGER_LITTLE = 1,         //little finger   小指
uint16 MOTOR_FINGER_RING = 2,           //ring finger   无名指
uint16 MOTOR_FINGER_MIDDLE = 3,         //middle finger   中指
uint16 MOTOR_FINGER_FORE = 4,           //Fore finger   食指
uint16 MOTOR_FINGER_THUMB_BEND = 5,     //thumb bend  拇指弯曲
uint16 MOTOR_FINGER_THUMB_ROTATION = 6, //thumb rotation  拇指旋转
```

## 与 tiangong_pro/plugins/hand.py 的关键差异

| 项 | 天轶2.0(本文档) | 天工Pro(已有驱动) |
|---|---|---|
| 状态读取 | topic `/inspire_hand/state/{l,r}_hand`(JointState) | service `/inspire_hand/get_angle/{l,r}_hand` |
| 字段语义 | position/velocity/effort 均为百分比(0–1) | angle_ratio(百分比) |
| 指关节ID | 1-6(小指→拇指旋转) | 同 |
| 控制 | 见 `hand_ctrl` 动作卡(topic+service 双通道) | service 通道 |

> 本目录为 `draft` 阶段,`impl/hand.py` 尚未提供。待驱动代码编写后,在此摘录 `HandStatePlugin` 本体与关键依赖方法。
> 本目录不含任何口令/密钥。
