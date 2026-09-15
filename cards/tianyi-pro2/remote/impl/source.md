# 实现来源(source)—— remote

- **源仓库**:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 `unitree/tiangong_pro/` 代码)
- **文件路径**:`plugins/remote.py`(待实现)
- **类名**:`RemoteStatePlugin`(待实现)
- **公共依赖**:`ros_bridge.py`(ROS2 订阅桥)、`bodyctrl_msgs/msg/SbusData`
- **注册位置**:`main.py` 插件聚合(待实现);驱动镜像/端口:待定
- **MCP 协议**:JSON-RPC 2.0 over HTTP,注册到 Agent Core

## 数据源 topic(来自天轶2.0 SDK 文档)

| ROS2 topic | 频率 | 说明 |
|---|---|---|
| `/sbus_data/event` | 文档未注明(需量测) | 遥控器SBUS按键事件 + 摇杆数据 |

## SbusData.msg 字段

### 按键事件常量

```
KEY_NONE=0
KEY_A_UP=1   KEY_A_DOWN=2
KEY_B_UP=3   KEY_B_DOWN=4
KEY_C_UP=5   KEY_C_DOWN=6
KEY_D_UP=7   KEY_D_DOWN=8
KEY_E_UP=9   KEY_E_MID=10  KEY_E_DOWN=11
KEY_F_UP=12  KEY_F_MID=13  KEY_F_DOWN=14
KEY_G_LEFT=15 KEY_G_MID=16 KEY_G_RIGHT=17
KEY_H_LEFT=18 KEY_H_MID=19 KEY_H_RIGHT=20
```

### 字段

| 字段 | 类型 | 含义 |
|---|---|---|
| `header.stamp` | time | 采样时间戳 |
| `key_event_new` | int32 | 按键事件新值 |
| `key_event_old` | int32 | 按键事件旧值 |
| `button_a`–`button_d` | int8 | A–D 键值(-1 松开 / 1 按下) |
| `button_e` | int8 | E 键值(<-0.5 上拨 / -0.5~0.5 中 / >0.5 下拨) |
| `button_f` | int8 | F 键值(同 E) |
| `button_g` | int8 | G 键值(<-0.5 左拨 / -0.5~0.5 中 / >0.5 右拨) |
| `button_h` | int8 | H 键值(<-0.5 右拨 / -0.5~0.5 中 / >0.5 左拨) |
| `x1` | float32 | 左摇杆 X(左右,-1.0~1.0) |
| `y1` | float32 | 左摇杆 Y(上下,-1.0~1.0) |
| `x2` | float32 | 右摇杆 X(左右,-1.0~1.0) |
| `y2` | float32 | 右摇杆 Y(上下,-1.0~1.0) |

## 聚合输出 JSON 结构

```json
{
  "key_event": { "new": 0, "old": 0 },
  "buttons": { "a": -1, "b": -1, "c": -1, "d": -1, "e": 0, "f": 0, "g": 0, "h": 0 },
  "sticks": { "x1": 0.0, "y1": 0.0, "x2": 0.0, "y2": 0.0 },
  "timestamp_ms": 1784025258226,
  "control_level": "ANY"
}
```

> 本目录为 `draft` 阶段,`impl/remote.py` 尚未提供。待驱动代码编写后,在此摘录 `RemoteStatePlugin` 本体与关键依赖方法。
> 本目录不含任何口令/密钥。
