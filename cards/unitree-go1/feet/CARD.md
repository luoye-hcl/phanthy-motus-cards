# feet —— Go1 足端力/足端位姿(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `unitree-go1` |
| 卡片名(MCP 工具名) | `feet` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY`(高层/低层都出) |
| 作者 | `luoye-hcl` |
| 状态 | `accepted`(2026-07-14 实机验收通过) |

## 能力

读取 Go1 四条腿的**足底力原始值**;在高层控制态下另带**足端相对机身的位置/速度**。用于判断着地/承重、姿态与步态观察,供大模型或人监控机器狗当前的支撑状态。

## 接口

- 输出 topic:`/{ns}/state/feet`  格式:`data/json`
- 采样频率:`10` Hz
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`,core 不渲染执行按钮)

### 字段

| 字段 | 含义 | 单位 |
|---|---|---|
| `order` | 四足顺序,固定 `["FR","FL","RR","RL"]` | — |
| `foot_force_raw` | 四足足底力原始值(与 order 对应) | 原始计数 |
| `position_to_body[]` | 各足相对机身的位置 `{x,y,z}`(仅高层态) | m |
| `speed_to_body[]` | 各足相对机身的速度 `{x,y,z}`(仅高层态) | m/s |
| `timestamp_ms` | 采集时间戳 | ms |
| `control_level` | 当前驱动控制等级 | — |

## 数据来源 / 实现位置

- 源仓库:`luoye-hcl/go1-driver`
- 文件:`unitree/go1/plugins/mt_state.py`  类:`FeetCard`(继承 `MtStateCard`)
- 依赖:`plugins/mt_base.py`(状态卡基类/返回包络)、`go1_ctrl.py`(唯一硬件入口,factory 后端读真实 HighState)
- 注册:`unitree/go1/main.py`(MT HIGHLEVEL/LOWLEVEL 均出);驱动镜像 `go1`,MCP 端口 `15704`

## 状态说明

- 离线:`tests/test_mt_cards.py` 覆盖(feet 字段 `order[0]=="FR"`、含 `foot_force_raw`),`run_all.sh` 全绿。
- 实机:2026-07-14 经 factory 后端读到真实足底力(站立 ~250、阻尼 ~40),core 网页监控页 DATA STREAMS 正常出数据流,**验收通过**。详见 `verification/`。
