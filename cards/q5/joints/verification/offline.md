# 验收证据 —— joints

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS, 桥接 Domain 42 FastDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/joint_states` |
| 消息类型 | `sensor_msgs/msg/JointState` |
| 桥接输出 | `/${ns}/q5/joints` |
| 状态 | ✅ fresh=true |

### 真实数据样本(MCP tools/call action=info)

```json
{"fresh": true, "available": true, "joint_count": 34, "position_unit": "rad",
 "joints": [{"name": "right_shoulder_pitch_joint", "q": -0.0458},
            {"name": "left_elbow_pitch_joint", "q": -0.5994},
            {"name": "neck_pitch_joint", "q": 0.001},
            {"name": "left_hand_thumb_bend_joint", "q": 0.9928}]}
```

### 备注

34 关节实时骨架数据,含身体/双手,位置单位 rad

## 完整验收清单

- [x] MCP tools/list 确认工具 `joints` 已注册
- [x] MCP tools/call action=info 能返回数据
- [x] 数据经 q5_bus_bridge 桥接到 Agent Core(`/nvidia_desktop/q5/joints`)
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
