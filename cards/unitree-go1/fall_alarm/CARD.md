# fall_alarm —— Go1 跌倒/侧翻告警(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `unitree-go1` |
| 卡片名(MCP 工具名) | `fall_alarm` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY`(高层/低层都出) |
| 作者 | `luoye-hcl` |
| 状态 | `offline-green`(离线测试全绿;2026-07-13 实机只读已验证,完整样本待狗有电现采后升 accepted) |

## 能力

由 IMU 的 roll/pitch 幅度判定机身姿态告警等级 `ok` / `tilted` / `fallen`,并给出倾角与人话提示,为运动安全兜底。供大模型或人在指挥运动前后一眼判断"狗还站得稳吗 / 是不是翻了"。

## 接口

- 输出 topic:`/{ns}/state/fall_alarm`  格式:`data/json`
- 采样频率:`10` Hz
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`,core 不渲染执行按钮)
- 阈值可配(`config`):`tilt_warn_rad`(默认 `0.6` rad ≈ 34°)、`fall_rad`(默认 `1.2` rad ≈ 69°)

### 字段

| 字段 | 含义 | 单位 |
|---|---|---|
| `status` | 告警等级:`ok` / `tilted`(明显倾斜) / `fallen`(已翻倒) | — |
| `roll_rad` / `pitch_rad` | 当前横滚/俯仰角 | rad |
| `roll_deg` / `pitch_deg` | 当前横滚/俯仰角 | 度 |
| `tilt_warn_rad` | 触发 `tilted` 的阈值 | rad |
| `fall_rad` | 触发 `fallen` 的阈值 | rad |
| `hint` | 人话提示(如"姿态正常"/"机身明显倾斜"/"已跌倒") | — |
| `timestamp_ms` | 采集时间戳 | ms |
| `control_level` | 当前驱动控制等级 | — |

> 判定量 = `max(abs(roll), abs(pitch))`:≥ `fall_rad` → `fallen`;≥ `tilt_warn_rad` → `tilted`;否则 `ok`。
> 依赖 IMU 帧;连接后无新帧则按 `NO_FEEDBACK` 抑制(不误报)。

## 数据来源 / 实现位置

- 源仓库:`luoye-hcl/go1-driver`
- 文件:`unitree/go1/plugins/mt_state.py`  类:`FallAlarmCard`(继承 `MtStateCard`)
- 依赖:`plugins/mt_base.py`(状态卡基类/返回包络)、`go1_ctrl.py`(唯一硬件入口,factory 后端读真实 HighState.imu)
- 注册:`unitree/go1/main.py`(MT HIGHLEVEL/LOWLEVEL 均出);驱动镜像 `go1`,MCP 端口 `15704`

## 状态说明

- 离线:`tests/test_mt_ext.py`(`TestFallAlarm`:`ok`/`tilted`/`fallen` 三档阈值断言)通过,`run_all.sh` 全绿。
- 实机:2026-07-13 经 factory 后端实机只读验证,姿态正常时返回 `status:"ok"`(见 `verification/`)。**完整 JSON 返回样本待狗有电现采后补齐、届时升 `accepted`**。
