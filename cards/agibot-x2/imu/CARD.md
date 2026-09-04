# imu —— AgiBot X2 sensor 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `imu` |
| 类型 | `sensor` |
| 状态 | `draft` |

## 能力

胸部+躯干 IMU 合并数据流

## 接口

- 输出：`/agibot_x2/agibot_x2/imu`，格式 `data/json`

```json
{
  "type": "object",
  "properties": {}
}
```

## 使用约束

- 只读工具，不改变机器人状态。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
