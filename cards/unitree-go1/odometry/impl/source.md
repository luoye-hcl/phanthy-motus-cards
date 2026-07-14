# 实现来源(source)—— odometry

- **源仓库**:`luoye-hcl/go1-driver`
- **文件路径**:`unitree/go1/plugins/mt_state.py`
- **类名**:`OdometryCard`(继承 `MtStateCard`,覆写 `dispatch` 增 `reset_origin`)
- **公共依赖**:`plugins/mt_base.py`(`MtStateCard` 基类)、`go1_ctrl.py`(`Go1Control.get_odometry()`,factory 后端由真实 HighState 累计 position/yaw/里程)
- **注册位置**:`unitree/go1/main.py` 的 MT 卡片注册(仅 HIGHLEVEL 出;低层态无 position 不注册)
- **运行载体**:驱动镜像 `go1`,MCP 端口 `15704`,注册到 Agent Core

> `impl/odometry.py` 为摘录。以源仓库为准,不保证独立运行。本目录不含任何口令/密钥。
