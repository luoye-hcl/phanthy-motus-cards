# map_get —— AgiBot X2 processor 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `map_get` |
| 类型 | `processor` |
| 状态 | `draft` |

## 能力

按名称查询已保存地图（GetStoredMapByName）

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "map_name": {
      "type": "string"
    }
  },
  "required": [
    "map_name"
  ]
}
```

## 使用约束

- 只读工具，不改变机器人状态。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
