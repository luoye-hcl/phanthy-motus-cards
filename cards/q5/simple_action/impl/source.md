# 实现来源(source)—— simple_action

- **源仓库**:`robotera-q5-driver`(image: `robotera-q5`)
- **文件路径**:`simple_action.py`
- **类名**:`Plugin`
- **公共依赖**:`control_contract.py`(q5_is_control_ready)、`xbot_common_interfaces.action.SimpleActions`
- **注册位置**:`main.py` 插件聚合(MCP 端口 15794)

> `impl/simple_action.py` 为**摘录**(真实驱动源码),便于审核理解动作如何下发。以源仓库为准。
> 本目录不含任何口令/密钥。

## 关键实现

### Action 客户端

`ActionClient(SimpleActions, "/simple_actions")` → `send_goal_async(goal)`,goal 含 `action_name` + `time_cost`。

### 白名单

`DEFAULT_ACTIONS = {"zero": 4.0, "initpose_handsdown": 4.0, "lift_up": 4.0}`(时长由厂商定义)。

### 控制就绪门禁

- `q5_is_control_ready`:fresh /xbot_state ∈ READY/ACTIVE
- `get_lifecycle_state()`:motion_manager active
- `snapshot()["fresh"]`:fresh /joint_states
- `action_client.server_is_ready()`:action server ready
