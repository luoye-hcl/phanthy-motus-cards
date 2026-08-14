# 验收证据 —— base_drive

> 实机验证日期: 2026-08-13(门禁只读检查;运动下发待现场同意)
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 命令 Topic | `/wr1_base_drive_controller/cmd_vel` |
| 消息类型 | `geometry_msgs/msg/TwistStamped` |

### 门禁检查(MCP tools/call action=info,只读)

```json
{"ok": true, "state": "idle",
 "safety": {"ros_publisher_available": true,
   "other_publishers": [{"node_name": "joy_combo_node"}],
   "control_mode": "direct_velocity_interface",
   "q5_fsm": {"state": 3, "state_label": "READY"},
   "limits": {"max_linear_x_mps": 0.2, "max_angular_z_radps": 0.4, "max_duration_s": 2.0}}}
```

### 备注

门禁检查通过:发布器可用,q5_fsm=READY(3)。竞争发布者 joy_combo_node(遥控)。限幅 0.2m/s、0.4rad/s、2s。

## 完整验收清单

- [x] MCP tools/list 确认工具 `base_drive` 已注册
- [x] MCP tools/call action=info 返回门禁检查,ROS 发布器可用、控制就绪
- [ ] **运动下发实测**(需现场操作员在场 + 用户明确同意,机器人 READY/ACTIVE)
- [ ] core 网页面板呈现该卡
- [ ] MT 验收记录(人/日期/结论)

> 说明:本卡为 LOWLEVEL 直接控制卡,运动下发属机器人写操作,未获用户明确同意前不执行。
