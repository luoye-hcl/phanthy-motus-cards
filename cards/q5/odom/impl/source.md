# 实现来源(source)—— odom

- **源仓库**:`robotera-q5-driver`(image: `robotera-q5`)
- **文件路径**:`odom.py`(**已实现**)
- **类名**:`Plugin`
- **公共依赖**:`sensor_contract.py`、`nav_msgs/msg/Odometry`
- **注册位置**:`main.py` 插件聚合(MCP 端口 15794)

> `impl/odom.py` 为**真实驱动源码**(照 cpu_freq.py 模式:自建 ROS2 Node)。
> 本目录不含任何口令/密钥。

## 关键实现

### 订阅话题

| topic | 消息类型 |
|---|---|
| `/wr1_base_drive_controller/odom` | `nav_msgs/msg/Odometry` |

### 数据流

驱动(Domain 211 CycloneDDS)自建 Node 订阅 `/wr1_base_drive_controller/odom` → `build(msg)` 解析 position/orientation/linear/angular → 发布到 Agent Core 桥接 topic `/{ns}/q5/odom`(Domain 42 FastDDS)。
