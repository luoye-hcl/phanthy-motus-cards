# linkcraft —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `linkcraft` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

执行灵创动作资源（ExecuteActionResource）

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "resource_key": {
      "type": "string",
      "description": "资源 key，来自 linkcraft_catalog 工具"
    },
    "resource_version": {
      "type": "string",
      "description": "资源版本"
    },
    "resource_type": {
      "type": "string",
      "enum": [
        "BODY_MONTION",
        "ARM_MONTION"
      ],
      "description": "vendor 原始拼写（保留 MONTION 拼写以匹配 meta JSON 字段）"
    }
  },
  "required": [
    "resource_key",
    "resource_version",
    "resource_type"
  ]
}
```

## 使用约束

- 会执行真实动作资源。`BODY_MONTION` 和 `ARM_MONTION` 是 vendor 原始拼写，不能改写；执行前需用户明确授权。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
