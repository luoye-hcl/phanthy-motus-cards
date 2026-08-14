# simple_action —— Q5 预定义动作(控制卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `simple_action` |
| 类型 | `actuator` |
| 控制等级 | `LOWLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已实现但禁用,需现场解锁) |

## 能力

调用 Q5 厂商 action 服务 `/simple_actions`(`xbot_common_interfaces/action/SimpleActions`),执行白名单预定义动作。当前白名单:

- `zero` — 零位复位
- `initpose_handsdown` — 垂手初始姿势
- `lift_up` — 抬臂动作

## 安全前置条件

本卡**不会**执行 dynamic_launch/ready/activate 序列——需现场操作员完成并验证该序列后,才能显式解锁本卡。仅当 `/xbot_state` 为 READY/ACTIVE、motion_manager 生命周期 active、`/joint_states` 新鲜、且 action server ready 时才下发。

## 接口

- MCP 工具名:`simple_action`
- 调用:`{"action":"run", "action_name":"<白名单动作>"}`
- 返回包络(成功):`{ok:true, state, action_name, time_cost_s, cancellable}`
- 错误码:`ACTION_NOT_ALLOWED` / `ROS_UNAVAILABLE` / `LIFECYCLE_NOT_ACTIVE` / `Q5_FSM_NOT_READY` / `ACTION_SERVER_UNAVAILABLE` / `ACTION_IN_PROGRESS`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `start` | 无 | 检查动作服务和机器人状态 |
| `run` | action_name | 执行一个白名单预设动作 |
| `cancel` | 无 | 请求取消正在执行的动作 |
| `info` | 无 | 查看动作执行状态和安全条件 |

### 入参

| 参数 | 类型 | 说明 |
|---|---|---|
| `action_name` | string | zero / initpose_handsdown / lift_up |

### ROS2 Action

| action | 类型 |
|---|---|
| `/simple_actions` | `xbot_common_interfaces/action/SimpleActions` |

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`simple_action.py`  类:`Plugin`(已实现,config.yaml 中 disabled)
- 依赖:`control_contract.py`、`xbot_common_interfaces.action.SimpleActions`
- 注册:`main.py` 插件聚合;MCP 端口 15794

## 状态说明

- 驱动:`simple_action.py` 已实现,但 config.yaml 中 `enabled: false`(vendor action service,非直接关节控制路径)。
- 实机:`/simple_actions` action server 存在(ros2 action list 确认),待现场解锁后验收。
