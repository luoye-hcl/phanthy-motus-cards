# CHANGELOG — fall_alarm

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.0.0 — 2026-07-15 — luoye-hcl

- 首次收录。Go1 跌倒/侧翻告警只读传感器卡,10Hz,`/{ns}/state/fall_alarm`。
- 由 IMU roll/pitch 幅度判定 `ok`/`tilted`/`fallen`,阈值可配(`tilt_warn_rad`≈34° / `fall_rad`≈69°)。
- 离线测试全绿(`test_mt_ext.py::TestFallAlarm` 三档阈值);2026-07-13 实机只读已验证姿态正常返回 `ok`,完整 JSON 样本待采后升 `accepted`。
