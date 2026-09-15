# battery —— 天轶2.0 Pro 电池状态(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `tianyi-pro2` |
| 卡片名(MCP 工具名) | `battery` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(未实机验收) |

## 能力

读取天轶2.0 Pro 电池状态,1 Hz 低频。包括大小电池的电压/电流/电量,以及充放电方向判断(电流负值=放电,正值=充电)。用于电量监控、低电量告警、充放电状态判断,供大模型或人监控机器人能源状态。

## 接口

- 输出 topic:
  - `/power/battery/status`  格式:`bodyctrl_msgs/msg/PowerBatteryStatus`
- 采样频率:`1` Hz(文档明确,2026-07-28 实测确认)
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`)

### 实测数据样本(2026-07-28,x86 192.168.41.1)

| 字段 | 实测值 | 说明 |
|---|---|---|
| `master_battery_voltage` | 52.7 V | 主电池电压 |
| `master_battery_current` | 2.1 A | 主电池电流(待机功耗) |
| `master_battery_power` | 84.0 % | 主电池电量 |
| `pg12a`–`pg5ab` | 全 1 | 各路供电正常 |

> 注:实机待机时 current 为正(2.1A),与文档"负=放电,正=充电"的描述矛盾。待机时不可能在充电,电流方向定义可能需修正为"正=放电"。待进一步确认。

### 字段(PowerBatteryStatus)

| 字段 | 含义 | 单位 |
|---|---|---|
| `header.stamp` | 采样时间戳 | ns |
| `battery_installed` | 电池安装状态:0x00 无 / 0x01 小电池 / 0x02 大电池 / 0x03 大小都有 | 位图 |
| `battery_working` | 工作中电池:0x10 大电池 / 0x01 小电池 | 位图 |
| `master_battery_voltage` | 主电池电压 | V |
| `master_battery_current` | 主电池电流(负=放电,正=充电) | A |
| `master_battery_power` | 主电池电量 | % |
| `little_battery_voltage` | 小电池电压 | V |
| `little_battery_current` | 小电池电流(负=放电,正=充电) | A |
| `little_battery_power` | 小电池电量 | % |
| `pg12a`–`pg5ab` | 电源板各路供电状态(0 低/1 高) | bit |

### 聚合后 JSON 输出结构

```json
{
  "installed": 3,
  "working": 16,
  "master": { "voltage": 48.0, "current": -2.5, "power": 85.0 },
  "little": { "voltage": 12.0, "current": 0.0, "power": 90.0 },
  "pg": { "12a":1, "12b":1, "12c":1, "12d":1, "5cd":1, "5ab":1 },
  "timestamp_ms": 1784025258226,
  "control_level": "ANY"
}
```

## 数据来源 / 实现位置

- 源仓库:`<待建 tianyi-pro2-driver>`
- 文件:`plugins/battery.py`  类:`BatteryStatePlugin`(待实现)
- 依赖:`ros_bridge.py`、`bodyctrl_msgs/msg/PowerBatteryStatus`
- 注册:`main.py` 插件聚合;驱动镜像/端口:待定

## 状态说明

- 离线:未实现(驱动代码待写)。
- 实机:未验收。待真机 `ros2 topic echo /power/battery/status` 确认字段后升 `offline-green`。
