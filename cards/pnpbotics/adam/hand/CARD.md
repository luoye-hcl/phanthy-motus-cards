# hand —— Adam 灵巧手控制卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `pnpbotics-adam` |
| 卡片名 | `hand` |
| 类型 | `actuator` |
| 控制等级 | `HIGHLEVEL` |
| 状态 | `draft` |

## 能力

通过 DDS `rt/handcmd` 控制 Adam 双手 12 个电机通道，提供张开、闭合和单通道控制。单手语义动作已移至独立的 `hand_gesture` 卡。

## 安全前置条件

发送手部动作前确认手指和手掌周围没有障碍物。Adam 实机有效位置范围为 `0` 到 `1000`：`0` 为弯曲/闭合，`1000` 为伸直/张开。每只手通道为 `pinky`、`ring`、`middle`、`index`、`thumb_flex`、`thumb_rotate`。

## 接口

- MCP 工具：`hand`
- 基础动作：`open`、`close`、`set_fingers`、`start`、`stop`、`info`、`get_state`
- 单通道参数：`channel` 与 `value=0..1000`
- 指令通道：`rt/handcmd`
- 状态通道：`rt/handstate`

## 数据来源

驱动文件：`pndbotics/adam/device.py`，类：`HandPlugin`，对应 driver commit `bc12e3f`。

## 验收状态

MCP `tools/list` 已在 Adam Jetson 镜像 `release.260914.bc12e3f` 验证包含基础手部控制动作和参数；`get_state` 只读调用仍待验证。
