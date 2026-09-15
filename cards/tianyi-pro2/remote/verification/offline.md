# 验收证据 —— remote

> 本卡为 `draft` 阶段,驱动代码尚未实现。以下为待验收清单,待真机环境就绪后逐项补齐。
> 2026-07-28 已在真机执行 `ros2 topic echo/hz` 确认 topic 与字段,部分项已勾选。

## 离线测试(待补)

- [ ] 编写 `tests/test_remote.py`:覆盖 SbusData 与 Joy 解析、按键事件映射、摇杆值范围
- [ ] `bash tests/run_all.sh` 全绿
- [ ] `python3 -m json.tool metadata.json` 通过

## 实机验收(部分完成,2026-07-28)

- [x] 真机环境:`ros2 topic echo /sbus_data/event` 确认字段与值域(空闲态样本见文末)
- [x] `ros2 topic hz /sbus_data/event` 确认频率:实测 43.3 Hz
- [x] `ros2 topic echo /sbus_data` 确认 Joy 字段:12 轴 axes + 空 buttons 数组
- [x] `ros2 topic hz /sbus_data` 确认频率:实测 43.3 Hz(与 `/sbus_data/event` 同频)
- [x] 空闲态字段值域确认:`button_a`~`button_d`=-1,`button_e`~`button_g`=0,`button_h`=1(本样本 H 键按下),摇杆 x1/y1/x2/y2 全 -0.0
- [ ] 逐一按下 A/B/C/D 键,验证 button_a~d 在 -1/1 之间切换(待补按键态样本)
- [ ] 拨动 E/F/G/H,验证 button_e~h 与方向对应(待补拨片态样本)
- [ ] 推动摇杆,验证 x1/y1/x2/y2 在 -1.0~1.0 范围内变化(待补摇杆态样本)
- [ ] 验证 key_event_new/old 反映按键变化序列(待补按键态样本)
- [ ] `tools/preflight.py cards/tianyi-pro2/remote --host <天轶IP>` 全绿
- [ ] core 网页 DATA STREAMS 面板呈现该卡实时数据流
- [ ] 完整真实 JSON 样本(空闲态/按键态/摇杆推到位态多场景)
- [ ] MT 验收记录(人/日期/结论)

## 实机真实数据样本(2026-07-28 采集,空闲态)

### `/sbus_data`(sensor_msgs/Joy,43.3 Hz)

```yaml
header:
  stamp:
    sec: 1785235602
    nanosec: 364298612
  frame_id: ''
axes:
- -0.0
- -0.0
- -0.0
- -0.0
- -0.0
- -0.0
- 1.0
- -0.0
- -1.0
- -1.0
- -1.0
- -1.0
buttons: []
```

### `/sbus_data/event`(bodyctrl_msgs/SbusData,43.3 Hz,H 键按下)

```yaml
header:
  stamp:
    sec: 1785235603
    nanosec: 357007496
  frame_id: ''
key_event_new: 0
key_event_old: 0
button_a: -1
button_b: -1
button_c: -1
button_d: -1
button_e: 0
button_f: 0
button_g: 0
button_h: 1
x1: -0.0
y1: -0.0
x2: -0.0
y2: -0.0
```

### 聚合 JSON(对应上述样本)

```json
{
  "key_event": { "new": 0, "old": 0 },
  "buttons": { "a": -1, "b": -1, "c": -1, "d": -1, "e": 0, "f": 0, "g": 0, "h": 1 },
  "sticks": { "x1": -0.0, "y1": -0.0, "x2": -0.0, "y2": -0.0 },
  "timestamp_ms": 1785235603357,
  "control_level": "ANY"
}
```
