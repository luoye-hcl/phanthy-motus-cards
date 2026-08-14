# CHANGELOG — system_health

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.0.0 — 2026-08-13 — huangchanglong

- 以驱动 `robotera-q5-driver` 为准重写本卡,与插件 `system_health.py` 的 get_tool()/build() 对齐。
- 数据源 `/motion_manager/motion_status`(`xbot_common_interfaces/msg/MotionStatus`),桥接输出 `/{ns}/q5/system_health`。
- 状态 `draft`(驱动已部署,待实机验收)。
