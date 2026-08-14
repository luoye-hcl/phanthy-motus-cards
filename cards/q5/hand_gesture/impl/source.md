# 实现来源(source)—— hand_gesture

- **源仓库**:`robotera-q5-driver`(image: `robotera-q5`)
- **文件路径**:`hand_gesture.py`
- **类名**:`Plugin`
- **公共依赖**:`control_contract.py`(q5_is_control_ready/q5_active_status)、`joint_limits.py`(URDF 关节限制)
- **注册位置**:`main.py` 插件聚合(MCP 端口 15794,JSON-RPC 2.0 over HTTP,统一 `/mcp` 端点)
- **运行载体**:驱动容器 `q5-driver-huang`,注册到 Agent Core

> `impl/hand_gesture.py` 为**摘录**(`Plugin` 本体),便于审核理解命令如何下发;不保证脱离真实驱动独立运行。以源仓库为准。
> 本目录不含任何口令/密钥。

## 关键实现

### 命令下发

`dispatch(action, args)` → 校验控制就绪(fresh /xbot_state ∈ READY/ACTIVE + motion_manager active + fresh /joint_states) → 校验参数范围 → 发布到 `/hand_controller/commands`。

### 控制就绪门禁

- `control_contract.q5_is_control_ready(client)`:要求 fresh `/xbot_state` 状态为 READY(3) 或 ACTIVE(4)
- `client.get_lifecycle_state()`:要求 motion_manager 生命周期 `active`
- `client.snapshot()["fresh"]`:要求 fresh `/joint_states`
