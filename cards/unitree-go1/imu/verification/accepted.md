# 验收证据 —— imu

- **验收日期**:2026-07-14
- **验收方式**:core 网页监控页(DATA STREAMS 面板)呈现实时数据流,MT 验收通过。
- **后端**:factory(`robot_interface_high_level`,py3.7 .so),读真实 HighState.imu。

## 离线测试

- `tests/test_mt_cards.py`:覆盖 imu(含 `quaternion_wxyz`、`attitude_may_drift`)。
- `bash tests/run_all.sh`:全绿。

## 实机真实数据样本

站立态(z 轴重力 ≈9.64、IMU 温度 79℃):

```json
{
  "quaternion_wxyz": [0.999914, -0.012749, 0.001055, -0.002857],
  "gyroscope_rad_s": [0.005946, 0.005979, -0.001772],
  "accelerometer_m_s2": [-0.039504, -0.246603, 9.642648],
  "rpy_rad": [-0.025506, 0.002037, -0.005741],
  "temperature_c": 79,
  "attitude_may_drift": true,
  "timestamp_ms": 1784025258163,
  "control_level": "HIGHLEVEL"
}
```
