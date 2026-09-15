# 验收证据 —— fall_alarm

- **当前状态**:`offline-green`(离线测试全绿 + 实机只读已验证;完整 JSON 样本待采后升 `accepted`)

## 离线测试

- `tests/test_mt_ext.py::TestFallAlarm`:
  - `test_ok` —— roll/pitch 在阈值内 → `status == "ok"`
  - `test_tilted` —— roll 0.8 rad ∈ [0.6warn, 1.2fall) → `status == "tilted"`
  - `test_fallen` —— pitch 1.4 rad ≥ 1.2fall → `status == "fallen"`
- 运行结果:`Ran 27 tests ... OK`(`test_mt_ext.py` 全绿,2026-07-15 本地复跑)。

## 实机只读验证(2026-07-13)

- 经 factory 后端(工厂 `robot_interface_high_level`,py3.7 .so,读真实 HighState.imu)实机只读调用 `{"action":"read"}`。
- 结果:狗姿态正常时返回 `status:"ok"`,倾角字段随真实 IMU 变化,判定逻辑生效。
- 参见 `luoye-hcl/go1-driver:docs/WORKLOG_2026-07-13.md`(增值卡"实机只读已验证真数据")。

## 待补(升 accepted 的条件)

- 狗上电后经 factory 后端现采一段**完整 JSON 返回样本**(`{status, roll_rad, pitch_rad, roll_deg, pitch_deg, ...}`)+ 采集时间/环境;
- 最好含两态对比(站立 `ok` vs 人为倾斜 `tilted`),印证随真实姿态变化;
- core 网页监控页 DATA STREAMS 面板呈现该卡数据流截图/记录。
- 齐备后:新增 `verification/accepted.md`、`metadata.json` 加 `accepted_date` 并把 `status` 改 `accepted`、`version` 递增、`CHANGELOG` 加条。
