# CHANGELOG — net

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.0.0 — 2026-07-15 — luoye-hcl

- 首次收录。Go1 网络健康只读传感器卡,0.5Hz,`/{ns}/state/net`。
- 报告主机名/主用 IPv4/Wi-Fi 信号(`/proc/net/wireless`);纯系统读,覆写 `_produce` 跳过硬件新鲜度抑制,始终可读。
- 离线测试全绿(`test_mt_ext.py::TestNet`);2026-07-13 实机读到真实 wlan0 `link_quality=85`,完整 JSON 样本待采后升 `accepted`。
