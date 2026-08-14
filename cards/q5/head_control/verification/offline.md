# 验收证据 —— head_control

> 实机验证日期: 2026-08-13(门禁只读检查;运动下发待现场同意)
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794), ROS2 Humble Domain 211 CycloneDDS

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 命令 Topic | `/wr1_controller/commands` |
| 消息类型 | `xbot_common_interfaces/msg/HybridJointCommand` |

### 门禁检查(MCP tools/call action=info,只读)

```json
{"ok": true, "state": "idle",
 "safety": {"ros_publisher_available": true,
   "publisher_node": "q5_body_command",
   "control_mode": "direct_joint_position",
   "lifecycle_state": "active", "joint_state_fresh": true,
   "q5_fsm": {"state": 3, "state_label": "READY"},
   "joints": ["neck_yaw_joint", "neck_pitch_joint"]}}
```

### 备注

门禁检查通过:发布器 q5_body_command 可用,lifecycle=active,joint_state fresh,q5_fsm=READY。2 关节 neck_yaw[-0.79,0.79]/neck_pitch[-0.26,0.7]。与 arm_control 共享 body 发布器。

## 完整验收清单

- [x] MCP tools/list 确认工具 `head_control` 已注册
- [x] MCP tools/call action=info 返回门禁检查,ROS 发布器可用、控制就绪
- [ ] **运动下发实测**(需现场操作员在场 + 用户明确同意,机器人 READY/ACTIVE)
- [ ] core 网页面板呈现该卡
- [ ] MT 验收记录(人/日期/结论)

> 说明:本卡为 LOWLEVEL 直接控制卡,运动下发属机器人写操作,未获用户明确同意前不执行。
