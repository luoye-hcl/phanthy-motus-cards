# hand_gesture —— Adam 灵巧手语义动作卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `pnpbotics-adam` |
| 卡片名 | `hand_gesture` |
| 类型 | `actuator` |
| 控制等级 | `HIGHLEVEL` |
| 状态 | `draft` |

## 能力

复用基础 `hand` 控制线程，按左手或右手执行 `thumbs_up`、`wave_open`、`handshake`、`point`、`victory`、`rock` 六种语义手势，并保持另一只手当前目标。

## 安全前置条件

执行前确认手指和手掌周围没有障碍物。真实动作必须获得现场许可；动作结束后使用 `stop` 停止发送手部目标。

## 接口

- MCP 工具：`hand_gesture`
- 动作：`thumbs_up`、`wave_open`、`handshake`、`point`、`victory`、`rock`、`stop`
- 侧别：`side=left/right`
- 共享控制：基础 `hand` 的 DDS `rt/handcmd` 发布线程

## 数据来源

驱动文件：`pndbotics/adam/device.py`，类：`HandGesturePlugin`。目标生成复用 `HandPlugin` 的手型和当前位置缓存。

## 验收状态

本地 schema、单侧目标保持和分发测试已覆盖；新镜像中的 MCP 注册、画布显示和真实动作待部署后分步验证。
