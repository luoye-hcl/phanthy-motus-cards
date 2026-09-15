# 实现来源(source)—— net

- **源仓库**:`luoye-hcl/go1-driver`
- **文件路径**:`unitree/go1/plugins/mt_state.py`
- **类名**:`NetCard`(继承 `MtStateCard`,覆写 `_produce` 跳过硬件新鲜度抑制)
- **公共依赖**:`plugins/mt_base.py`(`MtStateCard` 基类);实现仅用标准库 `socket` + 读 `/proc/net/wireless`,不碰硬件、不依赖 `go1_ctrl` 的 HighState
- **注册位置**:`unitree/go1/main.py` 的 MT 卡片注册(ANY 级,高低层均含 net)
- **运行载体**:驱动镜像 `go1`,MCP 端口 `15704`,注册到 Agent Core

> `impl/net.py` 为摘录。以源仓库为准,不保证独立运行。本目录不含任何口令/密钥(IPv4/主机名为运行时读取,非硬编码)。
