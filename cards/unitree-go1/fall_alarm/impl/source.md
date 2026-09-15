# 实现来源(source)—— fall_alarm

- **源仓库**:`luoye-hcl/go1-driver`
- **文件路径**:`unitree/go1/plugins/mt_state.py`
- **类名**:`FallAlarmCard`(继承 `MtStateCard`)
- **公共依赖**:`plugins/mt_base.py`(`MtStateCard` 基类)、`go1_ctrl.py`(`Go1Control`,factory 后端读真实 HighState.imu 的 `rpy_rad`)
- **注册位置**:`unitree/go1/main.py` 的 MT 卡片注册(ANY 级,高低层均含 fall_alarm)
- **运行载体**:驱动镜像 `go1`,MCP 端口 `15704`,注册到 Agent Core

> `impl/fall_alarm.py` 为摘录。以源仓库为准,不保证独立运行。本目录不含任何口令/密钥。
