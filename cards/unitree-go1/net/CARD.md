# net —— Go1 网络健康(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `unitree-go1` |
| 卡片名(MCP 工具名) | `net` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY`(高层/低层都出) |
| 作者 | `luoye-hcl` |
| 状态 | `offline-green`(离线测试全绿;2026-07-13 实机读到真实 wlan0 信号,完整样本待狗有电现采后升 accepted) |

## 能力

报告驱动所在主机的网络健康:主机名、主用 IPv4、Wi-Fi 信号强度。联调时无线易掉,这张卡让大模型/人一眼看清链路是否还在。**纯系统读**(不经硬件帧)→ 不套状态卡"无新帧抑制",始终可读。

## 接口

- 输出 topic:`/{ns}/state/net`  格式:`data/json`
- 采样频率:`0.5` Hz
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`,core 不渲染执行按钮)

### 字段

| 字段 | 含义 | 单位 |
|---|---|---|
| `available` | 本卡是否可用(恒 `true`,系统读) | — |
| `hostname` | 主机名 | — |
| `ipv4` | 主用出口网卡 IPv4(经 UDP connect 8.8.8.8 选默认路由,不真发包) | — |
| `wifi.available` | 是否读到活动无线网卡 | — |
| `wifi.iface` | 无线网卡名(如 `wlan0`) | — |
| `wifi.link_quality` | 链路质量(`/proc/net/wireless` 第 3 列) | — |
| `wifi.signal_dbm` | 信号电平 | dBm |
| `timestamp_ms` | 采集时间戳 | ms |
| `control_level` | 当前驱动控制等级 | — |

> Wi-Fi 读 `/proc/net/wireless`(Linux/狗);Mac 等无该文件的平台 → `wifi.available:false` 并给 `reason`(诚实标注,不伪造)。

## 数据来源 / 实现位置

- 源仓库:`luoye-hcl/go1-driver`
- 文件:`unitree/go1/plugins/mt_state.py`  类:`NetCard`(继承 `MtStateCard`,覆写 `_produce` 跳过硬件新鲜度抑制)
- 依赖:`plugins/mt_base.py`(状态卡基类/返回包络);仅用标准库 `socket` + 读 `/proc/net/wireless`,不碰硬件
- 注册:`unitree/go1/main.py`(MT HIGHLEVEL/LOWLEVEL 均出);驱动镜像 `go1`,MCP 端口 `15704`

## 状态说明

- 离线:`tests/test_mt_ext.py::TestNet`(返回含 `available/hostname/ipv4/wifi/timestamp_ms`;connected 且无新硬件帧时仍出数据)通过,`run_all.sh` 全绿。
- 实机:2026-07-13 在狗上读到**真实 wlan0**,`wifi.link_quality = 85`(联调掉线时一眼可辨),验证生效(见 `verification/`)。**完整 JSON 返回样本待狗有电现采后补齐、届时升 `accepted`**。
