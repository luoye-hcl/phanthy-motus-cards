# 实现来源(source)—— teleop_state

- **源仓库**:`robotera-q5-driver`(image: `robotera-q5`)
- **文件路径**:`teleop_state.py`
- **类名**:`Plugin`
- **公共依赖**:`sensor_contract.py`
- **注册位置**:`main.py` 插件聚合(MCP 端口 15794)

> 数据流:驱动(Domain 211)订阅 `/teleop_state` → build() 生成 JSON → 桥接到 `/{ns}/q5/teleop_state`(Domain 42)。
