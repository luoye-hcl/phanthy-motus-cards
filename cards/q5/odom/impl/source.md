# 实现来源(source)—— odom

- **源仓库**:`robotera-q5-driver`(image: `robotera-q5`)
- **文件路径**:`odom.py`(**待实现**)
- **类名**:`Plugin`
- **公共依赖**:`q5_sdk_client.py`(需扩展订阅 `/wr1_base_drive_controller/odom`)、`sensor_contract.py`
- **注册位置**:`main.py` 插件聚合(MCP 端口 15794)

> `impl/odom.py` 为**参考实现骨架**(照 battery.py 模式),非真实驱动源码。
> 数据源 `/wr1_base_drive_controller/odom` 已在真机验证,但驱动尚未订阅该 topic,待开发后以源仓库为准。
> 本目录不含任何口令/密钥。

## 关键实现

### 订阅话题

| topic | 消息类型 |
|---|---|
| `/wr1_base_drive_controller/odom` | `nav_msgs/msg/Odometry` |

### 数据流(规划)

驱动(Domain 211 CycloneDDS)订阅 `/wr1_base_drive_controller/odom` → `build(snapshot)` 生成 JSON → 发布到 Agent Core 桥接 topic `/{ns}/q5/odom`(Domain 42 FastDDS)。
