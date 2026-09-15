# 验收证据 —— net

- **当前状态**:`offline-green`(离线测试全绿 + 实机只读已读到真实 wlan0;完整 JSON 样本待采后升 `accepted`)

## 离线测试

- `tests/test_mt_ext.py::TestNet`:
  - `test_read_fields` —— 返回含 `available` / `hostname` / `ipv4` / `wifi` / `timestamp_ms`
  - (connected 且无新硬件帧时)net 仍出数据 —— 印证覆写 `_produce` 跳过了硬件新鲜度抑制
- 运行结果:`Ran 27 tests ... OK`(`test_mt_ext.py` 全绿,2026-07-15 本地复跑)。

## 实机只读验证(2026-07-13)

- 在狗(主机名 `unitree5990`)上经 MCP 只读调用 `{"action":"read"}`。
- 读到**真实 wlan0**:`wifi.iface = "wlan0"`、`wifi.link_quality = 85`(联调掉线时可据此判断链路)。
- 参见 `luoye-hcl/go1-driver:docs/WORKLOG_2026-07-13.md`("net 网络健康:实机读到真实 wlan0 信号 85")。

## 待补(升 accepted 的条件)

- 狗上电后现采一段**完整 JSON 返回样本**(`{available, hostname, ipv4, wifi:{available, iface, link_quality, signal_dbm}, timestamp_ms, control_level}`)+ 采集时间/环境;
- core 网页监控页 DATA STREAMS 面板呈现该卡数据流截图/记录。
- 齐备后:新增 `verification/accepted.md`、`metadata.json` 加 `accepted_date` 并把 `status` 改 `accepted`、`version` 递增、`CHANGELOG` 加条。
