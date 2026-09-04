# pmu_led —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `pmu_led` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

设置 PMU 灯带模式与颜色（SetPmuLed）

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "mode": {
      "type": "string",
      "enum": [
        "constant",
        "breath",
        "flash",
        "flow"
      ],
      "default": "constant"
    },
    "r": {
      "type": "integer",
      "minimum": 0,
      "maximum": 255,
      "default": 0
    },
    "g": {
      "type": "integer",
      "minimum": 0,
      "maximum": 255,
      "default": 0
    },
    "b": {
      "type": "integer",
      "minimum": 0,
      "maximum": 255,
      "default": 0
    },
    "priority": {
      "type": "integer",
      "minimum": 0,
      "maximum": 100,
      "default": 100,
      "description": "灯带控制优先级 (0-100)；实测除 100（最高）外的任何值都被 PMU固件拒绝（返回 status_code 4132），推测系统默认状态灯以更高优先级占用了灯带，只有最高优先级请求才能覆盖。"
    },
    "reset_priority": {
      "type": "boolean",
      "default": false
    }
  }
}
```

## 使用约束

- 会改变物理灯带状态。实测 priority 非 100 会被固件以 `4132` 拒绝；测试不得擅自改变灯带。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
