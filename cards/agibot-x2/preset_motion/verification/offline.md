# 验收证据 —— preset_motion

> 当前状态：`draft`。2026-09-04 已从运行中的 X2 MCP `tools/list` 核对工具名、类型和 schema。

## 离线校验

- [ ] `python3 -m json.tool metadata.json` 通过
- [ ] `metadata.json` 的 `mcp_tool` 与运行时 `tools/list` 一致

## 实机/画布验收

- [ ] Core 画布展示 `preset_motion` 卡
- [ ] MCP `tools/list` 包含 `preset_motion` 且类型为 `actuator`
- [ ] 仅确认工具显示；不执行会改变机器人状态的 action。

## 已知状态

- 会触发真实肢体动作。`raise_hand`、`wave_hand`、`shake_hand`、`flying_kiss_hand`、`clap_hand`、`clipfist`、`salute`、`turn_wave_hand` 必须传 `area=left_hand` 或 `right_hand`，否则 vendor 返回 `code=1`。
