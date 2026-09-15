# 验收证据 —— hand

## 离线检查

- [x] `metadata.json` JSON 语法通过
- [x] schema 包含六种语义手势及 `side=left/right`
- [x] schema 包含 `channel` 和 `value=0..1000`
- [x] schema 与 driver commit `bc12e3f` 的 `HandPlugin.get_tool()` 对齐

## 实机只读检查

- [x] Adam Jetson 运行镜像 `release.260914.bc12e3f`
- [x] MCP `tools/list` 注册 `hand` actuator
- [x] MCP schema 暴露全部动作、侧别和通道参数
- [x] `rt/handstate` 已并入 43 项 joints 状态流
- [ ] MCP `get_state` 返回左右手 6 个通道当前位置

## 实机动作检查

- [ ] 获得现场许可后验证单侧 `thumbs_up`
- [ ] 验证 `point`、`victory`、`rock` 等手势且另一只手目标保持不变
- [ ] 动作结束后恢复张开姿态并停止控制线程
