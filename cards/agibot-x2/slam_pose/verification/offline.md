# 验收证据 —— slam_pose

> 当前状态：`draft`。2026-09-04 已从运行中的 X2 MCP `tools/list` 核对工具名、类型和 schema。

## 离线校验

- [ ] `python3 -m json.tool metadata.json` 通过
- [ ] `metadata.json` 的 `mcp_tool` 与运行时 `tools/list` 一致

## 实机/画布验收

- [ ] Core 画布展示 `slam_pose` 卡
- [ ] MCP `tools/list` 包含 `slam_pose` 且类型为 `sensor`
- [ ] 仅调用只读查询或订阅输出，确认真实数据。

## 已知状态

- 运行时 MCP 已注册，但 `config.yaml` 的 `slam.enabled` 为 false；以实际注册为准，数据待验收。
