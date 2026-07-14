# 验收证据 —— feet

- **验收日期**:2026-07-14
- **验收方式**:core 网页监控页(DATA STREAMS 面板)呈现该卡实时数据流,MT 验收通过。
- **后端**:factory(工厂 `robot_interface_high_level`,py3.7 .so),读真实 HighState。
- **链路**:驱动(:15704 真数据)→ ros_republisher 容器(`--ipc=host`,轮询 MCP 发 ROS topic)→ core 订阅显示。

## 离线测试

- `tests/test_mt_cards.py`:覆盖 feet(`order[0]=="FR"`、含 `foot_force_raw`)。
- `bash tests/run_all.sh`:全绿。

## 实机真实数据样本

站立态(足底力饱满、含足端位姿):

```json
{
  "order": ["FR", "FL", "RR", "RL"],
  "foot_force_raw": [246, 273, 251, 274],
  "position_to_body": [
    {"x": 0.17989, "y": -0.14397, "z": -0.29901},
    {"x": 0.18093, "y": 0.14857,  "z": -0.29760},
    {"x": -0.19722, "y": -0.13083, "z": -0.30044},
    {"x": -0.19693, "y": 0.13592,  "z": -0.29981}
  ],
  "timestamp_ms": 1784025258226,
  "control_level": "HIGHLEVEL"
}
```

阻尼态(收腿不承重,足底力显著变小)——印证数据随真实状态变化:

```json
{ "order": ["FR","FL","RR","RL"], "foot_force_raw": [27, 53, 44, 69] }
```
