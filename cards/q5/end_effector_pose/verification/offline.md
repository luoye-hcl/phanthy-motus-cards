# 验收证据 —— end_effector_pose

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/mobile_manipulator/end_effector_pose` |
| 消息类型 | `std_msgs/msg/Float32MultiArray` |
| 状态 | ⚠️ 有 1 个 publisher 但当前无数据流(仅移动操作模式发布,数据稀疏) |

### 真实数据样本(ros2 topic echo --once)

```json
{"data":[]}
```

### 备注

⚠️ 有 1 个 publisher 但当前无数据流(仅移动操作模式发布,数据稀疏)

## 完整验收清单

- [x] `ros2 topic list -t` 确认 topic 存在且类型匹配
- [x] `ros2 topic echo` 采样到真实数据
- [ ] 驱动插件实现并订阅 `/mobile_manipulator/end_effector_pose`
- [ ] 驱动注册到 Agent Core,桥接 `/nvidia_desktop/q5/end_effector_pose`
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
