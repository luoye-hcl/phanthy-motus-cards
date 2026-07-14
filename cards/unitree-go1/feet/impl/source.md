# 实现来源(source)—— feet

- **源仓库**:`luoye-hcl/go1-driver`
- **文件路径**:`unitree/go1/plugins/mt_state.py`
- **类名**:`FeetCard`(继承 `MtStateCard`)
- **公共依赖**:`plugins/mt_base.py`(`MtStateCard` 基类:`_produce`/`get_tool`/返回包络)、`go1_ctrl.py`(`Go1Control`,唯一硬件入口,factory 后端读真实 HighState)
- **注册位置**:`unitree/go1/main.py` 的 MT 卡片注册(HIGHLEVEL 与 LOWLEVEL 均含 feet)
- **运行载体**:驱动镜像 `go1`,MCP 端口 `15704`(JSON-RPC 2.0),注册到 Agent Core

> `impl/feet.py` 为**摘录**(FeetCard 本体 + 依赖的基类关键方法),便于审核理解返回值如何产生;不保证脱离真实驱动独立运行。以源仓库为准。
> 本目录不含任何口令/密钥。
