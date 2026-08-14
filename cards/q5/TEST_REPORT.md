# Q5 画布卡片测试文档

> 机器人: RobotEra Q5 (46 DOF, 差速底盘)  
> 驱动容器: `q5-driver-huang` (端口 15794)  
> MCP 服务 ID: `mcp-1786351358`  
> 框架仓库: https://github.com/yu821138652/phanthymotus-driver/tree/main/robotera/q5_bundle  
> 日期: 2026-08-14  

---

## 一、Sensor 卡片 (15 张)

### 1. joints (骨架可视化)

**用途**: 驱动 3D URDF 骨架渲染，展示机器人当前姿势。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据是否在 5s 内更新 | `true` | `false` 时骨架不更新，检查 ROS 连接 |
| `available` | bool | 是否收到过消息 | `true` | `false` 说明 /joint_states 无发布者 |
| `joint_count` | int | 关节总数 | `34` | 校验数据完整性 |
| `position_unit` | string | 位置单位 | `"rad"` | 弧度制，换算角度需 ×57.3 |
| `joints` | array | 关节列表，每项含 `name` 和 `q` | `[{"name":"left_drv_wheel_joint","q":0.0}]` | 逐关节读取角度送入 URDF 渲染器 |
| `source_topic` | string | 数据来源 | `"/joint_states"` | 排查时用于 ROS topic echo |

**调用方式**: `action=info`

**示例数据**:
```json
{
  "timestamp_ms": 1786691652000,
  "fresh": true,
  "available": true,
  "joint_count": 34,
  "position_unit": "rad",
  "joints": [
    {"name": "left_drv_wheel_joint", "q": 0.0},
    {"name": "right_shoulder_pitch_joint", "q": -0.000019},
    {"name": "left_elbow_pitch_joint", "q": -1.570}
  ]
}
```

---

### 2. joints_state (完整关节状态)

**用途**: 分组查看身体/左手/右手的 position、velocity、effort。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `true` | `false` 时数据不可信 |
| `joint_count` | int | 关节总数 | `34` | body:22 + left_hand:6 + right_hand:6 |
| `groups.body` | object | 身体 22 关节 | 见下 | 每关节含 position/velocity/effort |
| `groups.left_hand` | object | 左手 6 关节 | 见下 | 手指弯曲状态 |
| `groups.right_hand` | object | 右手 6 关节 | 见下 | 手指弯曲状态 |

**groups 内部结构**:
```json
{
  "joint_count": 22,
  "joints": [
    {
      "name": "left_drv_wheel_joint",
      "position": 0.0,      // 弧度
      "velocity": 0.0,      // rad/s
      "effort": 0.0         // 力矩
    }
  ]
}
```

**怎么用**:
- `position` 判断关节当前角度（静止时大部分≈0，肘关节约 -1.57 rad ≈ -90°）
- `velocity` 全为 0 表示机器人静止
- `effort` 非零表示关节有力负载（如 ankle=-24 表示脚踝承重）

---

### 3. robot_ready (就绪状态)

**用途**: 判断机器人是否可接受控制指令。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `robot_state` | string | 机器人状态标签 | `"ACTIVE"` | INIT/SELF_TEST/IDLE/READY/ACTIVE/SHUTDOWN/OTA/E_STOP/ERROR |
| `ready` | bool | 是否可控制 | `true` | 只有 READY 或 ACTIVE 时为 true，控制前必须确认 |
| `motion_ready` | bool | 运动管理器是否就绪 | `true` | false 时运动指令会被拒绝 |
| `motion_manager_active` | bool | 运动管理器生命周期 | `true` | false 说明 motion_manager 未启动 |
| `message_fresh` | bool | /xbot_state 消息是否新鲜 | `true` | false 时状态可能已过时 |
| `message` | string | 人类可读摘要 | `"状态: ACTIVE \| 运动管理器: ACTIVE"` | 快速理解当前状态 |

**怎么用**: 控制动作前必须检查 `ready=true` 且 `motion_ready=true`。`robot_state=ERROR` 或 `E_STOP` 时禁止一切控制。

---

### 4. battery (电池)

**用途**: 监控电池电量和健康状态。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `true` | false 时电量数据可能过时 |
| `percentage` | float | 电量百分比 | `81.0` | <15% 为 critical，应停止运动 |
| `level` | string | 电量等级 | `"normal"` | full/normal/low/critical/unknown |
| `voltage_v` | float | 电压 (V) | `64.49` | 正常范围约 55-67V，过低需充电 |
| `temperature_c` | float | 温度 (°C) | `29.0` | >50°C 需关注散热 |
| `message` | string | 状态摘要 | `null` 或 `"电量已满"` | 快速理解 |

**怎么用**: `level=critical` (<15%) 时应立即返回充电。`temperature_c > 50` 时减少运动强度。

---

### 5. system_health (运行健康)

**用途**: 综合监控运动状态、温度和故障。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 必需来源是否新鲜 | `true` | false 时健康状态不可信 |
| `robot_state` | string | 机器人状态 | `"READY"` | 同 robot_ready 的 robot_state |
| `robot_active` | bool | 机器人是否在运动 | `false` | true 时表示有活跃任务 |
| `robot_message` | string | 厂商状态消息 | `"Current state: READY"` | 透传厂商原文 |
| `temperature` | object | 温度摘要 | `{"max_celsius":57.0,"max_sensor":"neck_pitch_joint/driver_temperature","min_celsius":34.0,"min_sensor":"right_arm_yaw_joint/motor_temperature"}` | max>60°C 需关注 |
| `motion` | object\|null | 运动状态事件 | `null` | 事件驱动，无事件时为 null |
| `faults` | object\|null | 聚合故障列表 | 见下 | 检查 is_active=true 且 level<5 的项 |
| `message` | string | 健康摘要 | `"健康遥测正常"` | 快速理解 |

**faults 结构**:
```json
{
  "faults": [
    {
      "fault_code": 0,
      "level": 5,           // 5=OK, 4=WARN, 3=ERROR, 2=FATAL
      "name": "",
      "message": "Resource usage normal",
      "is_active": true,
      "hardware_id": "system_monitor"
    }
  ]
}
```

**怎么用**: `level <= 3` 且 `is_active=true` 的故障需立即处理。`temperature.max_celsius > 60` 需降温。

---

### 6. hand_state (手部关节状态)

**用途**: 监控左右手 6 个手指关节的位置、速度、力矩。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `true` | false 时手部数据不可信 |
| `hand_model` | string | 手部型号 | `"XHand Lite"` | 12 关节 (左6+右6) |
| `left` | object | 左手 6 关节 | 见下 | 拇指弯曲/旋转 + 食指/中指/无名指/小指弯曲 |
| `right` | object | 右手 6 关节 | 见下 | 同左手 |
| `hands_complete` | bool | 双手数据是否完整 | `true` | false 时缺失部分手臂数据 |

**left/right 结构**:
```json
{
  "joint_names": ["left_hand_thumb_bend_joint", "left_hand_thumb_rota_joint1", ...],
  "joint_count": 6,
  "positions": {"left_hand_thumb_bend_joint": 0.947, ...},
  "velocities": {"left_hand_thumb_bend_joint": 0.0, ...},
  "efforts": {"left_hand_thumb_bend_joint": -270.0, ...}
}
```

**怎么用**: `positions` 0=张开, 1=完全弯曲。`efforts` 负值大表示手指在用力抓握。

---

### 7. nav_state (导航状态)

**用途**: 查看导航栈状态（只读，不执行导航）。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `false` | false 时导航无数据 |
| `available` | bool | 是否收到过导航状态 | `false` | false 说明导航栈未运行 |
| `status` | string\|null | 导航状态文本 | `null` | 厂商透传的导航状态 |
| `publisher_connected` | bool | 发布者是否在线 | `false` | false 说明导航服务未启动 |
| `source_state` | string | 来源状态 | `"navigation_stack_not_running"` | 判断导航栈是否在运行 |
| `message` | string | 状态描述 | `"导航状态发布器未运行"` | 快速理解 |

**怎么用**: `publisher_connected=false` 时导航功能不可用。`source_state=navigation_stack_not_running` 表示需要启动导航栈。

---

### 8. estop (急停状态)

**用途**: 监控急停按钮和 FSM 急停状态。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `true` | false 时急停状态不可信 |
| `emergency_stop` | bool | 急停是否激活 | `false` | true 时所有控制卡拒绝执行 |
| `fsm_estop_detected` | bool | FSM 是否检测到急停 | `false` | 与 emergency_stop 取或，任一为 true 都危险 |
| `fsm_estop_reported` | bool | FSM 是否上报急停 | `false` | 历史急停标记 |
| `fsm_state` | int | FSM 状态码 | `-1` | -1=ERROR, 7=E_STOP |
| `fsm_message` | string | FSM 状态消息 | `"Current state: ERROR"` | 厂商状态文本 |
| `message` | string | 状态描述 | `null` | 有异常时才有值 |

**怎么用**: `emergency_stop=true` 或 `fsm_estop_detected=true` 时禁止一切运动。`fsm_state=-1` (ERROR) 也需排查。

---

### 9. diagnostics (诊断)

**用途**: 查看硬件/软件诊断聚合信息。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `false` | false 时无最新诊断 |
| `available` | bool | 是否有诊断数据 | `false` | false 说明诊断聚合器未发消息 |
| `data` | object\|null | 诊断数据 | `null` | 含 level/name/hw_id/key_values |
| `publisher_connected` | bool | 发布者是否在线 | `true` | true 但 available=false 表示等待事件 |
| `source_state` | string | 来源状态 | `"awaiting_diagnostic_event"` | 事件驱动，可能等待中 |
| `message` | string | 状态描述 | `"诊断发布器已连接，尚无诊断消息"` | 快速理解 |

**怎么用**: `data` 非空时检查 `level >= 2 (ERROR)` 的项。`publisher_connected=true` 但 `data=null` 是正常的（事件驱动）。

---

### 10. odom (里程计)

**用途**: 获取底盘位置、姿态和速度。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `true` | false 时定位不可信 |
| `frame_id` | string | 坐标系 | `"odom"` | 里程计坐标系 |
| `child_frame_id` | string | 子坐标系 | `"base_link"` | 机器人本体坐标系 |
| `position` | object | 位置 {x,y,z} (m) | `{"x":0.0,"y":0.0,"z":0.0}` | x=前后, y=左右; 起始点为原点 |
| `orientation` | object | 姿态四元数 {x,y,z,w} | `{"x":0,"y":0,"z":0,"w":1}` | w=1 表示朝向初始方向 |
| `linear` | object | 线速度 {x,y,z} (m/s) | `{"x":0.0,...}` | x=前进速度 |
| `angular` | object | 角速度 {x,y,z} (rad/s) | `{"x":0.0,...}` | z=转向角速度 |

**怎么用**: `position.x/y` 用于定位。`orientation` 四元数转 yaw 角: `yaw = 2*atan2(z,w)`。`linear.x > 0` 表示在前进。

---

### 11. heartbeat (系统心跳)

**用途**: 监控系统管理器是否存活。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 心跳是否新鲜 (5s 内) | `true` | false 时系统管理器可能已崩溃 |
| `stamp_sec` | int | 心跳时间戳秒 | `1786691653` | UTC 时间戳 |
| `stamp_nanosec` | int | 纳秒部分 | `624000000` | 精确时间 |
| `frame_id` | string | 帧标识 | `"system"` | 来源标识 |

**怎么用**: `fresh=false` 持续超过 10 秒说明系统管理器可能停止，需现场检查。

---

### 12. cpu_freq (CPU 频率)

**用途**: 监控 CPU 各核心频率。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `true` | false 时频率数据过时 |
| `cpu_freq` | object | CPU 频率数据 | 见下 | 含 24 核 + 汇总 |
| `cpu_freq.cpufreq_dic.cpu` | float | 当前总频率 (MHz) | `3664.67` | 整体 CPU 频率 |
| `cpu_freq.cpufreq_dic.cpu_max` | float | 最大频率 (MHz) | `4367.0` | CPU 规格 |
| `cpu_freq.cpufreq_dic.cpu_min` | float | 最小频率 (MHz) | `599.0` | 节能频率 |
| `cpu_freq.cpufreq_dic.cpu_avg` | float | 平均频率 (MHz) | `3663.84` | 整体平均 |
| `cpu_freq.cpufreq_dic.cpu_0` | float | 核0频率 (MHz) | `4360.22` | 逐核监控 |

**怎么用**: 频率持续低于 `cpu_min` 的 2 倍可能影响控制实时性。`cpu_max=4367` 表示 CPU 是 ~4.4GHz 规格。

---

### 13. teleop_state (遥操作状态)

**用途**: 判断机器人是否处于遥操作模式。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `true` | false 时状态过时 |
| `state` | string | 遥操作状态 | `"idle"` | idle=未在遥操作; active=正在遥操作 |

**怎么用**: `state=idle` 时机器人未在遥控。`state=active` 时外部遥控器有控制权，画布控制卡应避免冲突。

---

### 14. remote_command (遥控指令)

**用途**: 监控外部遥控器下发的按键指令。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `true` | false 时无最新指令 |
| `axes` | array | 摇杆轴值列表 | `[]` | 通常为空，有摇杆时有值 |
| `buttons` | array | 按钮状态数组 | `[2,0,0,1,0]` | 索引对应按钮编号，值为按下状态 |

**buttons 数组含义** (5 个按钮):
- `buttons[0]`: 按钮 0 状态 (0=未按, 1=按下, 2=释放)
- `buttons[1]`: 按钮 1 状态
- `buttons[2]`: 按钮 2 状态
- `buttons[3]`: 按钮 3 状态
- `buttons[4]`: 按钮 4 状态

**怎么用**: 监控遥控器按键。值 `1`=按下中, `2`=刚释放, `0`=未按。配合 teleop_state 判断遥控器操作。

---

### 15. end_effector_pose (末端位姿)

**用途**: 获取机械臂末端执行器位姿（抓取规划用）。

| 字段 | 类型 | 说明 | 示例值 | 怎么用 |
|------|------|------|--------|--------|
| `fresh` | bool | 数据新鲜度 | `false` | false 时无末端位姿数据 |
| `available` | bool | 是否收到过消息 | `false` | publisher 存在但不持续发数据 |
| `source_topic` | string | 数据来源 | `"/mobile_manipulator/end_effector_pose"` | MPC 发布 |
| `message` | string | 状态描述 | `"未收到末端位姿消息"` | MPC 未激活时无数据 |

**怎么用**: `available=false` 说明 MPC (模型预测控制) 未激活。需要 MPC 节点运行后才有数据。

---

## 二、Actuator 卡片 (5 张)

### 16. base_drive (底盘控制)

**用途**: 控制底盘前进、后退、转向。

**调用**: `action=<动作>&speed_mps=<速度>&duration_s=<时间>`

| action | 附加参数 | 说明 | 示例 |
|--------|----------|------|------|
| `start` | - | 检查控制条件 | `action=start` |
| `forward` | speed_mps, duration_s | 前进 | `action=forward&speed_mps=0.1&duration_s=1.0` |
| `backward` | speed_mps, duration_s | 后退 | `action=backward&speed_mps=0.05&duration_s=0.5` |
| `turn_left` | turn_speed_radps, duration_s | 原地左转 | `action=turn_left&turn_speed_radps=0.2&duration_s=1.0` |
| `turn_right` | turn_speed_radps, duration_s | 原地右转 | `action=turn_right&turn_speed_radps=0.2&duration_s=1.0` |
| `move` | linear_x, angular_z, duration_s | 高级组合 | `action=move&linear_x=0.1&angular_z=0.0&duration_s=1.0` |
| `cancel` | - | 立即停车 | `action=cancel` |
| `info` | - | 查看状态 | `action=info` |

**参数范围**:
- `speed_mps`: 0.01 ~ 0.20 m/s (默认 0.1)
- `turn_speed_radps`: 0.01 ~ 0.40 rad/s (默认 0.2)
- `linear_x`: -0.20 ~ 0.20 m/s
- `angular_z`: -0.40 ~ 0.40 rad/s
- `duration_s`: 0.1 ~ 2.0 s (默认 0.5)

**info 返回字段**:
| 字段 | 说明 | 示例 |
|------|------|------|
| `ok` | 操作是否成功 | `true` |
| `state` | 当前状态 | `"idle"` |
| `active_command` | 当前执行中的命令 | `null` (空闲时) |
| `safety.ros_publisher_available` | ROS 发布者是否可用 | `true` |
| `safety.control_mode` | 控制模式 | `"direct_velocity_interface"` |
| `safety.q5_fsm.state` | FSM 状态 | `-1` (ERROR) |

---

### 17. arm_control (手臂控制)

**用途**: 控制单个手臂关节到指定角度。

**调用**: `action=<关节名>&<关节参数>_rad=<角度>`

| action | 参数 | 说明 | 范围 (rad) |
|--------|------|------|------------|
| `left_shoulder_pitch_joint` | left_shoulder_pitch_rad | 左肩俯仰 | -2.79 ~ 2.79 |
| `left_shoulder_roll_joint` | left_shoulder_roll_rad | 左肩侧摆 | -0.24 ~ 1.83 |
| `left_arm_yaw_joint` | left_arm_yaw_rad | 左臂偏航 | -2.62 ~ 2.62 |
| `left_elbow_pitch_joint` | left_elbow_pitch_rad | 左肘俯仰 | -2.27 ~ 0.09 |
| `left_elbow_yaw_joint` | left_elbow_yaw_rad | 左肘偏航 | -2.62 ~ 2.62 |
| `left_wrist_pitch_joint` | left_wrist_pitch_rad | 左腕俯仰 | -1.05 ~ 1.05 |
| `left_wrist_roll_joint` | left_wrist_roll_rad | 左腕侧摆 | -1.05 ~ 1.05 |
| `right_shoulder_pitch_joint` | right_shoulder_pitch_rad | 右肩俯仰 | -2.79 ~ 2.79 |
| `right_shoulder_roll_joint` | right_shoulder_roll_rad | 右肩侧摆 | -1.83 ~ 0.24 |
| `right_arm_yaw_joint` | right_arm_yaw_rad | 右臂偏航 | -2.62 ~ 2.62 |
| `right_elbow_pitch_joint` | right_elbow_pitch_rad | 右肘俯仰 | -2.27 ~ 0.09 |
| `right_elbow_yaw_joint` | right_elbow_yaw_rad | 右肘偏航 | -2.62 ~ 2.62 |
| `right_wrist_pitch_joint` | right_wrist_pitch_rad | 右腕俯仰 | -1.05 ~ 1.05 |
| `right_wrist_roll_joint` | right_wrist_roll_rad | 右腕侧摆 | -1.05 ~ 1.05 |
| `start` | - | 检查连接 | - |
| `cancel` | - | 取消微调 | - |
| `info` | - | 查看状态 | - |

**怎么用**: `action=left_elbow_pitch_joint&left_elbow_pitch_rad=-1.0` 设置左肘到 -1.0 rad (约 -57°)。单次步进不超过 0.05 rad。

---

### 18. hand_control (手部控制)

**用途**: 控制左右手手指弯曲和拇指旋转。

| action | 附加参数 | 说明 | 示例 |
|--------|----------|------|------|
| `open_hand` | side | 张开整手 | `action=open_hand&side=left` |
| `close_hand` | side | 合拢整手 | `action=close_hand&side=right` |
| `set_hand` | side, curl_rad | 设置整手弯曲度 | `action=set_hand&side=both&curl_rad=0.5` |
| `set_finger` | side, finger, curl_rad, rotation_rad | 设置单指 | `action=set_finger&side=left&finger=thumb&curl_rad=0.3&rotation_rad=0.5` |
| `set` | targets (JSON数组) | 高级多关节 | `action=set&targets=[{"joint_name":"left_hand_index_joint1","position_rad":0.5}]` |
| `cancel` | - | 取消保持 | - |
| `info` | - | 查看状态 | - |

**参数范围**:
- `curl_rad`: 0.0 (张开) ~ 1.0 (完全弯曲)
- `rotation_rad`: 0.0 ~ 1.0 (仅拇指)
- `side`: left / right / both

---

### 19. hand_gesture (预设手势)

**用途**: 快速执行预设手势。

| action | 说明 | 示例 |
|--------|------|------|
| `open_hand` | 张手 | `action=open_hand&side=right` |
| `light_grip` | 轻握 | `action=light_grip&side=both` |
| `closed_fist` | 握拳 | `action=closed_fist&side=right` |
| `point` | 指向 | `action=point&side=right` |
| `pinch` | 捏取 | `action=pinch&side=left` |
| `victory` | 胜利 (V) | `action=victory&side=right` |
| `thumbs_up` | 点赞 | `action=thumbs_up&side=right` |
| `ok_sign` | OK | `action=ok_sign&side=left` |
| `three` | 比三 | `action=three&side=right` |
| `rock` | 摇滚 | `action=rock&side=right` |
| `cancel` | 取消 | - |
| `info` | 查看状态 | - |

---

### 20. head_control (头部控制)

**用途**: 控制头部偏航（左右转头）和俯仰（抬头/低头）。

| action | 参数 | 说明 | 范围 (rad) | 示例 |
|--------|------|------|------------|------|
| `neck_yaw` | neck_yaw_rad | 左右转头 | -0.79 ~ 0.79 | `action=neck_yaw&neck_yaw_rad=0.3` (右转) |
| `neck_pitch` | neck_pitch_rad | 抬头/低头 | -0.26 ~ 0.70 | `action=neck_pitch&neck_pitch_rad=0.3` (抬头) |
| `cancel` | - | 取消 | - | - |
| `info` | - | 查看状态 | - | - |

**方向约定**: 正值=抬头/右转, 负值=低头/左转。单次步进不超过 0.025 rad。

---

## 三、Resource 卡片 (1 张)

### 21. model (URDF 模型)

**用途**: 提供 3D 骨架渲染所需的 URDF 模型。

**调用**: `action=model`

| 字段 | 说明 | 示例 |
|------|------|------|
| `urdf` | URDF XML 文本 | (完整 XML) |
| `model` | 模型名 | `"RobotEra Q5"` |
| `geometry` | 几何标识 | `"q5_wr1_lite_robot_description"` |
| `source_topic` | ROS 模型来源 | `"/robot_description"` |
| `mesh_package` | 网格资源路径 | `"robot_control/description/wr1/lite/meshes"` |

**怎么用**: 获取 URDF 后配合 `joints` 卡的实时关节数据做 3D 渲染。

---

## 四、当前实机状态总结

| 卡片 | 状态 | 说明 |
|------|------|------|
| joints | ✅ fresh | 34 关节实时数据正常 |
| joints_state | ✅ fresh | 完整关节数据正常 |
| robot_ready | ✅ | robot_state=ACTIVE, ready=true |
| battery | ✅ | 81%, 64.5V, 29°C |
| system_health | ✅ | 健康正常, 最高温 57°C (neck_pitch) |
| hand_state | ✅ fresh | 左右手各 6 关节正常 |
| odom | ✅ fresh | 位置 (0,0), 静止 |
| heartbeat | ✅ fresh | 系统存活 |
| cpu_freq | ✅ fresh | 24 核, 平均 3664 MHz |
| teleop_state | ✅ fresh | state=idle |
| remote_command | ✅ fresh | buttons=[2,0,0,1,0] |
| estop | ✅ fresh | 急停未激活, 但 FSM state=ERROR |
| nav_state | ❌ | 导航栈未运行 |
| diagnostics | ❌ | 发布器已连接但无消息 |
| end_effector_pose | ❌ | MPC 未激活, 无数据 |
| base_drive | ✅ idle | 空闲, 控制可用 |
| arm_control | ⚠️ disabled | 硬件未使能 |
| hand_control | ✅ idle | 空闲, 控制可用 |
| hand_gesture | ✅ idle | 空闲, 控制可用 |
| head_control | ✅ idle | 空闲, 控制可用 |
