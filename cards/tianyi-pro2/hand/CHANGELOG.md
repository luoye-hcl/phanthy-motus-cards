# CHANGELOG — hand

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.1.0 — 2026-07-28 — huangchanglong

- 实机采集:左右手状态 topic `/inspire_hand/state/{left,right}_hand` 实测频率 24.8 Hz,回填 `metadata.json.rate_hz`。
- 确认 position/velocity/effort 为百分比(0–1):position 当前 ~1.0 表示手张开,velocity 静止全 0,effort ~0.2 保持张开力。
- 采集真实数据样本(手张开静止状态),录入 `verification/offline.md`。
- frame_id: `hand_left_link` / `hand_right_link`;消息类型 `sensor_msgs/msg/JointState`。

## v1.0.0 — 2026-07-28 — huangchanglong

- 首次收录。天轶2.0 Pro 仿生手状态只读传感器卡,订阅 `/inspire_hand/state/{left,right}_hand` 两路 topic。
- 状态 `draft`(驱动代码待写,未实机验收)。
- 接口字段以天轶2.0 SDK 文档(2026-05-21 版)为准;position/velocity/effort 均为百分比(0–1)。
