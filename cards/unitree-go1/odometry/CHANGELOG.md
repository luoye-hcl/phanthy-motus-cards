# CHANGELOG — odometry

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.0.0 — 2026-07-15 — luoye-hcl

- 首次收录。Go1 里程计只读传感器卡,5Hz,`/{ns}/state/odometry`(HIGHLEVEL 才有 position)。
- 报告当前 position/yaw、累计总路程、相对起点位移;`reset_origin` 动作重置起点(经 MCP 可调,UI 不出按钮)。
- 离线测试全绿(`test_mt_ext.py::TestOdometry`:结构/reset_origin/只读工具/里程累加);2026-07-13 实机只读已验证读取 OK,完整 JSON 样本待采后升 `accepted`。
