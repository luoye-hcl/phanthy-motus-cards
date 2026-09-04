# model —— AgiBot X2 resource 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `model` |
| 类型 | `resource` |
| 状态 | `draft` |

## 能力

返回配置的末端执行器变体（fist/hand/ultra）对应的 URDF

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "variant": {
      "type": "string",
      "enum": [
        "fist",
        "hand",
        "ultra"
      ]
    }
  }
}
```

## 使用约束

- 只读工具，不改变机器人状态。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
