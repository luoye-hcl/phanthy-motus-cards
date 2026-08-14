# 实现来源(source)—— battery

- **源仓库**:`robotera-q5-driver`(image: `robotera-q5`)
- **文件路径**:`battery.py`
- **类名**:`Plugin`
- **公共依赖**:`q5_sdk_client.py`(只读 ROS2 客户端,快照 `snapshot()`)、`sensor_contract.py`(topic_out 声明)
- **注册位置**:`main.py` 插件聚合(MCP 端口 15794,JSON-RPC 2.0 over HTTP,统一 `/mcp` 端点)
- **运行载体**:驱动容器 `q5-driver-huang`,注册到 Agent Core

> `impl/battery.py` 为**摘录**(`Plugin` 本体),便于审核理解返回值如何产生;不保证脱离真实驱动独立运行。以源仓库为准。
> 本目录不含任何口令/密钥。

## 关键实现

### 订阅话题

| topic | 消息类型 |
|---|---|
| `/battery_state` | `sensor_msgs/msg/BatteryState` |

### 数据流

驱动(Domain 211 CycloneDDS)订阅 `/battery_state` → `build(snapshot)` 生成 JSON → 发布到 Agent Core 桥接 topic `/{ns}/q5/battery`(Domain 42 FastDDS)。

### 新鲜度

- 消息带 `fresh`/`available`/`age_ms`/`stale` 标记
- 无新包不伪造数据(`fresh=false`)
