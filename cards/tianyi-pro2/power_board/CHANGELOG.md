# CHANGELOG — power_board

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.1.0 — 2026-07-28 — huangchanglong

- 实机采集真实数据样本(2026-07-28),替换 v1.0.0 中的预估占位值(全 0)。
- 实测频率:1.0 Hz(与文档预估一致)。
- 实测 MOS 温度:waist 51.9 / arm_a 57.8 / arm_b 57.6 / leg_a 53.9 / leg_b 51.9 °C,极值 max 65.8 °C(arm_a)、min 39.7 °C(leg_a)。
- 实测电流:arm_a 1.4 / arm_b 1.8 / leg_a -0.2 / leg_b 2.1 / waist 1.2 / head 0.0 A,极值 max 11.8 A(waist)、min -11.4 A(waist)。
- 实测电压:各支路 52.7–53.2 V,母线 52.6 V,极值 max 58.7 V(bus)、min 47.5 V(bus);各支路 volt_min 全 0(待复核)。
- 实测版本:software_version='26020120',hardware_version='0000'。
- 实测电池汇总:battery_voltage 52.9 V,battery_current 0.9 A,battery_power 87.0。
- 同步更新 `verification/offline.md`:实机数据样本已替换,部分验收项已标 ✅。
- 状态保持 `draft`(驱动代码仍未实现,仅完成实机数据采集)。

## v1.0.0 — 2026-07-28 — huangchanglong

- 首次收录。天轶2.0 Pro 电源板状态只读传感器卡,订阅 `/power/board/status`,1Hz。
- 覆盖各部位(腰/臂A/臂B/腿A/腿B)MOS 温度(含极值)、各支路电流/电压(含极值)、母线电压(含极值)、软/硬版本号、电池汇总。
- 状态 `draft`(驱动代码待写,未实机验收)。
