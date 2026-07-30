# CHANGELOG — battery

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.1.0 — 2026-07-28 — huangchanglong

- 实机采集真实数据样本(2026-07-28),替换 v1.0.0 中的预估占位值。
- 实测频率:1.0 Hz(与文档预估一致)。
- 实测主电池:电压 52.7 V,电流 +2.1 A(放电态),功率 84 W。
- 实测小电池:电压/电流/功率全 0(可能未安装或未工作)。
- 实测 `battery_installed=0`、`battery_working=0`(字段位图语义待复核)。
- 实测 pg 状态位全 1,共 10 路(pg12a–pg5ab + pgrdc1/2 + pgheader + pgbutton2),比 v1.0.0 描述的 6 路多 4 路。
- 发现 `master_battery_power` 字段疑似为功率 W 而非电量 %,电流方向(正=放电)与 v1.0.0 描述(正=充电)不一致,均待后续复核。
- 同步更新 `verification/offline.md`:实机数据样本已替换,部分验收项已标 ✅。
- 状态保持 `draft`(驱动代码仍未实现,仅完成实机数据采集)。

## v1.0.0 — 2026-07-28 — huangchanglong

- 首次收录。天轶2.0 Pro 电池状态只读传感器卡,订阅 `/power/battery/status`,1Hz。
- 覆盖主电池/小电池的电压/电流/电量,以及充放电方向判断(电流负=放电,正=充电)。
- 含电源板 pg12a–pg5ab 六路供电状态位。
- 状态 `draft`(驱动代码待写,未实机验收)。
