# 实现来源(source)—— motor

- **源仓库**:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 `unitree/tiangong_pro/` 代码)
- **文件路径**:`plugins/motor.py`(待实现)
- **类名**:`MotorStatePlugin`(待实现)
- **公共依赖**:`ros_bridge.py`(ROS2 订阅桥)、`bodyctrl_msgs/msg/MotorStatusMsg.msg`、`bodyctrl_msgs/msg/MotorStatus.msg`
- **注册位置**:`main.py` 插件聚合(待实现);驱动镜像/端口:待定
- **MCP 协议**:JSON-RPC 2.0 over HTTP,注册到 Agent Core

## 数据源 topic(来自天轶2.0 SDK 文档)

| ROS2 topic | 部位 | 关节ID |
|---|---|---|
| `/head/status` | 头部 | 1,2,3 |
| `/waist/status` | 腰部 | 31,32 |
| `/arm/status` | 双臂 | 11–17,21–27 |
| `/leg/status` | 腿部 | 51,52 |

## MotorStatusMsg.msg 定义

```
std_msgs/Header header
MotorStatus[] status

# MotorStatus.msg
uint16 name          # MotorName(见 MotorName.msg)
float32 pos          # rad
float32 speed        # rad
float32 current      # A
float32 temperature  # MOS温度
uint32 error
```

## MotorName.msg 关节ID映射(本文档版)

```
uint16 MOTOR_HEAD_1 = 1        # Head Roll
uint16 MOTOR_HEAD_2 = 2        # Head Pitch
uint16 MOTOR_HEAD_3 = 3        # Head Yaw
uint16 MOTOR_ARM_LEFT_1 = 11   # Left Shoulder Pitch
uint16 MOTOR_ARM_LEFT_2 = 12   # Left Shoulder Roll
uint16 MOTOR_ARM_LEFT_3 = 13   # Left Shoulder Yaw
uint16 MOTOR_ARM_LEFT_4 = 14   # Left Elbow Pitch
uint16 MOTOR_ARM_LEFT_5 = 15   # Left Wrist Yaw
uint16 MOTOR_ARM_LEFT_6 = 16   # Left Wrist Pitch
uint16 MOTOR_ARM_LEFT_7 = 17   # Left Wrist Roll
uint16 MOTOR_ARM_RIGHT_1 = 21  # Right Shoulder Pitch
uint16 MOTOR_ARM_RIGHT_2 = 22  # Right Shoulder Roll
uint16 MOTOR_ARM_RIGHT_3 = 23  # Right Shoulder Yaw
uint16 MOTOR_ARM_RIGHT_4 = 24  # Right Elbow Pitch
uint16 MOTOR_ARM_RIGHT_5 = 25  # Right Wrist Yaw
uint16 MOTOR_ARM_RIGHT_6 = 26  # Right Wrist Pitch
uint16 MOTOR_ARM_RIGHT_7 = 27  # Right Wrist Roll
uint16 MOTOR_WAIST_01 = 31     # Waist Yaw
uint16 MOTOR_WAIST_02 = 32     # Waist Pitch
uint16 MOTOR_LEG_LEFT_1 = 51   # Hip Pitch(文档未标左右)
uint16 MOTOR_LEG_LEFT_2 = 52   # Knee Pitch
```

> 本目录为 `draft` 阶段,`impl/motor.py` 尚未提供。待驱动代码编写后,在此摘录 `MotorStatePlugin` 本体与关键依赖方法。
> 本目录不含任何口令/密钥。
