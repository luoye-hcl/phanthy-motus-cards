# Q5 画布卡片验收文档

> 机器人: RobotEra Q5 (46 DOF, 差速底盘)  
> 驱动容器: `q5-driver-huang` (端口 15794)  
> Agent Core: `phanthy-motus-agent-core-1` (端口 15678)  
> MCP 服务 ID: `mcp-1786351358`  
> 日期: 2026-08-14

---

## 一、Sensor 卡片 (15 张)

### 1. joints (骨架可视化)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 (5s 内) | 判断关节数据是否实时 |
| `joint_count` | 关节总数 (34) | 确认数据完整性 |
| `position_unit` | 位置单位 (rad) | 单位换算依据 |
| `joints` | 关节数组, 每项含 `name` 和 `q` (弧度) | URDF 3D 可视化的驱动数据 |
| `source_topic` | /joint_states | 数据来源 |

**使用方式**: `action=info` 获取当前骨架快照, 配合 `model` 卡的 URDF 做 3D 渲染。

---

### 2. joints_state (完整关节状态)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断是否可用 |
| `joint_count` | 关节总数 (34) | 完整性校验 |
| `groups.body` | 身体关节 (22个), 每个含 position/velocity/effort | 运动状态监控 |
| `groups.left_hand` | 左手关节 (6个) | 手指状态监控 |
| `groups.right_hand` | 右手关节 (6个) | 手指状态监控 |
| `source_topic` | /joint_states | 数据来源 |

**使用方式**: `action=info` 获取分组后的完整关节状态。每个关节包含 position (弧度)、velocity (rad/s)、effort (力矩)。

**精简说明**: 原版有 positions/velocities/efforts 三组扁平字典 + groups 重复输出, 现已合并为 groups 内每关节一个对象。

---

### 3. robot_ready (就绪状态)

| 字段 | 说明 | 用途 |
|------|------|------|
| `robot_state` | 机器人状态标签 (INIT/IDLE/READY/ACTIVE/E_STOP/ERROR) | 判断机器人当前业务状态 |
| `ready` | 是否可控制 (READY 或 ACTIVE) | 控制前置条件 |
| `motion_ready` | 运动管理器是否就绪 | 运动指令前置条件 |
| `motion_manager_active` | 运动管理器生命周期是否 active | 底层运动服务状态 |
| `message_fresh` | /xbot_state 消息是否新鲜 | 数据可靠性 |
| `message` | 人类可读状态摘要 | 快速理解 |

**使用方式**: `action=info` 查询。控制动作前必须确认 `ready=true` 且 `motion_ready=true`。

**精简说明**: 原版有 message_freshness 嵌套对象、robot_status 嵌套对象、motion_manager_lifecycle 嵌套对象、ready_scope 等冗余字段, 现已扁平化为核心字段。

---

### 4. battery (电池)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断电池数据是否实时 |
| `percentage` | 电量百分比 (0-100) | 低电量预警 |
| `level` | 电量等级 (full/normal/low/critical/unknown) | 快速判断 |
| `voltage_v` | 电压 (V) | 电池健康判断 |
| `temperature_c` | 温度 (°C) | 过热保护 |
| `message` | 状态摘要 | 快速理解 |

**使用方式**: `action=info` 查询。`level=critical` 时应停止运动。

---

### 5. system_health (运行健康)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 必需来源是否新鲜 | 整体健康判断 |
| `robot_state` | 机器人状态 (READY/ACTIVE等) | 业务状态 |
| `robot_active` | 机器人是否在运动中 | 运动状态判断 |
| `temperature` | 温度摘要 (max/min 传感器名和温度) | 过热监控 |
| `motion` | 运动状态事件 (事件驱动, 可能为 null) | 运动事件追踪 |
| `faults` | 聚合故障列表 | 故障诊断 |
| `message` | 健康摘要 | 快速理解 |

**使用方式**: `action=info` 查询。`fresh=false` 或 `faults` 中有 `is_active=true` 且 `level<5` 时需关注。

**精简说明**: 原版每个来源都有 available/fresh/age_ms/received_at_ms/source_topic/source_publisher_count/report_state/event_driven/data 共 9 个字段 × 4 来源 = 36 个字段, 现已提取核心信息为扁平结构。

---

### 6. hand_state (手部关节状态)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断数据可靠性 |
| `groups.left_hand` | 左手 6 个关节的 position/velocity/effort | 手部状态监控 |
| `groups.right_hand` | 右手 6 个关节的 position/velocity/effort | 手部状态监控 |
| `source_topic` | /joint_states | 数据来源 |

**使用方式**: `action=info` 查询。与 joints_state 的 hand 部分一致, 但独立发布便于手部专用画布。

---

### 7. nav_state (导航状态)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断导航数据可靠性 |
| `status` | 导航状态文本 | 透传厂商导航状态 |
| `publisher_connected` | 发布者是否在线 | 判断导航服务是否运行 |
| `source_topic` | /era_nav/nav_status | 数据来源 |

**使用方式**: `action=info` 查询。注意: 此卡只读导航状态, 不执行导航。

---

### 8. estop (急停状态)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断状态可靠性 |
| `estop_active` | 急停是否激活 | 安全判断 |
| `state` | 厂商状态码 | 底层状态 |
| `message` | 状态描述 | 快速理解 |

**使用方式**: `action=info` 查询。`estop_active=true` 时所有控制卡应拒绝执行。

---

### 9. diagnostics (诊断)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断诊断数据可靠性 |
| `items` | 诊断项列表, 每项含 level/name/hw_id/key_values | 硬件/软件诊断 |
| `source_topic` | /diagnostics_agg | 数据来源 |

**使用方式**: `action=info` 查询。关注 `level >= ERROR(2)` 的项。

---

### 10. odom (里程计)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断定位可靠性 |
| `position` | 底盘位置 {x, y, z} (m) | 定位 |
| `orientation` | 姿态四元数 {x, y, z, w} | 朝向 |
| `linear` | 线速度 {x, y, z} (m/s) | 运动速度 |
| `angular` | 角速度 {x, y, z} (rad/s) | 转向速度 |
| `source_topic` | /wr1_base_drive_controller/odom | 数据来源 |

**使用方式**: `action=info` 查询底盘位置和速度。

---

### 11. heartbeat (系统心跳)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 心跳是否新鲜 (5s 内) | 系统存活判断 |
| `stamp_sec` | 心跳时间戳 (秒) | 时间同步参考 |
| `frame_id` | 帧标识 | 来源标识 |
| `source_topic` | /system/heartbeat | 数据来源 |

**使用方式**: `action=info` 查询。`fresh=false` 表示系统管理器可能已停止。

---

### 12. cpu_freq (CPU 频率)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断数据可靠性 |
| `frequencies` | 各 CPU 核心频率列表 (MHz) | 性能监控 |
| `source_topic` | /cpu_freq | 数据来源 |

**使用方式**: `action=info` 查询。频率过低可能影响控制实时性。

---

### 13. teleop_state (遥操作状态)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断状态可靠性 |
| `state` | 遥操作状态数据 | 遥操作模式判断 |
| `source_topic` | /teleop_state | 数据来源 |

**使用方式**: `action=info` 查询。判断机器人是否处于遥操作模式。

---

### 14. remote_command (遥控指令)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断数据可靠性 |
| `command` | 最近遥控指令内容 | 遥控指令监控 |
| `source_topic` | /send_remote/command | 数据来源 |

**使用方式**: `action=info` 查询。监控外部下发的遥控指令。

---

### 15. end_effector_pose (末端位姿)

| 字段 | 说明 | 用途 |
|------|------|------|
| `fresh` | 数据是否新鲜 | 判断数据可靠性 |
| `pose` | 末端执行器位姿 | 抓取规划 |
| `source_topic` | /mobile_manipulator/end_effector_pose | 数据来源 |

**使用方式**: `action=info` 查询。注意: publisher 存在但不一定持续发数据 (MPC 未激活时)。

---

## 二、Actuator 卡片 (5 张)

### 16. base_drive (底盘控制)

| 参数 | 说明 | 范围 | 默认值 |
|------|------|------|--------|
| `action` | 动作类型 | start/forward/backward/turn_left/turn_right/move/cancel/info | - |
| `speed_mps` | 移动速度 | 0.01-0.20 m/s | 0.1 |
| `turn_speed_radps` | 转向速度 | 0.01-0.40 rad/s | 0.2 |
| `linear_x` | 前后速度 (move 模式) | -0.20-0.20 m/s | 0.1 |
| `angular_z` | 转向速度 (move 模式) | -0.40-0.40 rad/s | 0.0 |
| `duration_s` | 持续时间 | 0.1-2.0 s | 0.5 |

**使用方式**: `action=forward&speed_mps=0.1&duration_s=1.0` 前进 1 秒。每次动作到时自动停车。

---

### 17. arm_control (手臂控制)

| 参数 | 说明 | 范围 |
|------|------|------|
| `action` | 指定关节名或 cancel/info | 14 个关节名 |
| `{joint}_rad` | 目标角度 | 各关节不同 |

**关节限制**:
- 肩俯仰: ±2.79 rad
- 肩侧摆: 左[-0.24, 1.83] / 右[-1.83, 0.24]
- 臂偏航: ±2.62 rad
- 肘俯仰: [-2.27, 0.09] rad
- 肘偏航: ±2.62 rad
- 腕俯仰: ±1.05 rad
- 腕侧摆: ±1.05 rad

**使用方式**: `action=left_elbow_pitch_joint&left_elbow_pitch_rad=-1.0` 设置左肘角度。

---

### 18. hand_control (手部控制)

| 参数 | 说明 | 范围 |
|------|------|------|
| `action` | open_hand/close_hand/set_hand/set_finger/set/cancel/info | - |
| `side` | 执行侧 | left/right/both |
| `finger` | 手指 | thumb/index/middle/ring/pinky |
| `curl_rad` | 弯曲角度 | 0.0-1.0 rad |
| `rotation_rad` | 拇指旋转 | 0.0-1.0 rad |
| `targets` | 多关节目标数组 | 最多 12 个 |

**使用方式**: `action=open_hand&side=left` 张开左手。

---

### 19. hand_gesture (预设手势)

| 参数 | 说明 |
|------|------|
| `action` | open_hand/light_grip/closed_fist/point/pinch/victory/thumbs_up/ok_sign/three/rock/cancel/info |
| `side` | left/right/both |

**使用方式**: `action=victory&side=right` 右手比胜利手势。

---

### 20. head_control (头部控制)

| 参数 | 说明 | 范围 |
|------|------|------|
| `action` | neck_yaw/neck_pitch/cancel/info | - |
| `neck_yaw_rad` | 偏航角度 | -0.79-0.79 rad |
| `neck_pitch_rad` | 俯仰角度 | -0.26-0.70 rad |

**使用方式**: `action=neck_pitch&neck_pitch_rad=0.3` 抬头。正值抬头, 负值低头。

---

## 三、Resource 卡片 (1 张)

### 21. model (URDF 模型)

| 字段 | 说明 | 用途 |
|------|------|------|
| `urdf` | Q5 身体骨架 URDF XML | 3D 可视化渲染 |
| `model` | 模型名 "RobotEra Q5" | 标识 |
| `geometry` | 几何描述标识 | 渲染引擎匹配 |
| `mesh_package` | 网格资源路径 | 外观加载 |

**使用方式**: `action=model` 获取 URDF, 配合 `joints` 卡的实时数据做 3D 骨架渲染。

---

## 四、通用调用约定

### MCP 调用格式
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "<卡名>",
    "arguments": {"action": "info"}
  }
}
```

### Sensor 卡片 action
- `info`: 读取当前数据 (主要用法)
- `start`: 启动卡片 ROS2 发布 (画布自动调用)
- `stop`: 停止发布

### Actuator 卡片 action
- 控制卡 action 即为具体动作名 (如 `forward`, `open_hand`)
- `start`: 检查连接和状态
- `cancel`: 取消当前动作
- `info`: 查看当前运动状态和安全条件

### 数据新鲜度
- `fresh=true`: 5 秒内收到过消息
- `fresh=false`: 数据过期或未收到
- `stale=true`: 已有数据但超过 5 秒未更新
