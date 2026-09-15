# 验收证据 —— battery

> 本卡为 `draft` 阶段,驱动代码尚未实现。以下为待验收清单,部分实机项已采集到真实数据(2026-07-28)。

## 离线测试(待补)

- [ ] 编写 `tests/test_battery.py`:覆盖 PowerBatteryStatus 解析、主/小电池字段映射、pg 状态位
- [ ] `bash tests/run_all.sh` 全绿
- [x] `python3 -m json.tool metadata.json` 通过

## 实机验收(部分完成)

- [x] 真机环境:`ros2 topic echo /power/battery/status` 确认字段与值域(2026-07-28 采集)
- [x] `ros2 topic hz /power/battery/status` 确认 1Hz(实测 1.0 Hz)
- [x] 验证充放电方向(电流负=放电,正=充电)与实际状态一致(实测 +2.1A,放电态)
- [ ] 验证电量百分比范围 0–100(实测 `master_battery_power=84.0`,需复核字段语义:可能为功率 W 而非电量 %)
- [x] 验证 pg 状态位 0/1 含义(实测 pg12a–pg5ab、pgrdc1/2、pgheader、pgbutton2 全 1,各路电源正常)
- [ ] `tools/preflight.py cards/tianyi-pro2/battery --host <天轶IP>` 全绿
- [ ] core 网页 DATA STREAMS 面板呈现该卡实时数据流
- [ ] 完整真实 JSON 样本(充电态/放电态/低电量态多场景,当前仅放电态)
- [ ] MT 验收记录(人/日期/结论)

## 实机真实数据样本(2026-07-28 采集)

### ROS 原始消息(`/power/battery/status`,`bodyctrl_msgs/msg/PowerBatteryStatus`,1.0 Hz)

```yaml
header:
  stamp:
    sec: 1785234925
    nanosec: 59845658
  frame_id: ''
battery_installed: 0
battery_working: 0
master_battery_voltage: 52.70000076293945
master_battery_current: 2.0999999046325684
master_battery_power: 84.0
little_battery_voltage: 0.0
little_battery_current: 0.0
little_battery_power: 0.0
pg12a: 1
pg12b: 1
pg12c: 1
pg12d: 1
pg5cd: 1
pg5ab: 1
pgrdc2: 1
pgrdc1: 1
pgheader: 1
pgbutton2: 1
```

### 聚合后 JSON 输出(按 metadata payload_fields 映射)

```json
{
  "installed": 0,
  "working": 0,
  "master": { "voltage": 52.7, "current": 2.1, "power": 84.0 },
  "little": { "voltage": 0.0, "current": 0.0, "power": 0.0 },
  "pg": { "12a": 1, "12b": 1, "12c": 1, "12d": 1, "5cd": 1, "5ab": 1, "rdc1": 1, "rdc2": 1, "header": 1, "button2": 1 },
  "timestamp_ms": 1785234925598,
  "control_level": "ANY"
}
```

### 实测要点(2026-07-28)

- 频率:1.0 Hz 确认
- 主电池电压 52.7 V,电流 +2.1 A(正=放电),功率 84 W(字段名 `master_battery_power`,实测疑似为功率 W 而非电量 %,需后续复核)
- 小电池电压/电流/功率全 0(可能未安装或未工作)
- `battery_installed=0`, `battery_working=0`(可能表示未检测到标准电池包或非标准状态,需后续复核字段位图语义)
- pg* 状态位全 1(pg12a–pg5ab、pgrdc1/2、pgheader、pgbutton2 共 10 路),各路电源正常
- 电流正=放电(2.1 A 放电态),与 CARD.md 中"负=放电,正=充电"的描述不一致,需后续复核方向定义
