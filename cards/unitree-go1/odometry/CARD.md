# odometry —— Go1 里程计(只读传感器卡 + reset_origin)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `unitree-go1` |
| 卡片名(MCP 工具名) | `odometry` |
| 类型 | `sensor`(只读数据流,无执行按钮;另有 `reset_origin` 经 MCP 可调) |
| 控制等级 | `HIGHLEVEL`(高层态才有 position;低层态无位置) |
| 作者 | `luoye-hcl` |
| 状态 | `offline-green`(离线测试全绿;2026-07-13 实机只读已验证,完整样本待狗有电现采后升 accepted) |

## 能力

报告狗的里程:当前世界系 position/yaw、累计总路程、相对起点位移。让高层规划/大模型知道"走了多远、在哪、离起点多远"。坐标系 = 狗上电起点为原点(x 前、y 左)。起点默认取首帧,可用 `reset_origin` 重置。

## 接口

- 输出 topic:`/{ns}/state/odometry`  格式:`data/json`
- 采样频率:`5` Hz
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`,core 不渲染执行按钮)
- 重置起点:`{"action":"reset_origin"}` —— 把当前位置设为新原点(经 MCP 调用,UI 上不出按钮)

### 字段

| 字段 | 含义 | 单位 |
|---|---|---|
| `position_m` | 当前世界系位置 `[x, y, z]` | m |
| `yaw_rad` | 当前航向角 | rad |
| `total_distance_m` | 累计总路程(里程计累加,跳变丢弃) | m |
| `origin_m` | 起点 `[x, y]`(首帧或 reset_origin 时设) | m |
| `displacement_m.dx` / `.dy` | 相对起点的位移分量 | m |
| `displacement_m.distance` | 相对起点的直线距离 `hypot(dx,dy)` | m |
| `offline` | 后端是否离线(离线 fake 时 `true`) | — |
| `timestamp_ms` | 采集时间戳 | ms |
| `control_level` | 当前驱动控制等级 | — |

## 数据来源 / 实现位置

- 源仓库:`luoye-hcl/go1-driver`
- 文件:`unitree/go1/plugins/mt_state.py`  类:`OdometryCard`(继承 `MtStateCard`,覆写 `dispatch` 增 `reset_origin`)
- 依赖:`plugins/mt_base.py`(状态卡基类/返回包络)、`go1_ctrl.py`(`get_odometry()`,factory 后端由 HighState 累计 position/yaw/里程)
- 注册:`unitree/go1/main.py`(仅 MT HIGHLEVEL 出;低层态无 position 不出);驱动镜像 `go1`,MCP 端口 `15704`

## 状态说明

- 离线:`tests/test_mt_ext.py::TestOdometry`(结构含 `position_m/yaw_rad/total_distance_m/displacement_m/origin_m`;`reset_origin` 重置;工具只读无 action 按钮;里程累加、跳变丢弃)通过,`run_all.sh` 全绿。
- 实机:2026-07-13 经 factory 后端实机只读验证读取 OK(见 `verification/`)。**完整 JSON 返回样本待狗有电现采后补齐、届时升 `accepted`**。
