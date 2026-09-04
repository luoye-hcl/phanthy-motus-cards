# joint_command —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `joint_command` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

按 leg/waist/arm/head 分组下发关节位置/速度/力矩/刚度/阻尼指令

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "area": {
      "type": "string",
      "enum": [
        "leg",
        "waist",
        "arm",
        "head"
      ],
      "description": "关节分组"
    },
    "joints": {
      "type": "array",
      "description": "关节指令列表",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "position": {
            "type": "number"
          },
          "velocity": {
            "type": "number",
            "default": 0
          },
          "effort": {
            "type": "number",
            "default": 0
          },
          "stiffness": {
            "type": "number",
            "default": 0
          },
          "damping": {
            "type": "number",
            "default": 0
          }
        },
        "required": [
          "name",
          "position"
        ]
      }
    }
  },
  "required": [
    "area",
    "joints"
  ]
}
```

## 使用约束

- 高风险直接关节控制。必须使用真实 URDF 关节名和机械限位，且仅在保护措施、正确模式和用户明确授权均具备时调用。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
