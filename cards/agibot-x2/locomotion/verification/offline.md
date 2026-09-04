# 验收证据 —— locomotion

> 当前状态：`draft`。2026-09-04 已从运行中的 X2 MCP `tools/list` 核对工具名、类型和 schema。

## 离线校验

- [ ] `python3 -m json.tool metadata.json` 通过
- [ ] `metadata.json` 的 `mcp_tool` 与运行时 `tools/list` 一致

## 实机/画布验收

- [ ] Core 画布展示 `locomotion` 卡
- [ ] MCP `tools/list` 包含 `locomotion` 且类型为 `actuator`
- [ ] 仅确认工具显示；不执行会改变机器人状态的 action。

## 已知状态

- `set_velocity` 会导致真实移动，且未注册时会自动注册输入源；仅在现场清空、FSM 正确且用户额外确认后调用。
