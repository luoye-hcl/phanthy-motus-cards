# 验收证据 —— hand_state

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS, 桥接 Domain 42 FastDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/joint_states` |
| 消息类型 | `sensor_msgs/msg/JointState` |
| 桥接输出 | `/${ns}/q5/hand_state` |
| 状态 | ✅ fresh=true |

### 真实数据样本(MCP tools/call action=info)

```json
{"fresh": true, "hand_model": "XHand Lite", "hands_complete": true,
 "left": {"joint_count": 6, "positions": {"left_hand_thumb_bend_joint": 0.9928,
   "left_hand_index_joint1": 0.9095}},
 "right": {"joint_count": 6, "positions": {"right_hand_thumb_bend_joint": -0.0085,
   "right_hand_index_joint1": 0.2090}}}
```

### 备注

左右手各 6 关节 complete=true,左手握拳状(弯曲≈0.9~1.0),右手张开状(≈0.2)

## 完整验收清单

- [x] MCP tools/list 确认工具 `hand_state` 已注册
- [x] MCP tools/call action=info 能返回数据
- [x] 数据经 q5_bus_bridge 桥接到 Agent Core(`/nvidia_desktop/q5/hand_state`)
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
