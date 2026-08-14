# 实现来源(source)—— remote_command

- **源仓库**:`robotera-q5-driver`(image: `robotera-q5`)
- **文件路径**:`remote_command.py`(**已实现**)
- **类名**:`Plugin`
- **公共依赖**:`sensor_contract.py`、`sensor_msgs/msg/Joy`
- **注册位置**:`main.py` 插件聚合(MCP 端口 15794)

> `impl/remote_command.py` 为**真实驱动源码**(照 cpu_freq.py 模式:自建 ROS2 Node)。
> 本目录不含任何口令/密钥。

## 关键实现

### 订阅话题

| topic | 消息类型 |
|---|---|
| `/send_remote/command` | `sensor_msgs/msg/Joy` |

### 数据流

驱动(Domain 211 CycloneDDS)自建 Node 订阅 `/send_remote/command` → `build(msg)` 解析 axes + buttons → 发布到 Agent Core 桥接 topic `/{ns}/q5/remote_command`(Domain 42 FastDDS)。
