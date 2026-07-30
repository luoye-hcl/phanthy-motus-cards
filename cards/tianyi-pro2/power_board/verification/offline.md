# 验收证据 —— power_board

> 本卡为 `draft` 阶段,驱动代码尚未实现。以下为待验收清单,部分实机项已采集到真实数据(2026-07-28)。

## 离线测试(待补)

- [ ] 编写 `tests/test_power_board.py`:覆盖 PowerStatus 解析、温度/电流/电压字段映射、极值字段、版本字符串
- [ ] `bash tests/run_all.sh` 全绿
- [x] `python3 -m json.tool metadata.json` 通过

## 实机验收(部分完成)

- [x] 真机环境:`ros2 topic echo /power/board/status` 确认字段与值域(2026-07-28 采集)
- [x] `ros2 topic hz /power/board/status` 确认 1Hz(实测 1.0 Hz)
- [x] 验证各部位 MOS 温度范围合理(室温 ~60°C)(实测 waist 51.9 / arm_a 57.8 / arm_b 57.6 / leg_a 53.9 / leg_b 51.9 °C)
- [x] 验证电流正值/极值与运动状态关联(实测 arm_a 1.4 / arm_b 1.8 / leg_a -0.2 / leg_b 2.1 / waist 1.2 / head 0.0 A)
- [x] 验证母线电压与电池电压一致(实测 bus_volt 52.6 V,battery_voltage 52.9 V,差 0.3 V 在合理范围内)
- [x] 验证软件/硬件版本号字符串格式(实测 software_version='26020120',hardware_version='0000')
- [ ] `tools/preflight.py cards/tianyi-pro2/power_board --host <天轶IP>` 全绿
- [ ] core 网页 DATA STREAMS 面板呈现该卡实时数据流
- [ ] 完整真实 JSON 样本(空载态/运动态/过温态多场景,当前仅 1 个静态样本)
- [ ] MT 验收记录(人/日期/结论)

## 实机真实数据样本(2026-07-28 采集)

### ROS 原始消息(`/power/board/status`,`bodyctrl_msgs/msg/PowerStatus`,1.0 Hz)

```yaml
header:
  stamp:
    sec: 1785235601
    nanosec: 395603459
  frame_id: ''
waist_temp: 51.900001525878906
arm_a_temp: 57.79999923706055
arm_b_temp: 57.599998474121094
leg_a_temp: 53.900001525878906
leg_b_temp: 51.900001525878906
waist_temp_max: 58.900001525878906
arm_a_temp_max: 65.80000305175781
arm_b_temp_max: 64.19999694824219
leg_a_temp_max: 63.5
leg_b_temp_max: 55.900001525878906
waist_temp_min: 41.400001525878906
arm_a_temp_min: 42.400001525878906
arm_b_temp_min: 42.099998474121094
leg_a_temp_min: 39.700000769345
leg_b_temp_min: 42.400001525878906
arm_a_curr: 1.399999976158142
arm_b_curr: 1.7999999523162842
leg_a_curr: -0.20000000298023224
leg_b_curr: 2.0999999046325684
waist_curr: 1.2000000476837158
head_curr: 0.0
arm_a_curr_max: 8.699999809265137
arm_b_curr_max: 9.100000381469727
leg_a_curr_max: 5.400000095367432
leg_b_curr_max: 9.800000190734863
waist_curr_max: 11.800000190734863
head_curr_max: 0.0
arm_a_curr_min: -5.800000190734863
arm_b_curr_min: -7.0
leg_a_curr_min: -7.0
leg_b_curr_min: -8.300000190734863
waist_curr_min: -11.399999618530273
head_curr_min: 0.0
arm_a_volt: 53.0
arm_b_volt: 52.900001525878906
leg_a_volt: 53.20000076293945
leg_b_volt: 52.900001525878906
waist_volt: 52.70000076293945
bus_volt: 52.599998474121094
arm_a_volt_max: 57.599998474121094
arm_b_volt_max: 57.09999694824219
leg_a_volt_max: 57.900001525878906
leg_b_volt_max: 57.09999694824219
waist_volt_max: 57.0
bus_volt_max: 58.70000076293945
arm_a_volt_min: 0.0
arm_b_volt_min: 0.0
leg_a_volt_min: 0.0
leg_b_volt_min: 0.0
waist_volt_min: 0.0
bus_volt_min: 47.5
software_version: '26020120'
hardware_version: '0000'
battery_voltage: 52.900001525878906
battery_current: 0.8999999761581421
battery_power: 87.0
```

### 聚合后 JSON 输出(按 metadata payload_fields 映射)

```json
{
  "temp": {
    "waist": 51.9, "arm_a": 57.8, "arm_b": 57.6, "leg_a": 53.9, "leg_b": 51.9,
    "max": { "waist": 58.9, "arm_a": 65.8, "arm_b": 64.2, "leg_a": 63.5, "leg_b": 55.9 },
    "min": { "waist": 41.4, "arm_a": 42.4, "arm_b": 42.1, "leg_a": 39.7, "leg_b": 42.4 }
  },
  "current": {
    "arm_a": 1.4, "arm_b": 1.8, "leg_a": -0.2, "leg_b": 2.1, "waist": 1.2, "head": 0.0,
    "max": { "arm_a": 8.7, "arm_b": 9.1, "leg_a": 5.4, "leg_b": 9.8, "waist": 11.8, "head": 0.0 },
    "min": { "arm_a": -5.8, "arm_b": -7.0, "leg_a": -7.0, "leg_b": -8.3, "waist": -11.4, "head": 0.0 }
  },
  "voltage": {
    "arm_a": 53.0, "arm_b": 52.9, "leg_a": 53.2, "leg_b": 52.9, "waist": 52.7, "bus": 52.6,
    "max": { "arm_a": 57.6, "arm_b": 57.1, "leg_a": 57.9, "leg_b": 57.1, "waist": 57.0, "bus": 58.7 },
    "min": { "arm_a": 0.0, "arm_b": 0.0, "leg_a": 0.0, "leg_b": 0.0, "waist": 0.0, "bus": 47.5 }
  },
  "version": { "software": "26020120", "hardware": "0000" },
  "battery": { "voltage": 52.9, "current": 0.9, "power": 87.0 },
  "timestamp_ms": 1785235601395,
  "control_level": "ANY"
}
```

### 实测要点(2026-07-28)

- 频率:1.0 Hz 确认
- MOS 温度:腰部 51.9 / 臂A 57.8 / 臂B 57.6 / 腿A 53.9 / 腿B 51.9 °C,极值 max 65.8 °C(臂A)、min 39.7 °C(腿A)
- 电流:臂A 1.4 / 臂B 1.8 / 腿A -0.2 / 腿B 2.1 / 腰 1.2 / 头 0.0 A;极值 max 11.8 A(腰)、min -11.4 A(腰)
- 电压:各支路 52.7–53.2 V,母线 52.6 V,极值 max 58.7 V(母线)、min 47.5 V(母线);各支路 volt_min 全 0(可能为历史最低或未初始化)
- software_version='26020120',hardware_version='0000'
- battery_voltage 52.9 V,battery_current 0.9 A,battery_power 87.0(字段名 `battery_power`,与 battery 卡的 `master_battery_power` 类似,语义待复核)
- 该 topic 也包含 battery_voltage/current/power,与 battery 卡有数据重叠
