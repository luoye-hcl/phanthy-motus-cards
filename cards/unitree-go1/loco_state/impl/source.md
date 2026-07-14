# 实现来源(source)—— loco_state

- **源仓库**:`luoye-hcl/go1-driver`
- **文件路径**:`unitree/go1/plugins/mt_state.py`
- **类名**:`LocoStateCard`(继承 `MtStateCard`)
- **公共依赖**:`plugins/mt_base.py`、`go1_ctrl.py`(`get_high_state()`,factory 后端读真实 HighState;`MODE_NAMES`/`GAIT_NAMES` 映射码→名)
- **注册位置**:`unitree/go1/main.py` 的 MT 卡片注册(仅 HIGHLEVEL)
- **运行载体**:驱动镜像 `go1`,MCP 端口 `15704`,注册到 Agent Core

> `impl/loco_state.py` 为摘录。以源仓库为准,不保证独立运行。本目录不含任何口令/密钥。
