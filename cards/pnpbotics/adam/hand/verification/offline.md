# 验收证据 —— hand

## 离线检查

- [x] `metadata.json` JSON 语法通过
- [x] schema 仅包含基础 `hand` 控制动作
- [x] schema 包含 `side`、`channel` 和 `value=0..1000`
- [x] schema 与 `HandPlugin.get_tool()` 对齐

## 实机只读检查

- [x] Adam Jetson 运行镜像 `release.260914.bc12e3f`
- [x] MCP `tools/list` 注册 `hand` actuator
- [x] MCP schema 暴露基础动作、侧别和通道参数
- [x] `joints` 状态流仅包含 31 个 URDF 身体关节
- [x] `rt/handstate` 通过独立 `hands` / `hand_state` 数据流暴露 12 个硬件位置通道
- [ ] MCP `get_state` 返回左右手 6 个通道当前位置

## 实机动作检查

- [ ] 获得现场许可后验证基础张开、闭合和单通道控制
- [ ] 动作结束后恢复张开姿态并停止控制线程
