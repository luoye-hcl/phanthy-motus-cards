# 验收证据 —— battery

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS, 桥接 Domain 42 FastDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/battery_state` |
| 消息类型 | `sensor_msgs/msg/BatteryState` |
| 桥接输出 | `/${ns}/q5/battery` |
| 状态 | ✅ fresh=true |

### 真实数据样本(MCP tools/call action=info)

```json
{"fresh": true, "percentage": 59.0, "level": "normal",
 "voltage_v": 63.06, "temperature_c": 41.0}
```

### 备注

电量 59%,电压 63.06V,温度 41°C

## 完整验收清单

- [x] MCP tools/list 确认工具 `battery` 已注册
- [x] MCP tools/call action=info 能返回数据
- [x] 数据经 q5_bus_bridge 桥接到 Agent Core(`/nvidia_desktop/q5/battery`)
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
