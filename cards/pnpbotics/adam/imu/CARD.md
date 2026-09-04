# imu —— Adam IMU 状态卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `pnpbotics-adam` |
| 卡片名 | `imu` |
| 类型 | `sensor`(只读) |
| 控制等级 | `ANY` |
| 状态 | `draft` |

## 能力

输出 Adam 的姿态四元数、角速度、线加速度、偏航俯仰滚转和 IMU 温度，用于查看机身姿态和运动状态。

## 接口

- 输出：`/{ns}/state/imu`
- 格式：`data/json`
- 四元数顺序：`[w,x,y,z]`
- 角速度单位：`rad/s`；加速度单位：`m/s²`；温度单位：`°C`

## 数据来源

驱动文件：`pnpbotics/adam/device.py`，类：`StatePlugin`。数据来自 DDS `rt/lowstate` 的 `imu_state`。

## 验收状态

待镜像构建后在画布确认 IMU 数据持续更新且字段顺序正确。
