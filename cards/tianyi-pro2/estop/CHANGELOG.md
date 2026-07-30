# CHANGELOG — estop

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.1.0 — 2026-07-28 — huangchanglong

- 实机采集真实数据样本(2026-07-28),替换 v1.0.0 中的预估占位值。
- **频率修正:实测 19.2 Hz**,远高于 v1.0.0 文档预估的 1 Hz;`metadata.json` 的 `rate_hz` 已从 1.0 更新为 19.2,`mcp_tool.description` 同步修正。
- 实测静态样本(正常态):`is_estop=false`、`is_remote_estop=false`、`is_power_on=true`、`work_time=0`。
- 发现 ROS 消息中 `is_estop`/`is_remote_estop`/`is_power_on` 字段为嵌套结构 `{data: bool}`,聚合到 JSON 时应解包为顶层 bool。
- 同步更新 `verification/offline.md`:实机数据样本已替换,部分验收项已标 ✅。
- 状态保持 `draft`(驱动代码仍未实现,仅完成实机数据采集;按键触发/断电等多场景测试待补)。

## v1.0.0 — 2026-07-28 — huangchanglong

- 首次收录。天轶2.0 Pro 急停/按键状态只读传感器卡,订阅 `/power/board/key_status`,1Hz。
- 覆盖急停按键(`is_estop`)、软急停(`is_remote_estop`)、电源供电(`is_power_on`)及累计工作时间。
- 状态 `draft`(驱动代码待写,未实机验收)。
