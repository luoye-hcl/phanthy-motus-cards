# 验收证据 —— motor

> 本卡为 `draft` 阶段,驱动代码尚未实现。以下为待验收清单,部分实机数据已采集(2026-07-28)。

## 离线测试(待补)

- [ ] 编写 `tests/test_motor.py`:覆盖四路 topic 解析、关节ID映射、error 码识别
- [ ] `bash tests/run_all.sh` 全绿
- [x] `python3 -m json.tool metadata.json` 通过(2026-07-28)

## 实机验收(部分完成)

- [x] 真机环境:`ros2 topic echo /head/status` 确认字段与采样频率(2026-07-28)
- [x] `ros2 topic hz /head/status` 量测频率,回填 `metadata.json.rate_hz`(2026-07-28,四路实测:head=400Hz, waist/arm/leg=500Hz)
- [ ] `tools/preflight.py cards/tianyi-pro2/motor --host <天轶IP>` 全绿
- [ ] core 网页 DATA STREAMS 面板呈现该卡实时数据流
- [ ] 完整真实 JSON 样本(站立/运动/异常多场景)—— 已采集站立静姿单场景,运动/异常待补
- [ ] MT 验收记录(人/日期/结论)

## 实机真实数据样本(2026-07-28 采集)

采集场景:站立静姿。四路 topic 原始 `ros2 topic echo` 输出(YAML 格式)片段如下。

### /head/status (400 Hz)

```yaml
header:
  stamp:
    sec: 1785235584
    nanosec: 389225402
  frame_id: head
status:
- name: 1
  pos: 0.045701026916503906
  speed: -0.0009613037109375
  current: -0.0091552734375
  temperature: 43.0
  error: 0
- name: 2
  pos: 0.01841592788696289
  speed: 0.0003204345703125
  current: 0.0152587890625
  temperature: 47.0
  error: 0
- name: 3
  pos: -0.11542558670043945
  speed: 0.0163421630859375
  current: -0.0091552734375
  temperature: 46.0
  error: 0
```

### /waist/status (500 Hz)

```yaml
header:
  stamp:
    sec: 1785235585
    nanosec: 354897663
  frame_id: waist
status:
- name: 31
  pos: 0.02660497836768627
  speed: 0.0
  current: 0.0
  temperature: 0.0
  error: 0
- name: 32
  pos: 0.08870723098516464
  speed: 0.0
  current: 0.0
  temperature: 0.0
  error: 0
```

> 注:关节 32(Waist Pitch)确认存在!但 `temperature`/`current`/`speed` 全为 0,推测 waist 模组待机或未上电,需上电后复测。

### /arm/status (500 Hz)

```yaml
header:
  stamp:
    sec: 1785235587
    nanosec: 390328299
  frame_id: arm
status:
- name: 11
  pos: -0.03161430358886719
  speed: -0.0003204345703125
  current: 0.0885009765625
  temperature: 38.0
  error: 0
- name: 12
  pos: 0.05771589279174805
  speed: -0.0003204345703125
  current: 0.0152587890625
  temperature: 38.0
  error: 0
- name: 13
  pos: 0.08659791946411133
  speed: 0.0003204345703125
  current: -0.0030517578125
  temperature: 35.0
  error: 0
- name: 14
  pos: -0.1350860595703125
  speed: -0.0003204345703125
  current: -0.0274658203125
  temperature: 33.0
  error: 0
- name: 15
  pos: -4.8160552978515625e-05
  speed: 0.0003204345703125
  current: 0.0152587890625
  temperature: 35.0
  error: 0
- name: 16
  pos: -0.059314727783203125
  speed: -0.0003204345703125
  current: -0.0274658203125
  temperature: 37.0
  error: 0
- name: 17
  pos: -0.18513059616088867
  speed: -0.0009613037109375
  current: -0.0030517578125
  temperature: 34.0
  error: 0
- name: 21
  pos: 0.0421605110168457
  speed: 0.0009613037109375
  current: -0.0701904296875
  temperature: 36.0
  error: 0
- name: 22
  pos: 0.0004558563232421875
  speed: -0.0003204345703125
  current: -0.1068115234375
  temperature: 37.0
  error: 0
- name: 23
  pos: 0.06135988235473633
  speed: 0.0003204345703125
  current: 0.0030517578125
  temperature: 34.0
  error: 0
- name: 24
  pos: -0.2658815383911133
  speed: 0.0003204345703125
  current: -0.0457763671875
  temperature: 32.0
  error: 0
- name: 25
  pos: -0.11536073684692383
  speed: 0.0003204345703125
  current: 0.0091552734375
  temperature: 35.0
  error: 0
- name: 26
  pos: 0.019482135772705078
  speed: 0.0003204345703125
  current: 0.0030517578125
  temperature: 37.0
  error: 0
- name: 27
  pos: -0.05234479904174805
  speed: -0.0009613037109375
  current: 0.0030517578125
  temperature: 35.0
  error: 0
```

### /leg/status (500 Hz)

```yaml
header:
  stamp:
    sec: 1785235590
    nanosec: 390594575
  frame_id: leg
status:
- name: 51
  pos: -0.0875447615981102
  speed: 0.0
  current: 0.0
  temperature: 0.0
  error: 0
- name: 52
  pos: -0.2633053958415985
  speed: 0.0
  current: 0.0
  temperature: 0.0
  error: 0
```

> 注:leg 与 waist 相同,`temperature`/`current`/`speed` 全为 0,推测腿部模组待机或未上电,需上电后复测。

## 关键发现(2026-07-28)

1. **四路 topic 频率不一致**:head=400Hz, waist/arm/leg=500Hz。`metadata.json.rate_hz` 设为 null,在 `topic_out` 各项中标注各自频率。
2. **waist 关节 32 确认存在**:MotorName 文档里的 Waist Pitch(32)在实机数据中出现,但本样本中 temp/current/speed 为 0,需上电后复测以确认其在通电状态下是否正常输出。
3. **leg 与 waist 待机态**:两路 temp/current/speed 全 0,只有 pos 有值。需在机器人上电、腿部进入工作状态后复测,以采集有效的速度/电流/温度数据。
4. **字段结构与文档一致**:name/pos/speed/current/temperature/error 五字段齐全,所有关节 error=0(无故障)。
5. **温度范围合理(已上电部位)**:head 43–47℃,arm 32–38℃,均在正常 MOS 工作温度区间。

## 未完成项

- 驱动代码 `plugins/motor.py` 未实现
- `tests/test_motor.py` 未编写
- `tools/preflight.py` 卡级预检未跑
- core 网页 DATA STREAMS 面板未对接
- 运动场景 / 异常场景数据未采集
- MT 验收记录未生成
- waist 上电后复测、leg 上电后复测
