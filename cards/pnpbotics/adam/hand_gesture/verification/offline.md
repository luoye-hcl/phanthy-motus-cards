# 验收证据 —— hand_gesture

## 离线检查

- [x] `metadata.json` JSON 语法通过
- [x] schema 包含六种手势、`stop` 和 `side=left/right`
- [x] driver 测试覆盖独立工具注册、分发、基础 `hand` schema 隔离和另一只手目标保持

## 实机只读检查

- [x] `release.260915.a886991` 实机 MCP `tools/list` 注册 `hand_gesture` actuator；`info` 可用，DDS publisher 与反馈 reader 均可用
- [ ] 画布显示独立 `hand_gesture` 卡片及参数

## 实机动作检查

- [ ] 获得现场许可后验证左手和右手语义动作
- [ ] 验证未选中手保持原目标
- [ ] 动作结束后恢复张开姿态并调用 `stop`
