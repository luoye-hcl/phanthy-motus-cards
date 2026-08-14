# 实现来源(source)—— cpu_freq

- **源仓库**:`robotera-q5-driver`(image: `robotera-q5`)
- **文件路径**:`cpu_freq.py`
- **类名**:`Plugin`
- **公共依赖**:`sensor_contract.py`
- **注册位置**:`main.py` 插件聚合(MCP 端口 15794)

> 数据流:驱动(Domain 211)订阅 `/cpu_freq` → build() 生成 JSON → 桥接到 `/{ns}/q5/cpu_freq`(Domain 42)。
