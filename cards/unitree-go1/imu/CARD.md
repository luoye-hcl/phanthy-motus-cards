# imu —— Go1 IMU 姿态/角速度/加速度(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `unitree-go1` |
| 卡片名(MCP 工具名) | `imu` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY` |
| 作者 | `luoye-hcl` |
| 状态 | `accepted`(2026-07-14 实机验收通过) |

## 能力

读取 Go1 机身 IMU 的**四元数姿态、角速度、加速度、欧拉角、IMU 温度**。供大模型/人判断机身朝向与运动状态,是姿态/跌倒/运动安全判断的数据基础。

## 接口

- 输出 topic:`/{ns}/state/imu`  格式:`data/json`
- 采样频率:`20` Hz
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`)

### 字段

| 字段 | 含义 | 单位 |
|---|---|---|
| `quaternion_wxyz` | 姿态四元数 `[w,x,y,z]` | — |
| `gyroscope_rad_s` | 三轴角速度 `[x,y,z]` | rad/s |
| `accelerometer_m_s2` | 三轴加速度 `[x,y,z]`(静止时 z≈9.8) | m/s² |
| `rpy_rad` | 欧拉角 `[roll,pitch,yaw]` | rad |
| `temperature_c` | IMU 温度 | ℃ |
| `attitude_may_drift` | 姿态漂移提示(加速运动时姿态可能漂移) | bool |
| `timestamp_ms` | 采集时间戳 | ms |
| `control_level` | 当前驱动控制等级 | — |

## 数据来源 / 实现位置

- 源仓库:`luoye-hcl/go1-driver`
- 文件:`unitree/go1/plugins/mt_state.py`  类:`ImuCard`(继承 `MtStateCard`)
- 依赖:`plugins/mt_base.py`、`go1_ctrl.py`(factory 后端读真实 HighState.imu)
- 注册:`unitree/go1/main.py`(ANY 级,高低层均出);驱动镜像 `go1`,MCP 端口 `15704`

## 状态说明

- 离线:`tests/test_mt_cards.py` 覆盖 imu 字段;`run_all.sh` 全绿。
- 实机:2026-07-14 读到真实四元数、温度 79℃、静止时加速度 z≈9.64,core 网页数据流正常,**验收通过**。详见 `verification/`。
