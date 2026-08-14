# 验收证据 —— diagnostics

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS, 桥接 Domain 42 FastDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/diagnostics_agg` |
| 消息类型 | `diagnostic_msgs/msg/DiagnosticArray` |
| 桥接输出 | `/${ns}/q5/diagnostics` |
| 状态 | ⚠️ 无诊断消息 |

### 真实数据样本(MCP tools/call action=info)

```json
{"fresh": false, "available": false, "has_diagnostic_message": false,
 "source_publisher_count": 1, "publisher_connected": true,
 "source_state": "awaiting_diagnostic_event",
 "message": "诊断发布器已连接，尚无诊断消息"}
```

### 备注

发布器已连接(1 个),但事件式诊断无新消息,属正常等待状态

## 完整验收清单

- [x] MCP tools/list 确认工具 `diagnostics` 已注册
- [x] MCP tools/call action=info 能返回数据
- [x] 数据经 q5_bus_bridge 桥接到 Agent Core(`/nvidia_desktop/q5/diagnostics`)
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
