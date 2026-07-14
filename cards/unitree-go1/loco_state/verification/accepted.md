# 验收证据 —— loco_state

- **验收日期**:2026-07-14
- **验收方式**:core 网页监控页(DATA STREAMS 面板)呈现实时数据流,MT 验收通过。
- **后端**:factory(`robot_interface_high_level`,py3.7 .so),读真实 HighState。

## 离线测试

- `tests/test_mt_cards.py`:覆盖 loco_state(含 `mode_name`、`velocity_body_mps`)。
- `bash tests/run_all.sh`:全绿。

## 实机真实数据样本

站立态(mode=1 force_stand、机身高 0.30m):

```json
{
  "mode": 1, "mode_name": "force_stand",
  "gait_type": 0, "gait_name": "idle",
  "foot_raise_height_m": 0.0,
  "position_m": [0.023333, -0.030358, 0.29891],
  "body_height_m": 0.29921,
  "velocity_body_mps": {"forward": 4.2e-05, "lateral": 0.000413},
  "velocity_index_2_raw": -0.01313,
  "yaw_speed_rad_s": 0.00462,
  "timestamp_ms": 1784025258287,
  "control_level": "HIGHLEVEL"
}
```

阻尼态(mode=7 damp、机身降到 0.047m)——印证数据随真实状态变化:

```json
{ "mode": 7, "mode_name": "damp", "body_height_m": 0.04734 }
```
