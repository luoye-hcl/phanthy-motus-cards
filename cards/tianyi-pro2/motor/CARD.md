# motor —— 天轶2.0 Pro 全身21电机状态(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `tianyi-pro2` |
| 卡片名(MCP 工具名) | `motor` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY`(高层/低层都出) |
| 作者 | `huangchanglong` |
| 状态 | `draft`(未实机验收) |

## 能力

聚合天轶2.0 Pro 全身 21 个电机关节的实时状态(位置/速度/电流/温度/错误),按部位分四路 ROS2 topic 订阅后归一输出。用于姿态监控、关节健康巡查、控制环反馈观察,供大模型或人监控机器人当前身体状态。

覆盖部位与关节ID(与 `MotorName.msg` 定义一致):

| 部位 | 关节ID | 关节名 |
|---|---|---|
| 头部 | 1,2,3 | Head Roll/Pitch/Yaw |
| 左臂 | 11–17 | Left Shoulder Pitch/Roll/Yaw, Left Elbow Pitch, Left Wrist Yaw/Pitch/Roll |
| 右臂 | 21–27 | Right Shoulder Pitch/Roll/Yaw, Right Elbow Pitch, Right Wrist Yaw/Pitch/Roll |
| 腰部 | 31,32 | Waist Yaw/Pitch |
| 腿部 | 51,52 | Hip Pitch, Knee Pitch |

> 手指 12 DOF 归 `hand` 卡;底盘 2 DOF 非电机,归 `chassis` 卡;均不在本卡。

## 接口

- 输出 topic(4 路,频率各不同):
  - `/head/status`   格式:`bodyctrl_msgs/msg/MotorStatusMsg`  频率:400 Hz
  - `/waist/status`  格式:`bodyctrl_msgs/msg/MotorStatusMsg`  频率:500 Hz
  - `/arm/status`    格式:`bodyctrl_msgs/msg/MotorStatusMsg`  频率:500 Hz
  - `/leg/status`    格式:`bodyctrl_msgs/msg/MotorStatusMsg`  频率:500 Hz
- 采样频率:四路 topic 频率不同(head=400Hz, waist=500Hz, arm=500Hz, leg=500Hz)(2026-07-28 实测)
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`,core 不渲染执行按钮)

### 实测数据样本(2026-07-28,x86 192.168.41.1,bodycontrol 已激活)

| 部位 | 关节 | pos(rad) | temp(°C) | 说明 |
|---|---|---|---|---|
| head | 1 | 0.0457 | 43 | |
| head | 2 | 0.0184 | 47 | |
| head | 3 | -0.1154 | 46 | |
| waist | 31 | 0.0266 | 0 | 待机,temp/current/speed 全 0 |
| waist | 32 | 0.0887 | 0 | 待机 |
| arm | 11-17, 21-27 | — | 32-38 | 14 关节正常 |
| leg | 51 | -0.0875 | 0 | 待机 |
| leg | 52 | -0.2633 | 0 | 待机 |

### 字段(每路 MotorStatusMsg)

| 字段 | 含义 | 单位 |
|---|---|---|
| `header.stamp` | 采样时间戳 | ns |
| `status[].name` | 关节ID(见 MotorName.msg,1/2/3/11–17/21–27/31/32/51/52) | — |
| `status[].pos` | 关节位置 | rad |
| `status[].speed` | 关节速度 | rad/s |
| `status[].current` | 关节电流 | A |
| `status[].temperature` | MOS 温度 | ℃ |
| `status[].error` | 关节错误码(见下表) | — |

### error 错误码定义

| error 值 | 含义 |
|---|---|
| 33072 | 设备掉线 |
| 33073 | 关节位置超限 |
| 1 | 关节电机过温 |
| 2 | 过流 |
| 3 | 电压过低 |
| 4 | 关节 MOS 过温 |
| 5 | 堵转 |
| 6 | 电压过高 |
| 7 | 缺相 |
| 8 | 编码器错误 |

### 聚合后 JSON 输出结构

```json
{
  "parts": {
    "head":  [{ "name":1, "pos":..., "speed":..., "current":..., "temperature":..., "error":0 }, ...],
    "waist": [...],
    "arm":   [...],
    "leg":   [...]
  },
  "timestamp_ms": 1784025258226,
  "control_level": "ANY"
}
```

## 数据来源 / 实现位置

- 源仓库:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 tiangong_pro 代码)
- 文件:`plugins/motor.py`  类:`MotorStatePlugin`(待实现)
- 依赖:`ros_bridge.py`(ROS2 订阅桥)、`bodyctrl_msgs`(msg 依赖)
- 注册:`main.py` 插件聚合;驱动镜像/端口:待定(MCP HTTP server, JSON-RPC 2.0)

> 本卡为 `draft` 阶段,驱动代码尚未编写。接口字段以天轶2.0 SDK 文档(2026-05-21 版)为准。

## 状态说明

- 离线:未实现(驱动代码待写)。
- 实机:未验收。待真机环境 `ros2 topic echo /head/status` 确认字段与频率后升 `offline-green`。
- 升 `accepted` 流程:见 `docs/WEBSITE_VERIFICATION.md`。
