# teleop_session —— 通用 recording-only Shadow 参考卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `generic-teleop-shadow`（不绑定机型） |
| MCP 工具 | `teleop_session` |
| 类型 / 控制等级 | `actuator` / `ANY`（只记录） |
| 模式 | `shadow` |
| 状态 | `offline-green`；不是硬件遥操验收 |

## 能力

这张卡只描述一个无机器人适配器的 Android OpenXR/WebRTC Shadow Driver。它接收严格帧、运行 fenced 会话，并产生 `would_apply` / `would_stop` 记录；`mode=shadow`、`actuation_enabled=false`、`hardware_output=false` 是不可切换的边界。当前默认采集端是 Core 中的一套共享 Native OpenXR 客户端代码，由 `meta` / `pico` flavor 分别生成 Quest 与 PICO APK；两者都不要求佩戴者在头显内打开 WebXR 页面或操作应用菜单。

`metadata.json.mcp_tool` 与 Driver 源提交 `68f07c4fb367effca19ce46007b0bbafce158fa6` 的默认 `teleop_session` descriptor 逐字段一致。默认 descriptor 中 `robot_id=null`；这表示参考实例未绑定任何机器人，不是可执行身份。

## 可见数据流

1. PC 上的 Core 控制台持有操作者身份、会话、租约、Live 确认和 Capture assignment；Meta/PICO 采集端都不持有这些控制权限。
2. 已配对的 `client_kind=native_openxr` 先连接 Core Capture WSS，只有收到 PC 手工签发的当前会话 assignment 后，才与 Driver 协商 ICE/DTLS/SCTP DataChannel；Pose 不经 MCP 转发。
3. Native RTC Frame 必须省略 `boot_id`、`session_id`、`epoch`、`fence`。Driver 从验票后的 peer binding 注入 authority，客户端不能覆盖。
4. 通过验证的帧只进入 recording final-dispatch；最新帧 mailbox 深度为 1，stop 有独立 ACK 记录，但不存在 publisher、motor API 或硬件输出。

## 默认推荐流程：PC 控制 Native Capture

1. 操作者只在 PC 浏览器打开 Core 的 `GET /teleop.html`，登录后手工生成一次性 Capture 配对。
2. APK 首次安装后，由 PC 通过 ADB 调用 Core 源树 `clients/quest-capture-native/scripts/launch_capture.sh --platform meta|pico`，启动 `native_openxr` 并输入一次性配对信息；后续仍由 PC 显式执行 `launch_capture.sh --platform meta --resume` 或 `launch_capture.sh --platform pico --resume`。`--platform` 是必填项，防止把两个独立 package 的凭据或启动目标混用。
3. Native Activity 在前台且取得 OpenXR `FOCUSED` 输入所有权时可自动进入 OpenXR session。它不是开机自启服务，也不能在 Android 后台持续采集；佩戴者无需打开 WebXR 页面或点击应用菜单。首装仍可能出现 Android/OpenXR 系统权限提示，这一点尚未真机验收。
4. PC 操作者手工 Acquire Shadow 会话，等待 Capture 显示 ready，再手工 Attach。只有 PC 可以 Pause/HOLD 或 Release；页面刷新、断线和重新佩戴都不会自动 Acquire、Attach 或恢复会话。
5. 佩戴者仍需戴好 Quest 或 PICO，并用双手 squeeze 作为动作 deadman；tracking、FOCUSED、WSS 或 RTC 丢失会关闭采集并让 Core fail-close 到 HOLD。

`Direct WebXR` 只保留为操作者显式选择的 fallback，不属于默认流程，也不会与 Native Capture 在同一会话内静默切换。切换 source 前必须先 HOLD/Release，再新建会话。

## MCP 动作

| action | 入参 | 类型 / 范围 / 单位 | 必填 | confirm | 可见结果 |
|---|---|---|---|---|---|
| `start` | 无 | — | — | 否 | 返回 lifecycle readiness，不创建会话。 |
| `prepare_shadow` | `session_id`,`epoch`,`fence` | canonical UUID；integer `>=1`；string 至少 24 字符 | 是 | 否 | 安装 Core 发放的 Shadow authority。 |
| `heartbeat` | `boot_id`,`session_id`,`epoch`,`fence` | UUID、UUID、integer、string；无单位 | 是 | 否 | 唯一可续租入口；RTC heartbeat 不续租。 |
| `pause` | 完整 identity | 同上 | 是 | 否 | 进入 paused 并记录 stop ACK。 |
| `soft_stop` | 完整 identity | 同上 | 是 | 否 | 进入 HOLD，不会由旧帧恢复。 |
| `release` | 完整 identity | 同上 | 是 | 否 | 撤销 authority 并关闭 peer。 |
| `status` | 无 | — | — | 否 | 返回脱敏 session、lease、Pose、RTC、recording 与 counters。 |
| `submit_shadow_frame` | `frame` | Strict Frame v1 object，canonical JSON 最大 64 KiB | 是 | 否 | 低频诊断/回放入口，不是高频 RTC 路径。 |
| `stop` | 无 | — | — | 否 | 停止 lifecycle 并释放 Shadow 会话。 |

成功返回标准 MCP `result.content=[{"type":"text","text":"<JSON snapshot>"}]`，snapshot 不包含 fence。HTTP `401` 表示 Driver Bearer 失配；JSON-RPC `-32601` 表示 method/tool/action 不存在，`-32602` 表示 action 参数、identity、lease 或 Frame 不合法。

RTC control 仅允许只读 `peer_ping` 和 `status`。`heartbeat` 返回 `rtc_cannot_renew_lease`，`pause` / `soft_stop` / `release` 返回 `rtc_control_requires_core`。

## 验收边界

本卡可验收的是：descriptor、客户端 authority 禁止字段、只读 RTC control 和永久零输出 recording 证据。详细命令见 [verification/offline.md](verification/offline.md)。

本卡没有机器人机型/profile/IK 映射，不含硬件模式，也不得用来声明 Meta/PICO→机器人实机可用。具体机器人机型的映射、输出形状和硬件证据必须放在该机型自己的 Card/Driver 中。

## 状态

`offline-green` 仅表示本地协议、recording 边界和两种 Android flavor 的构建/静态检查通过。Meta 与 PICO `arm64-v8a` debug APK 已在 macOS x86_64 主机构建成功；Quest 当前 ADB 为 `unauthorized`，PICO APK 尚未安装或运行，二者都没有本轮头显运行验收。当前 G1 关机且本轮没有任何硬件输出。上述 Native 流程仍是待设备验收的操作合约，不是已完成的真机证据。

## 数据来源

见 [impl/source.md](impl/source.md)。`impl/teleop_session.py` 只是可执行的审阅摘录，不是 Driver 副本。
