# 实现来源(source)—— battery

- **源仓库**:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 `unitree/tiangong_pro/` 代码)
- **文件路径**:`plugins/battery.py`(待实现)
- **类名**:`BatteryStatePlugin`(待实现)
- **公共依赖**:`ros_bridge.py`(ROS2 订阅桥)、`bodyctrl_msgs/msg/PowerBatteryStatus`
- **注册位置**:`main.py` 插件聚合(待实现);驱动镜像/端口:待定
- **MCP 协议**:JSON-RPC 2.0 over HTTP,注册到 Agent Core

## 数据源 topic(来自天轶2.0 SDK 文档)

| ROS2 topic | 频率 | 说明 |
|---|---|---|
| `/power/battery/status` | 1 Hz | 主/小电池电压/电流/电量 + 电源板 pg 状态位 |

## PowerBatteryStatus.msg 字段

| 字段 | 类型 | 含义 |
|---|---|---|
| `header.stamp` | time | 采样时间戳 |
| `battery_installed` | uint8 | 电池安装位图:0x00 无 / 0x01 小电池 / 0x02 大电池 / 0x03 大小都有 |
| `battery_working` | uint8 | 工作中电池:0x10 大电池 / 0x01 小电池 |
| `master_battery_voltage` | float32 | 主电池电压(V) |
| `master_battery_current` | float32 | 主电池电流(A,负=放电,正=充电) |
| `master_battery_power` | float32 | 主电池电量(%) |
| `little_battery_voltage` | float32 | 小电池电压(V) |
| `little_battery_current` | float32 | 小电池电流(A,负=放电,正=充电) |
| `little_battery_power` | float32 | 小电池电量(%) |
| `pg12a`–`pg5ab` | uint8 | 电源板各路供电状态(0 低/1 高) |

## 聚合输出 JSON 结构

```json
{
  "installed": 3,
  "working": 16,
  "master": { "voltage": 48.0, "current": -2.5, "power": 85.0 },
  "little": { "voltage": 12.0, "current": 0.0, "power": 90.0 },
  "pg": { "12a":1, "12b":1, "12c":1, "12d":1, "5cd":1, "5ab":1 },
  "timestamp_ms": 1784025258226,
  "control_level": "ANY"
}
```

> 本目录为 `draft` 阶段,`impl/battery.py` 尚未提供。待驱动代码编写后,在此摘录 `BatteryStatePlugin` 本体与关键依赖方法。
> 本目录不含任何口令/密钥。
