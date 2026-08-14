# CHANGELOG — hand_gesture

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.0.0 — 2026-08-13 — huangchanglong

- 以驱动 `robotera-q5-driver` 为准重写本卡,与插件 `hand_gesture.py` 的 get_tool()/dispatch() 对齐。
- 命令 topic `/hand_controller/commands`(`xbot_common_interfaces/msg/HybridJointCommand`)。
- 状态 `draft`(驱动已部署,待实机验收)。
