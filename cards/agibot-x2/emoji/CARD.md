# emoji —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `emoji` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

播放屏幕表情（PlayEmoji）

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "emotion": {
      "type": "string",
      "enum": [
        "idle_blink",
        "idle_calm_1",
        "idle_calm_2",
        "idle_game",
        "idle_cute_1",
        "idle_cute_2",
        "idle_cute_3",
        "idle_cute_4",
        "eye_close",
        "eye_open",
        "eye_boring_1",
        "eye_abnormal",
        "eye_sleepy",
        "eye_happy",
        "eye_extremehappy_1",
        "eye_extremehappy_2",
        "eye_sad",
        "eye_sympathy",
        "eye_confuse",
        "eye_shock",
        "eye_actcute",
        "eye_serious",
        "eye_thinking",
        "eye_angry",
        "eye_extremeangry",
        "eye_adore",
        "eye_extremeadore",
        "eye_charge"
      ]
    },
    "loop": {
      "type": "boolean",
      "default": false
    },
    "priority": {
      "type": "integer",
      "default": 0
    }
  },
  "required": [
    "emotion"
  ]
}
```

## 使用约束

- 会改变屏幕表情状态，调用前需额外授权。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
