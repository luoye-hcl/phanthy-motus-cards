# 验收证据 —— joint_command

> 当前状态：`draft`。2026-09-04 已从运行中的 X2 MCP `tools/list` 核对工具名、类型和 schema。

## 离线校验

- [ ] `python3 -m json.tool metadata.json` 通过
- [ ] `metadata.json` 的 `mcp_tool` 与运行时 `tools/list` 一致

## 实机/画布验收

- [ ] Core 画布展示 `joint_command` 卡
- [ ] MCP `tools/list` 包含 `joint_command` 且类型为 `actuator`
- [ ] 仅确认工具显示；不执行会改变机器人状态的 action。

## 已知状态

- 高风险直接关节控制。必须使用真实 URDF 关节名和机械限位，且仅在保护措施、正确模式和用户明确授权均具备时调用。
