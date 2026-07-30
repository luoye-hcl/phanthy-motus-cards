# 实现来源(source)—— power_board

- **源仓库**:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 `unitree/tiangong_pro/` 代码)
- **文件路径**:`plugins/power_board.py`(待实现)
- **类名**:`PowerBoardStatePlugin`(待实现)
- **公共依赖**:`ros_bridge.py`(ROS2 订阅桥)、`bodyctrl_msgs/msg/PowerStatus`
- **注册位置**:`main.py` 插件聚合(待实现);驱动镜像/端口:待定
- **MCP 协议**:JSON-RPC 2.0 over HTTP,注册到 Agent Core

## 数据源 topic(来自天轶2.0 SDK 文档)

| ROS2 topic | 频率 | 说明 |
|---|---|---|
| `/power/board/status` | 1 Hz | 电源板各部位温度/电流/电压(含极值),软/硬版本,电池汇总 |

## PowerStatus.msg 字段

### 温度(°C)

| 字段 | 含义 |
|---|---|
| `waist_temp` | 腰部 MOS 温度 |
| `arm_a_temp` | 臂A MOS 温度 |
| `arm_b_temp` | 臂B MOS 温度 |
| `leg_a_temp` | 腿A MOS 温度 |
| `leg_b_temp` | 腿B MOS 温度 |
| `waist_temp_max` / `waist_temp_min` | 腰部 MOS 温度极值 |
| `arm_a_temp_max` / `arm_a_temp_min` | 臂A MOS 温度极值 |
| (arm_b / leg_a / leg_b 同上) | |

### 电流(A)

| 字段 | 含义 |
|---|---|
| `arm_a_curr` | 臂A 电流 |
| `arm_b_curr` | 臂B 电流 |
| `leg_a_curr` | 腿A 电流 |
| `leg_b_curr` | 腿B 电流 |
| `waist_curr` | 腰部电流 |
| `head_curr` | 头部电流 |
| `*_curr_max` / `*_curr_min` | 各支路电流极值 |

### 电压(V)

| 字段 | 含义 |
|---|---|
| `arm_a_volt` | 臂A 电压 |
| `arm_b_volt` | 臂B 电压 |
| `leg_a_volt` | 腿A 电压 |
| `leg_b_volt` | 腿B 电压 |
| `waist_volt` | 腰部电压 |
| `bus_volt` | 母线电压 |
| `*_volt_max` / `*_volt_min` | 各支路电压极值 |

### 版本 & 电池

| 字段 | 含义 |
|---|---|
| `software_version` | 软件版本 |
| `hardware_version` | 硬件版本 |
| `battery_voltage` | 电池电压(V) |
| `battery_current` | 电池电流(A) |
| `battery_power` | 电池电量(%) |

## 聚合输出 JSON 结构

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

> 本目录为 `draft` 阶段,`impl/power_board.py` 尚未提供。待驱动代码编写后,在此摘录 `PowerBoardStatePlugin` 本体与关键依赖方法。
> 本目录不含任何口令/密钥。
