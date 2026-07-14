# loco_state —— Go1 运动状态(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `unitree-go1` |
| 卡片名(MCP 工具名) | `loco_state` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `HIGHLEVEL`(高层运动状态,仅高层出) |
| 作者 | `luoye-hcl` |
| 状态 | `accepted`(2026-07-14 实机验收通过) |

## 能力

读取 Go1 的**高层运动状态**:当前模式(idle/force_stand/walk/damp…)、步态、里程(机身位置)、机身高度、机身系速度、偏航角速度。供大模型/人判断"狗当前处于什么运动状态、能不能下一步动作"。

## 接口

- 输出 topic:`/{ns}/loco/state`  格式:`data/json`
- 采样频率:`10` Hz
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`)

### 字段

| 字段 | 含义 | 单位 |
|---|---|---|
| `mode` / `mode_name` | 运动模式码 / 名称(如 1=force_stand、7=damp) | — |
| `gait_type` / `gait_name` | 步态码 / 名称 | — |
| `foot_raise_height_m` | 抬脚高度 | m |
| `position_m` | 机身里程位置 `[x,y,z]` | m |
| `body_height_m` | 机身高度 | m |
| `velocity_body_mps` | 机身系速度 `{forward, lateral}` | m/s |
| `velocity_index_2_raw` | 官方 velocity[2] 原始值(语义与 yawSpeed 冲突,不命名) | 原始 |
| `yaw_speed_rad_s` | 偏航角速度 | rad/s |
| `timestamp_ms` | 采集时间戳 | ms |
| `control_level` | 当前驱动控制等级 | — |

## 数据来源 / 实现位置

- 源仓库:`luoye-hcl/go1-driver`
- 文件:`unitree/go1/plugins/mt_state.py`  类:`LocoStateCard`(继承 `MtStateCard`)
- 依赖:`plugins/mt_base.py`、`go1_ctrl.py`(`get_high_state()`,factory 后端读真实 HighState)
- 注册:`unitree/go1/main.py`(仅 HIGHLEVEL);驱动镜像 `go1`,MCP 端口 `15704`

## 状态说明

- 离线:`tests/test_mt_cards.py` 覆盖(含 `mode_name`、`velocity_body_mps`);`run_all.sh` 全绿。
- 实机:2026-07-14 读到真实运动态(站立 mode=1 force_stand / 阻尼 mode=7 damp、机身高度 0.30m↔0.05m 随状态变),core 网页数据流正常,**验收通过**。详见 `verification/`。
