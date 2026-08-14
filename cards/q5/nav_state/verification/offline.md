# 验收证据 —— nav_state

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS, 桥接 Domain 42 FastDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/era_nav/nav_status` |
| 消息类型 | `std_msgs/msg/String` |
| 桥接输出 | `/${ns}/q5/nav_state` |
| 状态 | ⚠️ 导航栈未运行 |

### 真实数据样本(MCP tools/call action=info)

```json
{"fresh": false, "available": false, "has_status": false, "status": null,
 "source_publisher_count": 0, "source_state": "navigation_stack_not_running",
 "message": "导航状态发布器未运行"}
```

### 备注

导航栈未运行(publisher=0),无数据流

## 完整验收清单

- [x] MCP tools/list 确认工具 `nav_state` 已注册
- [x] MCP tools/call action=info 能返回数据
- [x] 数据经 q5_bus_bridge 桥接到 Agent Core(`/nvidia_desktop/q5/nav_state`)
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
