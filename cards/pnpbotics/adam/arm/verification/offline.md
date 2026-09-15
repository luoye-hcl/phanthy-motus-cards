# 验收证据 —— arm

## 离线检查

- [x] `metadata.json` JSON 语法通过
- [x] schema 仅包含基础 `arm` 控制动作
- [x] schema 与 `ArmPlugin.get_tool()` 对齐

## 实机只读检查

- [x] Adam Jetson 运行镜像 `release.260914.bc12e3f`
- [x] MCP `tools/list` 注册 `arm` actuator
- [x] MCP schema 暴露基础 `arm` 控制动作

## 实机动作检查

- [ ] 机器人站立且已进入实时接收状态
- [ ] 获得现场许可后验证基础上肢控制
- [ ] 动作结束后调用 `disable` 或恢复安全姿态
