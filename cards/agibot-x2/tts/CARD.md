# tts —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `tts` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

文字转语音播报（PlayTts）

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "text": {
      "type": "string"
    },
    "priority": {
      "type": "string",
      "enum": [
        "background",
        "service",
        "mission",
        "interaction",
        "system",
        "warning",
        "safety"
      ],
      "default": "interaction"
    },
    "interrupt": {
      "type": "boolean",
      "default": false,
      "description": "是否打断同等优先级播报"
    }
  },
  "required": [
    "text"
  ]
}
```

## 使用约束

- 会从机器人扬声器播报，需额外授权，不能作为无副作用测试。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
