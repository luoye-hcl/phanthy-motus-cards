# locomotion —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `locomotion` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

MC 行走速度控制：需先 register 输入源再 set_velocity；另外机器人 FSM 必须已处于 locomotion_default/run_default 模式（用 mc_mode 切换），站立(stand_default)等模式下 register 会成功但 set_velocity 不会驱动实际行走

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": [
        "register",
        "set_velocity",
        "disable"
      ],
      "description": "Action to perform"
    },
    "forward": {
      "type": "number",
      "description": "前进速度 m/s，+前进/-后退"
    },
    "lateral": {
      "type": "number",
      "description": "侧移速度 m/s，+左移/-右移"
    },
    "angular": {
      "type": "number",
      "description": "转向角速度 rad/s，+左转/-右转"
    }
  },
  "required": [
    "action"
  ],
  "x-action-params": {
    "register": {
      "params": [],
      "description": "以本驱动名义注册一个 MC 输入源（SetMcInputSource ADD）"
    },
    "set_velocity": {
      "params": [
        "forward",
        "lateral",
        "angular"
      ],
      "description": "发布行走速度指令"
    },
    "disable": {
      "params": [],
      "description": "禁用本驱动的输入源"
    }
  }
}
```

## 使用约束

- `set_velocity` 会导致真实移动，且未注册时会自动注册输入源；仅在现场清空、FSM 正确且用户额外确认后调用。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
