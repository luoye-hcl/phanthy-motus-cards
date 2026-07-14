# CHANGELOG — imu

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.0.0 — 2026-07-14 — luoye-hcl

- 首次收录。Go1 IMU 只读传感器卡,20Hz,`/{ns}/state/imu`。
- 实机验收通过(真实四元数/温度 79℃/加速度 z≈9.64,core 网页数据流正常)。
