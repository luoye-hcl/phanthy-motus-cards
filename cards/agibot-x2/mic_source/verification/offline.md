# 验收证据 —— mic_source

> 当前状态：`draft`。2026-09-04 已从运行中的 X2 MCP `tools/list` 核对工具名、类型和 schema。

## 离线校验

- [ ] `python3 -m json.tool metadata.json` 通过
- [ ] `metadata.json` 的 `mcp_tool` 与运行时 `tools/list` 一致

## 实机/画布验收

- [ ] Core 画布展示 `mic_source` 卡
- [ ] MCP `tools/list` 包含 `mic_source` 且类型为 `actuator`
- [ ] 仅确认工具显示；不执行会改变机器人状态的 action。

## 已知状态

- `get` 为只读查询；`set` 改变硬件输入配置，需额外授权。
