# 验收证据 —— arm

## 离线检查

- [x] `metadata.json` JSON 语法通过
- [x] schema 包含 `gesture=raise_hand` 和 `side=left/right`
- [x] schema 与 driver commit `bc12e3f` 的 `ArmPlugin.get_tool()` 对齐

## 实机只读检查

- [x] Adam Jetson 运行镜像 `release.260914.bc12e3f`
- [x] MCP `tools/list` 注册 `arm` actuator
- [x] MCP schema 暴露 `gesture`、`raise_hand`、`left/right`

## 实机动作检查

- [ ] 机器人站立且已进入实时接收状态
- [ ] 获得现场许可后分别验证左侧和右侧 `raise_hand`
- [ ] 动作结束后调用 `disable` 或恢复安全姿态
