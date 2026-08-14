# 验收证据 —— odom

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/wr1_base_drive_controller/odom` |
| 消息类型 | `nav_msgs/msg/Odometry` |
| 状态 | ✅ 有数据流(当前位置/速度全 0 = 机器人静止未动) |

### 真实数据样本(ros2 topic echo --once)

```json
{"frame_id":"odom","child_frame_id":"base_link",
 "position":{"x":0.0,"y":0.0,"z":0.0},
 "orientation":{"x":0.0,"y":0.0,"z":0.0,"w":1.0},
 "linear":{"x":0.0,"y":0.0,"z":0.0},"angular":{"x":0.0,"y":0.0,"z":0.0}}
```

### 备注

✅ 有数据流(当前位置/速度全 0 = 机器人静止未动)

## 完整验收清单

- [x] `ros2 topic list -t` 确认 topic 存在且类型匹配
- [x] `ros2 topic echo` 采样到真实数据
- [ ] 驱动插件实现并订阅 `/wr1_base_drive_controller/odom`
- [ ] 驱动注册到 Agent Core,桥接 `/nvidia_desktop/q5/odom`
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
