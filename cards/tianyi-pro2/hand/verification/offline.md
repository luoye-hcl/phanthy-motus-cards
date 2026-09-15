# 验收证据 —— hand

> 本卡为 `draft` 阶段,驱动代码尚未实现。以下为待验收清单,待真机环境就绪后逐项补齐。

## 离线测试(待补)

- [ ] 编写 `tests/test_hand.py`:覆盖左右手 JointState 解析、6 DOF 字段映射、百分比范围检查
- [ ] `bash tests/run_all.sh` 全绿
- [ ] `python3 -m json.tool metadata.json` 通过

## 实机验收

- [✅] 真机环境:`ros2 topic echo /inspire_hand/state/left_hand` 确认字段与采样频率
- [✅] `ros2 topic hz /inspire_hand/state/left_hand` 量测频率,回填 `metadata.json.rate_hz`(实测 24.8 Hz)
- [✅] 验证 position/velocity/effort 确为百分比(0–1),而非物理单位
      - position 当前 ~1.0 表示手张开;velocity 静止时全 0;effort ~0.2 保持张开力
- [ ] `tools/preflight.py cards/tianyi-pro2/hand --host <天轶IP>` 全绿
- [ ] core 网页 DATA STREAMS 面板呈现该卡实时数据流
- [ ] 完整真实 JSON 样本(张开/握拳/受力多场景)
- [ ] MT 验收记录(人/日期/结论)

## 实机真实数据样本

> 采集日期: 2026-07-28
> 采集场景: 手张开静止状态
> 消息类型: `sensor_msgs/msg/JointState`
> 实测频率: 左 24.8 Hz / 右 24.8 Hz
> frame_id: `hand_left_link` / `hand_right_link`
> position 确认为百分比(0–1),当前 ~1.0 表示手张开

### /inspire_hand/state/left_hand (24.8 Hz)

```yaml
header:
  stamp:
    sec: 1785235595
    nanosec: 964754700
  frame_id: hand_left_link
name:
- '1'
- '2'
- '3'
- '4'
- '5'
- '6'
position:
- 0.9980000257492065
- 0.9860000014305115
- 1.0
- 0.9980000257492065
- 0.9789999723434448
- 0.9380000233650208
velocity:
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
effort:
- 0.21799999475479126
- 0.23499999940395355
- 0.2199999988079071
- 0.20900000631809235
- 0.21199999749660492
- 0.2329999953508377
```

### /inspire_hand/state/right_hand (24.8 Hz)

```yaml
header:
  stamp:
    sec: 1785235599
    nanosec: 356547013
  frame_id: hand_right_link
name:
- '1'
- '2'
- '3'
- '4'
- '5'
- '6'
position:
- 1.0
- 1.0
- 0.9919999837875366
- 1.0
- 0.9919999837875366
- 0.9660000205039978
velocity:
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
- 0.0
effort:
- 0.20999999344348907
- 0.19599999487400055
- 0.2409999966621399
- 0.19900000095367432
- 0.2199999988079071
- 0.25099998712539673
```
