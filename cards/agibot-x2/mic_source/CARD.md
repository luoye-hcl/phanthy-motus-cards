# mic_source —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `mic_source` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

切换内置/外置麦克风来源（SetMicSourceRequest）

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": [
        "set",
        "get"
      ],
      "description": "Action to perform"
    },
    "source": {
      "type": "string",
      "enum": [
        "internal",
        "external"
      ]
    }
  },
  "required": [
    "action"
  ],
  "x-action-params": {
    "set": {
      "params": [
        "source"
      ],
      "description": "设置麦克风来源"
    },
    "get": {
      "params": [],
      "description": "查询当前麦克风来源"
    }
  }
}
```

## 使用约束

- `get` 为只读查询；`set` 改变硬件输入配置，需额外授权。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
