# hand_command —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `hand_command` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

手部指令：张开/握拳/自定义手指位置（HandCommandArray）

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": [
        "open",
        "close",
        "set_positions",
        "get_state"
      ],
      "description": "Action to perform"
    },
    "left": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "description": "左手各手指位置 [thumb, index, middle, ring, little]"
    },
    "right": {
      "type": "array",
      "items": {
        "type": "number"
      },
      "description": "右手各手指位置 [thumb, index, middle, ring, little]"
    }
  },
  "required": [
    "action"
  ],
  "x-action-params": {
    "open": {
      "params": [],
      "description": "张开手掌（左右手可分别指定）"
    },
    "close": {
      "params": [],
      "description": "握拳（左右手可分别指定）"
    },
    "set_positions": {
      "params": [
        "left",
        "right"
      ],
      "description": "自定义左右手各手指的位置数组"
    },
    "get_state": {
      "params": [],
      "description": "查询手部关节最新状态快照"
    }
  }
}
```

## 使用约束

- `get_state` 为只读快照；其余 action 会改变手部物理状态，需额外授权。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
