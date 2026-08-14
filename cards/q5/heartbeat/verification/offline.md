# 验收证据 —— heartbeat

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/system/heartbeat` |
| 消息类型 | `std_msgs/msg/Header` |
| 状态 | ✅ 有数据流(约 3.5Hz,动态启动管理器存活) |

### 真实数据样本(ros2 topic echo --once)

```json
{"stamp":{"sec":1786618664,"nanosec":417291073},"frame_id":"dynamic_launch_manager"}
```

### 备注

✅ 有数据流(约 3.5Hz,动态启动管理器存活)

## 完整验收清单

- [x] `ros2 topic list -t` 确认 topic 存在且类型匹配
- [x] `ros2 topic echo` 采样到真实数据
- [ ] 驱动插件实现并订阅 `/system/heartbeat`
- [ ] 驱动注册到 Agent Core,桥接 `/nvidia_desktop/q5/heartbeat`
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
