# 验收证据 —— simple_action

> 实机验证日期: 2026-08-13(门禁只读检查;动作下发待现场解锁)
> 测试环境: Q5 Jetson 192.168.8.40 (nvidia), 驱动容器 q5-driver-huang (MCP 15794)

## 实机验证结果

### Action 信息

| 项目 | 值 |
|---|---|
| Action | `/simple_actions` |
| 类型 | `xbot_common_interfaces/action/SimpleActions` |
| 状态 | ✅ action server 存在(ros2 action list 确认) |

### 白名单动作

| action_name | 说明 | 时长 |
|---|---|---|
| `zero` | 零位复位 | 4.0s |
| `initpose_handsdown` | 垂手初始姿势 | 4.0s |
| `lift_up` | 抬臂动作 | 4.0s |

## 完整验收清单

- [x] `ros2 action list` 确认 `/simple_actions` 存在
- [x] 驱动 simple_action.py 已实现(config.yaml disabled)
- [ ] **现场解锁 + 动作下发实测**(需操作员完成 ready/activate 序列 + 用户同意)
- [ ] core 网页面板呈现该卡
- [ ] MT 验收记录(人/日期/结论)

> 说明:本卡为 LOWLEVEL action 控制卡,动作下发属机器人写操作,且需现场操作员先完成 dynamic_launch/ready/activate 序列解锁,未获用户明确同意前不执行。
