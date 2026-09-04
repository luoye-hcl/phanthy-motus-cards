# battery —— Adam 电池状态卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `pnpbotics-adam` |
| 卡片名 | `battery` |
| 类型 | `sensor`(只读) |
| 控制等级 | `ANY` |
| 状态 | `draft` |

## 能力

输出 Adam 电池电压、电流、功率、累计电量和厂商状态，用于判断机器人是否适合继续运动。

## 接口

- 输出：`/{ns}/state/battery`
- 格式：`data/json`
- `voltage`: V；`current`: A；`power`: W；`wh_accumulated`: Wh

## 数据来源

驱动文件：`pnpbotics/adam/device.py`，类：`StatePlugin`。数据来自 DDS `rt/lowstate` 的 `battery_data`。

## 验收状态

待镜像构建后在画布确认电池字段持续更新。
