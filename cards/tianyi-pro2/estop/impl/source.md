# 实现来源(source)—— estop

- **源仓库**:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 `unitree/tiangong_pro/` 代码)
- **文件路径**:`plugins/estop.py`(待实现)
- **类名**:`EstopStatePlugin`(待实现)
- **公共依赖**:`ros_bridge.py`(ROS2 订阅桥)、`bodyctrl_msgs/msg/PowerBoardKeyStatus`
- **注册位置**:`main.py` 插件聚合(待实现);驱动镜像/端口:待定
- **MCP 协议**:JSON-RPC 2.0 over HTTP,注册到 Agent Core

## 数据源 topic(来自天轶2.0 SDK 文档)

| ROS2 topic | 频率 | 说明 |
|---|---|---|
| `/power/board/key_status` | 1 Hz | 急停/软急停/电源按键状态 + 工作时间 |

## PowerBoardKeyStatus.msg 字段

| 字段 | 类型 | 含义 |
|---|---|---|
| `header.stamp` | time | 采样时间戳 |
| `work_time` | uint32 | 累计工作时间(s) |
| `is_estop` | bool | 急停按键是否被按下 |
| `is_remote_estop` | bool | 软急停是否被按下 |
| `is_power_on` | bool | 电源是否正常供电 |

## 聚合输出 JSON 结构

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

> 本目录为 `draft` 阶段,`impl/estop.py` 尚未提供。待驱动代码编写后,在此摘录 `EstopStatePlugin` 本体与关键依赖方法。
> 本目录不含任何口令/密钥。
