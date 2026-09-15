# remote —— 天轶2.0 Pro 遥控器状态(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `tianyi-pro2` |
| 卡片名(MCP 工具名) | `remote` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(未实机验收) |

## 能力

读取天轶2.0 Pro 遥控器(SBUS)事件与摇杆数据。包括 8 个按键(A/B/C/D 按钮 + E/F/G/H 拨片)的事件新旧值、实时键值,以及双摇杆四轴(x1/y1/x2/y2,范围 -1.0~1.0)。用于遥控器输入监控、按键事件检测、摇杆方向读取,供大模型或人了解操作员的实时控制意图。

## 接口

- 输出 topic(两个 topic 同时以 43.3 Hz 发布):
  - `/{ns}/sbus_data`  格式:`sensor_msgs/msg/Joy`(12 轴 axes + buttons 数组)
  - `/{ns}/sbus_data/event`  格式:`bodyctrl_msgs/msg/SbusData`(按键事件 + 摇杆,聚合用此 topic)
- 采样频率:43.3 Hz(实机 `ros2 topic hz` 量测,两个 topic 同频)
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`)
- 聚合后单流输出:`/{ns}/state/remote`  格式:`data/json`

### 按键事件常量(SbusData)

| 常量 | 值 | 说明 |
|---|---|---|
| `KEY_NONE` | 0 | 无事件 |
| `KEY_A_UP` / `KEY_A_DOWN` | 1 / 2 | A键抬起 / 按下 |
| `KEY_B_UP` / `KEY_B_DOWN` | 3 / 4 | B键抬起 / 按下 |
| `KEY_C_UP` / `KEY_C_DOWN` | 5 / 6 | C键抬起 / 按下 |
| `KEY_D_UP` / `KEY_D_DOWN` | 7 / 8 | D键抬起 / 按下 |
| `KEY_E_UP` / `KEY_E_MID` / `KEY_E_DOWN` | 9 / 10 / 11 | E键上拨 / 回中 / 下拨 |
| `KEY_F_UP` / `KEY_F_MID` / `KEY_F_DOWN` | 12 / 13 / 14 | F键上拨 / 回中 / 下拨 |
| `KEY_G_LEFT` / `KEY_G_MID` / `KEY_G_RIGHT` | 15 / 16 / 17 | G键左拨 / 回中 / 右拨 |
| `KEY_H_LEFT` / `KEY_H_MID` / `KEY_H_RIGHT` | 18 / 19 / 20 | H键左拨 / 回中 / 右拨 |

### 字段(SbusData,`/sbus_data/event`)

| 字段 | 含义 | 范围 |
|---|---|---|
| `header.stamp` | 采样时间戳 | ns |
| `key_event_new` | 按键事件新值 | 0–20 |
| `key_event_old` | 按键事件旧值 | 0–20 |
| `button_a`–`button_d` | A–D键值 | -1 松开 / 1 按下 |
| `button_e` | E键值 | <-0.5 上拨 / -0.5~0.5 中 / >0.5 下拨 |
| `button_f` | F键值 | <-0.5 上拨 / -0.5~0.5 中 / >0.5 下拨 |
| `button_g` | G键值 | <-0.5 左拨 / -0.5~0.5 中 / >0.5 右拨 |
| `button_h` | H键值 | <-0.5 右拨 / -0.5~0.5 中 / >0.5 左拨 |
| `x1` | 左摇杆X方向(左右) | -1.0~1.0 |
| `y1` | 左摇杆Y方向(上下) | -1.0~1.0 |
| `x2` | 右摇杆X方向(左右) | -1.0~1.0 |
| `y2` | 右摇杆Y方向(上下) | -1.0~1.0 |

### 字段(Joy,`/sbus_data`)

| 字段 | 含义 | 备注 |
|---|---|---|
| `header.stamp` | 采样时间戳 | ns |
| `axes` | 12 轴浮点数组 | 索引 0-11,范围 -1.0~1.0;实机空闲态多轴为 -0.0,索引 6 为 1.0,索引 8-11 恒为 -1.0 |
| `buttons` | 按键整型数组 | 实机观察为空数组 `[]`,按键事件通过 `/sbus_data/event` 的 `button_a`–`button_h` 上报 |

### 聚合后 JSON 输出结构

```json
{
  "key_event": { "new": 0, "old": 0 },
  "buttons": { "a": -1, "b": -1, "c": -1, "d": -1, "e": 0, "f": 0, "g": 0, "h": 0 },
  "sticks": { "x1": 0.0, "y1": 0.0, "x2": 0.0, "y2": 0.0 },
  "timestamp_ms": 1784025258226,
  "control_level": "ANY"
}
```

## 数据来源 / 实现位置

- 源仓库:`<待建 tianyi-pro2-driver>`
- 文件:`plugins/remote.py`  类:`RemoteStatePlugin`(待实现)
- 依赖:`ros_bridge.py`、`bodyctrl_msgs/msg/SbusData`
- 注册:`main.py` 插件聚合;驱动镜像/端口:待定

## 状态说明

- 离线:未实现(驱动代码待写)。
- 实机:部分验收(2026-07-28)。已通过 `ros2 topic echo/hz` 确认两个 topic 同频 43.3 Hz、字段与值域符合预期,空闲态样本已采集;按键态/摇杆推到位态样本待补。待驱动实现后升 `offline-green`。

## 实机真实数据样本(2026-07-28 采集)

### `/sbus_data`(Joy,43.3 Hz,空闲态)

```yaml
header:
  stamp: {sec: 1785235602, nanosec: 364298612}
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

### `/sbus_data/event`(SbusData,43.3 Hz,空闲态,H 键被按下)

```yaml
header:
  stamp: {sec: 1785235603, nanosec: 357007496}
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

> 备注:本样本中 `button_h=1` 表示 H 键处于按下/拨动位;摇杆四轴全为 -0.0(居中)。按键事件 `key_event_new/old` 均为 0(无新事件触发)。
