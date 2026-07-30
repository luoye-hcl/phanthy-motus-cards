# CHANGELOG — force_torque

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.1.0 — 2026-07-28 — huangchanglong

- 实机采集:确认 `/arm_6dof_left`、`/arm_6dof_right` 均为 100 Hz,与文档一致。
- 实机采集:确认消息类型 `geometry_msgs/msg/WrenchStamped`、frame_id `6dof_left_link` / `6dof_right_link`、单位(力 N,力矩 N·m)。
- 采集真实数据样本(机器人站立态,手臂自然下垂),写入 `verification/offline.md`。
- 验收清单更新:频率/字段/类型/frame_id/单位项打 ✅;坐标系正负号、preflight、网页面板、多场景样本、MT 记录项保留未完成。
- 状态保持 `draft`(驱动代码仍未写,离线测试未补)。

## v1.0.0 — 2026-07-28 — huangchanglong

- 首次收录。天轶2.0 Pro 双臂六维力只读传感器卡,订阅 `/arm_6dof_{left,right}`,100Hz。
- 状态 `draft`(驱动代码待写,未实机验收)。
- 接口字段以天轶2.0 SDK 文档(2026-05-21 版)为准;坐标系 X 前/Y 左/Z 上。
