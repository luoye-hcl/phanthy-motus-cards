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

通过 DDS `rt/handcmd` 控制 Adam 双手 12 个手指，支持全部张开、全部闭合、分别设置左右手指位置和读取手状态。

## 安全前置条件

发送手部动作前确认手指和手掌周围没有障碍物。PND 灵巧手位置范围为 `0` 到 `1000`：`0` 为弯曲/闭合，`1000` 为伸直/张开。左右手数组顺序均为 `[pinky, ring, middle, index, thumb1, thumb2]`。

## 接口

- MCP 工具：`hand`
- 动作：`open`、`close`、`set_fingers`、`get_state`
- 指令通道：`rt/handcmd`
- 状态通道：`rt/handstate`

## 数据来源

驱动文件：`pnpbotics/adam/device.py`，类：`HandPlugin`。

## 验收状态

待镜像构建后先在画布读取 `get_state`，再人工确认后做张开/闭合验证。
