# power_board —— 天轶2.0 Pro 电源板状态(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `tianyi-pro2` |
| 卡片名(MCP 工具名) | `power_board` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(未实机验收) |

## 能力

读取天轶2.0 Pro 电源板状态,1 Hz 低频。包括各部位(腰/臂A/臂B/腿A/腿B)MOS 温度(含极值)、各支路电流/电压(含极值)、母线电压(含极值)、软件/硬件版本号,以及电池电压/电流/电量汇总。用于电源系统健康监控、过温/过流告警、电压异常检测,供大模型或人监控机器人供电状态。

## 接口

- 输出 topic:
  - `/power/board/status`  格式:`bodyctrl_msgs/msg/PowerStatus`
- 采样频率:`1` Hz(文档明确,2026-07-28 实测确认)
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`)

### 实测数据样本(2026-07-28,x86 192.168.41.1)

| 字段 | 实测值 | 说明 |
|---|---|---|
| `waist_temp` | ~51°C | 腰部 MOS 温度 |
| `arm_a_temp` | ~55°C | 臂A MOS 温度 |
| `arm_b_temp` | ~53°C | 臂B MOS 温度 |
| `leg_a_temp` | ~58°C | 腿A MOS 温度(最高) |
| `leg_b_temp` | ~52°C | 腿B MOS 温度 |
| `software_version` | `26020120` | 软件版本号 |

### 字段(PowerStatus)

| 字段 | 含义 | 单位 |
|---|---|---|
| `header.stamp` | 采样时间戳 | ns |
| `waist_temp` | 腰部 MOS 温度 | °C |
| `arm_a_temp` | 臂A MOS 温度 | °C |
| `arm_b_temp` | 臂B MOS 温度 | °C |
| `leg_a_temp` | 腿A MOS 温度 | °C |
| `leg_b_temp` | 腿B MOS 温度 | °C |
| `*_temp_max` / `*_temp_min` | 各部位 MOS 温度极值 | °C |
| `arm_a_curr`–`head_curr` | 各支路电流(臂A/臂B/腿A/腿B/腰/头) | A |
| `*_curr_max` / `*_curr_min` | 各支路电流极值 | A |
| `arm_a_volt`–`bus_volt` | 各支路电压(臂A/臂B/腿A/腿B/腰/母线) | V |
| `*_volt_max` / `*_volt_min` | 各支路电压极值 | V |
| `software_version` | 软件版本 | — |
| `hardware_version` | 硬件版本 | — |
| `battery_voltage` | 电池电压 | V |
| `battery_current` | 电池电流 | A |
| `battery_power` | 电池电量 | % |

### 聚合后 JSON 输出结构

```json
{
  "temp": {
    "waist": 45.0, "arm_a": 42.0, "arm_b": 41.0, "leg_a": 43.0, "leg_b": 40.0,
    "max": { "waist": 50.0, "arm_a": 48.0, "arm_b": 47.0, "leg_a": 49.0, "leg_b": 46.0 },
    "min": { "waist": 25.0, "arm_a": 24.0, "arm_b": 23.0, "leg_a": 25.0, "leg_b": 22.0 }
  },
  "current": {
    "arm_a": 1.5, "arm_b": 1.4, "leg_a": 2.0, "leg_b": 1.9, "waist": 0.5, "head": 0.2,
    "max": { "arm_a": 3.0, "arm_b": 2.8, "leg_a": 4.0, "leg_b": 3.8, "waist": 1.0, "head": 0.4 },
    "min": { "arm_a": 0.1, "arm_b": 0.1, "leg_a": 0.2, "leg_b": 0.2, "waist": 0.05, "head": 0.01 }
  },
  "voltage": {
    "arm_a": 48.0, "arm_b": 48.0, "leg_a": 48.0, "leg_b": 48.0, "waist": 48.0, "bus": 48.0,
    "max": { "arm_a": 50.0, "arm_b": 50.0, "leg_a": 50.0, "leg_b": 50.0, "waist": 50.0, "bus": 50.0 },
    "min": { "arm_a": 46.0, "arm_b": 46.0, "leg_a": 46.0, "leg_b": 46.0, "waist": 46.0, "bus": 46.0 }
  },
  "version": { "software": "v1.0.0", "hardware": "v1.0" },
  "battery": { "voltage": 48.0, "current": -2.5, "power": 85.0 },
  "timestamp_ms": 1784025258226,
  "control_level": "ANY"
}
```

## 数据来源 / 实现位置

- 源仓库:`<待建 tianyi-pro2-driver>`
- 文件:`plugins/power_board.py`  类:`PowerBoardStatePlugin`(待实现)
- 依赖:`ros_bridge.py`、`bodyctrl_msgs/msg/PowerStatus`
- 注册:`main.py` 插件聚合;驱动镜像/端口:待定

## 状态说明

- 离线:未实现(驱动代码待写)。
- 实机:未验收。待真机 `ros2 topic echo /power/board/status` 确认字段后升 `offline-green`。
