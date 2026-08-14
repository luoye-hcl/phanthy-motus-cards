# arm_control —— Q5 手臂控制(控制卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `q5` |
| 卡片名(MCP 工具名) | `arm_control` |
| 类型 | `actuator` |
| 控制等级 | `LOWLEVEL` |
| 作者 | `huangchanglong` |
| 状态 | `draft`(驱动已部署,待实机验收) |

## 能力

将单个身体关节设置到指定安全角度(左右各 7 关节,共 14 个)。目标角度基于捆绑 URDF 关节限制校验后,按部署固定插补时间插值下发。

## 安全前置条件

直接控制接口,仅在机器人未处于保护/急停状态、`/xbot_state` 为 READY/ACTIVE、motion_manager 生命周期 active、且 `/joint_states` 新鲜时有效。动作有时限,到时自动停车/保持。

## 接口

- MCP 工具名:`arm_control`
- 调用:`{"action":"<动作>", ...入参}`
- 返回包络(成功):`{ok:true, card, action, state, command, timestamp_ms}`
- 返回包络(失败):`{ok:false, code, message, details, timestamp_ms}`
- 错误码:`INVALID_ARGUMENT` / `ROS_UNAVAILABLE` / `LIFECYCLE_NOT_ACTIVE` / `Q5_FSM_NOT_READY` / `LIMIT_EXCEEDED` / `MOTION_IN_PROGRESS`

### Actions

| action | 入参 | 说明 |
|---|---|---|
| `start` | 无 | 检查连接状态 |
| `left_shoulder_pitch_joint` | left_shoulder_pitch_rad | 左肩俯仰,范围[-2.79,2.79]rad |
| `left_shoulder_roll_joint` | left_shoulder_roll_rad | 左肩横滚,范围[-0.24,1.83]rad |
| `left_arm_yaw_joint` | left_arm_yaw_rad | 左上臂偏航,范围[-2.62,2.62]rad |
| `left_elbow_pitch_joint` | left_elbow_pitch_rad | 左肘俯仰,范围[-2.27,0.09]rad |
| `left_elbow_yaw_joint` | left_elbow_yaw_rad | 左肘偏航,范围[-2.62,2.62]rad |
| `left_wrist_pitch_joint` | left_wrist_pitch_rad | 左腕俯仰,范围[-1.05,1.05]rad |
| `left_wrist_roll_joint` | left_wrist_roll_rad | 左腕旋转,范围[-1.05,1.05]rad |
| `right_shoulder_pitch_joint` | right_shoulder_pitch_rad | 右肩俯仰,范围[-2.79,2.79]rad |
| `right_shoulder_roll_joint` | right_shoulder_roll_rad | 右肩横滚,范围[-1.83,0.24]rad |
| `right_arm_yaw_joint` | right_arm_yaw_rad | 右上臂偏航,范围[-2.62,2.62]rad |
| `right_elbow_pitch_joint` | right_elbow_pitch_rad | 右肘俯仰,范围[-2.27,0.09]rad |
| `right_elbow_yaw_joint` | right_elbow_yaw_rad | 右肘偏航,范围[-2.62,2.62]rad |
| `right_wrist_pitch_joint` | right_wrist_pitch_rad | 右腕俯仰,范围[-1.05,1.05]rad |
| `right_wrist_roll_joint` | right_wrist_roll_rad | 右腕旋转,范围[-1.05,1.05]rad |
| `cancel` | 无 | 取消微调,保持当前角度 |
| `info` | 无 | 查看状态 |

### 入参

| 参数 | 类型 | 单位 | 说明 |
|---|---|---|---|
| `left_shoulder_pitch_rad` | number | rad | 左肩俯仰目标角度,范围[-2.79,2.79] |
| `left_shoulder_roll_rad` | number | rad | 左肩横滚目标角度,范围[-0.24,1.83] |
| `left_arm_yaw_rad` | number | rad | 左上臂偏航目标角度,范围[-2.62,2.62] |
| `left_elbow_pitch_rad` | number | rad | 左肘俯仰目标角度,范围[-2.27,0.09] |
| `left_elbow_yaw_rad` | number | rad | 左肘偏航目标角度,范围[-2.62,2.62] |
| `left_wrist_pitch_rad` | number | rad | 左腕俯仰目标角度,范围[-1.05,1.05] |
| `left_wrist_roll_rad` | number | rad | 左腕旋转目标角度,范围[-1.05,1.05] |
| `right_shoulder_pitch_rad` | number | rad | 右肩俯仰目标角度,范围[-2.79,2.79] |
| `right_shoulder_roll_rad` | number | rad | 右肩横滚目标角度,范围[-1.83,0.24] |
| `right_arm_yaw_rad` | number | rad | 右上臂偏航目标角度,范围[-2.62,2.62] |
| `right_elbow_pitch_rad` | number | rad | 右肘俯仰目标角度,范围[-2.27,0.09] |
| `right_elbow_yaw_rad` | number | rad | 右肘偏航目标角度,范围[-2.62,2.62] |
| `right_wrist_pitch_rad` | number | rad | 右腕俯仰目标角度,范围[-1.05,1.05] |
| `right_wrist_roll_rad` | number | rad | 右腕旋转目标角度,范围[-1.05,1.05] |


### ROS2 话题

| topic | 消息类型 |
|---|---|
| `/wr1_controller/commands` | `xbot_common_interfaces/msg/HybridJointCommand` |

### 返回示例

```json
{"ok":true,"card":"arm_control","action":"left_elbow_pitch_joint","state":"moving","command":{"joint":"left_elbow_pitch_joint","target_rad":-0.5}}
```

## 数据来源 / 实现位置

- 源仓库:`robotera-q5-driver`(image: `robotera-q5`)
- 文件:`arm_control.py`  类:`Plugin`
- 依赖:`control_contract.py`(控制就绪校验 q5_is_control_ready)、`joint_limits.py`(URDF 关节限制)
- 注册:`main.py` 插件聚合;MCP 端口 15794,注册到 Agent Core

## 状态说明

- 驱动:`q5-driver-huang`(容器)已在 Jetson 192.168.8.40 运行,已注册到 Agent Core。
- 实机:待逐卡验收后升 `offline-green`。
