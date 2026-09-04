# joints —— Adam 全身关节状态卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `pnpbotics-adam` |
| 卡片名 | `joints` |
| 类型 | `sensor`(只读) |
| 控制等级 | `ANY` |
| 状态 | `draft` |

## 能力

以约 50Hz 输出 Adam 当前全身关节位置，供画布显示姿态和 3D 骨架。关节位置单位为 `rad`，具体关节数量由 `lite`、`sp` 或 `pro` 机型决定。

## 接口

- 输出：`/{ns}/state/joints`
- 格式：`sensor/skeleton`
- 数据：`joints[].idx`、`joints[].name`、`joints[].q`

## 数据来源

驱动文件：`pnpbotics/adam/device.py`，类：`StatePlugin`。数据来自 DDS `rt/lowstate`。

## 验收状态

待镜像构建后在画布确认工具可见、关节数组持续更新、机型关节数量正确。
