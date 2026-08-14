# 验收证据 —— system_health

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS, 桥接 Domain 42 FastDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/motion_manager/motion_status` |
| 消息类型 | `xbot_common_interfaces/msg/MotionStatus` |
| 桥接输出 | `/${ns}/q5/system_health` |
| 状态 | ✅ 部分源新鲜 |

### 真实数据样本(MCP tools/call action=info)

```json
{"robot_active": false, "available_sources": ["robot", "temperature", "faults"],
 "stale_sources": [], "all_required_sources_fresh": true,
 "temperature_summary": {"reading_count": 40, "maximum_celsius": 60.0,
   "maximum_sensor": "neck_pitch_joint/driver_temperature", "minimum_celsius": 34.0}}
```

### 备注

40 个温度读数,最高 60°C(neck_pitch driver),最低 34°C。robot/temperature/faults 新鲜,motion 事件源无新事件。

## 完整验收清单

- [x] MCP tools/list 确认工具 `system_health` 已注册
- [x] MCP tools/call action=info 能返回数据
- [x] 数据经 q5_bus_bridge 桥接到 Agent Core(`/nvidia_desktop/q5/system_health`)
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
