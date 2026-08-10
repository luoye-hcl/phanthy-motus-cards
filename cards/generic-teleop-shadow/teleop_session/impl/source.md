# 实现来源

- 仓库：`4paradigm/phanthymotus-driver`，Draft PR [#117](https://github.com/4paradigm/phanthymotus-driver/pull/117)
- 固定提交：`68f07c4fb367effca19ce46007b0bbafce158fa6`
- descriptor 与 MCP facade：`generic/teleop_shadow/main.py:tool_definitions`、`ShadowDriverService`
- Frame/ticket 协议：`generic/teleop_shadow/protocol.py`
- 会话状态机：`generic/teleop_shadow/runtime.py:ShadowRuntime`
- WebRTC：`generic/teleop_shadow/rtc.py:RtcManager`
- 最终 recording 边界：`generic/teleop_shadow/dispatch.py:FinalDispatchArbiter`、`RecordingAdapter`
- 依赖：`aiohttp`、`aiortc`、`cryptography`、`PyYAML`
- 镜像 / 端口：`generic/teleop_shadow/Dockerfile`、`teleop-shadow`、loopback `15711`

`metadata.json.mcp_tool` 是该提交 `tool_definitions()` 的默认第一个工具：`driver_id=teleop-shadow-driver`、`robot_id=null`、开启 authenticated Core proxy signaling。部署时可以为实例设置稳定 `robot_id`，但这张参考卡不预设任何物理机器人。

`ShadowRuntime` 只把严格验证后的意图交给 `RecordingAdapter`，公开状态使用 `kind=recording`、`hardware_output=false`、`would_apply` / `would_stop` 作为证据。源路径不实现机型映射、IK、DDS publisher 或其他执行器。

真实服务从 `config.yaml` 读取身份与注册配置，默认在 `127.0.0.1:15711` 提供 `/mcp`、`/offer` 和 health，并向 Agent Core 注册 descriptor。注册与 signaling 使用部署时注入的 Bearer/ticket secret；Card 不保存任何凭据。

Card 中的纯 Python 摘录仅保留精确 descriptor 与三个可测边界：浏览器 authority 不可覆盖、RTC control 不能续租/改状态、recording 永久零硬件输出。错误处理、并发和完整验证以固定 Driver 提交为准。

推荐的 Android OpenXR 采集消费者位于 Core 仓库 `4paradigm/phanthymotus` 的 `agent-core/clients/quest-capture-native`（Core 应用根内路径仍为 `clients/quest-capture-native`，路径名仅为兼容保留）。共享 Khronos OpenXR/C++ 代码以 `meta` / `pico` flavor 分别构建 `com.phanthymotus.questcapture` 与 `com.phanthymotus.picocapture`；PICO flavor 支持运行时公开的 PICO 4 和 PICO 4 Ultra controller profile，没有支持的 PICO controller extension 时 fail-close。两种 flavor 都使用 `native_openxr` client kind；PC 通过 `scripts/launch_capture.sh --platform meta|pico` 的 ADB 启动流程完成首次配对，后续使用对应的 `--platform ... --resume`。该客户端不持有 Core session、lease、fence、operator token、Acquire 或 Live confirmation，也不把任何配对秘密或设备凭据保存到本卡。

Native Activity 只有在 Android 前台且 OpenXR 为 `FOCUSED` 时采集；当前实现没有开机自启或后台 OpenXR 能力。`Direct WebXR` 仍是 Core 页面中的显式 fallback，而不是 Native 路径的隐式降级。

此 Native 客户端包含在 Core Draft PR [#84](https://github.com/4paradigm/phanthymotus/pull/84)。Meta/PICO 两个 `arm64-v8a` debug APK 已在 macOS x86_64 主机构建并完成静态检查，但 PICO 尚未安装或运行，Quest 当前 ADB 为 `unauthorized`，因此这里没有头显真机验收。当前 G1 关机；这里没有部署 Driver、连接机器人或产生硬件输出。
