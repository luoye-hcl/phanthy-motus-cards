# estop —— 天轶2.0 Pro 急停/按键状态(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `tianyi-pro2` |
| 卡片名(MCP 工具名) | `estop` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(未实机验收) |

## 能力

读取天轶2.0 Pro 电源板按键/急停状态,1 Hz 低频。包括急停按键(`is_estop`)、软急停(`is_remote_estop`)、电源供电状态(`is_power_on`)以及累计工作时间。用于安全监控、急停状态检测、供电异常告警,供大模型或人判断机器人是否处于安全可运行状态。

## 接口

- 输出 topic:
  - `/power/board/key_status`  格式:`bodyctrl_msgs/msg/PowerBoardKeyStatus`
- 采样频率:`19.2` Hz(**实测,文档预估 1Hz,重大修正**)(2026-07-28 实测)
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`)

### 实测数据样本(2026-07-28,x86 192.168.41.1)

| 字段 | 实测值 | 说明 |
|---|---|---|
| `is_estop` | false | 急停未按下 |
| `is_power_on` | true | 电源正常供电 |

> 频率修正:文档预估 1Hz,实测 19.2Hz。这是安全关键 topic,实际频率远高于文档描述。

### 字段(PowerBoardKeyStatus)

| 字段 | 含义 | 单位 |
|---|---|---|
| `header.stamp` | 采样时间戳 | ns |
| `work_time` | 累计工作时间 | s |
| `is_estop` | 急停按键是否被按下 | bool |
| `is_remote_estop` | 软急停是否被按下 | bool |
| `is_power_on` | 电源是否正常供电 | bool |

### 聚合后 JSON 输出结构

```json
{
  "work_time": 3600,
  "is_estop": false,
  "is_remote_estop": false,
  "is_power_on": true,
  "timestamp_ms": 1784025258226,
  "control_level": "ANY"
}
```

## 数据来源 / 实现位置

- 源仓库:`<待建 tianyi-pro2-driver>`
- 文件:`plugins/estop.py`  类:`EstopStatePlugin`(待实现)
- 依赖:`ros_bridge.py`、`bodyctrl_msgs/msg/PowerBoardKeyStatus`
- 注册:`main.py` 插件聚合;驱动镜像/端口:待定

## 状态说明

- 离线:未实现(驱动代码待写)。
- 实机:未验收。待真机 `ros2 topic echo /power/board/key_status` 确认字段后升 `offline-green`。
