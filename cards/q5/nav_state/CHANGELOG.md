# CHANGELOG — nav_state

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.0.0 — 2026-08-13 — huangchanglong

- 以驱动 `robotera-q5-driver` 为准重写本卡,与插件 `nav_state.py` 的 get_tool()/build() 对齐。
- 数据源 `/era_nav/nav_status`(`std_msgs/msg/String`),桥接输出 `/{ns}/q5/nav_state`。
- 状态 `draft`(驱动已部署,待实机验收)。
