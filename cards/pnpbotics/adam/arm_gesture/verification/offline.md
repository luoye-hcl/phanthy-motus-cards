# 验收证据 —— arm_gesture

## 离线检查

- [x] `metadata.json` JSON 语法通过
- [x] schema 包含 `raise_hand`、`stop` 和 `side=left/right`
- [x] driver 测试覆盖独立工具注册、姿势分发和基础 `arm` schema 隔离

## 实机只读检查

- [ ] 新镜像 MCP `tools/list` 注册 `arm_gesture` actuator
- [ ] 画布显示独立 `arm_gesture` 卡片及参数

## 实机动作检查

- [ ] 机器人站立且已进入实时接收状态
- [ ] 获得现场许可后分别验证左侧和右侧 `raise_hand`
- [ ] 动作结束后调用 `stop` 或恢复安全姿态
