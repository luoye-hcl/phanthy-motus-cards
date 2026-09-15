# 验收证据 —— arm_gesture

## 离线检查

- [x] `metadata.json` JSON 语法通过
- [x] schema 包含 `raise_hand`、`stop`、`side=left/right`、`confirm` 和 `x-is-dangerous`
- [x] driver 拒绝未经确认的 `raise_hand`；`confirm=true` 只代表现场人工核实，不代表 driver 检测到站立或实时接收模式
- [x] driver 测试覆盖独立工具注册、姿势分发和基础 `arm` schema 隔离

## 实机只读检查

- [x] `release.260915.2135ca3` 实机 MCP `tools/list` 注册 `arm_gesture` actuator；schema 包含 `confirm` 和 `x-is-dangerous`，`info` 为 `idle`
- [x] 未传 `confirm=true` 的左侧 `raise_hand` 返回 `PRECONDITION_FAILED`，调用前后基础 `arm` 均为 `idle`，未启动目标发布
- [ ] 画布显示独立 `arm_gesture` 卡片及参数

## 实机动作检查

- [ ] 机器人站立且已进入实时接收状态
- [ ] 获得现场许可后分别验证左侧和右侧 `raise_hand`
- [ ] 动作结束后调用 `stop` 或恢复安全姿态
