# 验收证据 —— estop

> 本卡为 `draft` 阶段,驱动代码尚未实现。以下为待验收清单,部分实机项已采集到真实数据(2026-07-28)。

## 离线测试(待补)

- [ ] 编写 `tests/test_estop.py`:覆盖 PowerBoardKeyStatus 解析、bool 字段映射、work_time 累计
- [ ] `bash tests/run_all.sh` 全绿
- [x] `python3 -m json.tool metadata.json` 通过

## 实机验收(部分完成)

- [x] 真机环境:`ros2 topic echo /power/board/key_status` 确认字段与值域(2026-07-28 采集)
- [x] `ros2 topic hz /power/board/key_status` 确认频率(实测 **19.2 Hz**,远高于文档预估的 1 Hz)
- [ ] 物理按下急停按键,验证 `is_estop` 变为 true(实测静态样本 `is_estop=false`,未做按键触发测试)
- [ ] 触发软急停,验证 `is_remote_estop` 变为 true(实测静态样本 `is_remote_estop=false`,未做触发测试)
- [ ] 断开电源,验证 `is_power_on` 变为 false(实测静态样本 `is_power_on=true`,未做断电测试)
- [ ] 验证 `work_time` 随时间递增(实测 `work_time=0`,可能刚启动未累计,需后续复核)
- [ ] `tools/preflight.py cards/tianyi-pro2/estop --host <天轶IP>` 全绿
- [ ] core 网页 DATA STREAMS 面板呈现该卡实时数据流
- [ ] 完整真实 JSON 样本(正常态/急停态/断电态多场景,当前仅正常态)
- [ ] MT 验收记录(人/日期/结论)

## 实机真实数据样本(2026-07-28 采集)

### ROS 原始消息(`/power/board/key_status`,`bodyctrl_msgs/msg/PowerBoardKeyStatus`,19.2 Hz)

```yaml
header:
  stamp:
    sec: 1785234199
    nanosec: 624752073
  frame_id: ''
work_time: 0
is_estop:
  data: false
is_remote_estop:
  data: false
is_power_on:
  data: true
```

### 聚合后 JSON 输出(按 metadata payload_fields 映射)

```json
{
  "work_time": 0,
  "is_estop": false,
  "is_remote_estop": false,
  "is_power_on": true,
  "timestamp_ms": 1785234199624,
  "control_level": "ANY"
}
```

### 实测要点(2026-07-28)

- **频率:19.2 Hz**(重要修正:v1.0.0 文档预估为 1 Hz,实测远高于预估,需在 CARD.md 和 metadata 中同步修正)
- `is_estop=false`(急停按键未按下,正常态)
- `is_remote_estop=false`(软急停未触发,正常态)
- `is_power_on=true`(电源已上电,正常态)
- `work_time=0`(可能刚启动未累计,或字段语义为本次上电后工作时间,需后续复核)
- 注意:ROS 消息中 `is_estop`/`is_remote_estop`/`is_power_on` 字段为嵌套结构 `{data: bool}`,聚合到 JSON 时应解包为顶层 bool
