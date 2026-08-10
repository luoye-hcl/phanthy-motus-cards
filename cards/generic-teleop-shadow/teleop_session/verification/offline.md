# 离线验证证据

- 日期：2026-08-09
- Driver 源提交：`68f07c4fb367effca19ce46007b0bbafce158fa6`
- 能力摘要：`0deb8aea9802bfd31b9e43df273ed79000ad7de7de9c1e024abd5da80583ae7e`
- 范围：通用 Shadow descriptor、会话/RTC 协议与 recording final-dispatch；不含机型、IK 或硬件输出。

## Driver 回归

在固定源树运行：

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --offline --python 3.14 \
  --with-requirements generic/teleop_shadow/requirements.txt \
  python -m unittest discover -s generic/teleop_shadow/tests -v
```

结果：`108 passed`，`1 skipped`。条件 skip 是当前主机不可用 Docker Compose；本卡不把容器启动表述为已通过。本地 aiortc 测试不是头显真机证据。

本次集成工作树首次并发复跑时，`test_watchdog_revocation_supersedes_pause_while_stop_is_pending`
出现过一次时序失败：测试用真实 `sleep(110ms)` 模拟 `100ms` lease，同时与 `150ms` I/O
deadline 竞争，负载下会正确触发 `adapter_io_stalled`。生产 fail-closed 逻辑未放宽；测试改为共享
`FakeClock` 后，目标用例 `100/100 PASS`，runtime 组 `23/23 PASS`、deadline 组 `7/7 PASS`，
随后全量仍为上述 `108 passed / 1 skipped`。

## Cards 一致性

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  cards/generic-teleop-shadow/teleop_session/verification/test_card_consistency.py -v
```

该命令检查：

- `metadata.json.mcp_tool` 与可执行摘录的 descriptor 完全相等；
- source revision、capability digest、recording protocol 与 signaling 边界一致；
- 浏览器不能注入 authority，RTC 不能续租或修改会话；
- final-dispatch 只产生 `would_apply` / `would_stop`，`hardware_output=false`；
- 参考卡没有具体机型、硬件路径或 Core 修订号绑定。

如果同时有 Driver checkout，可以设置 `PHANTHYMOTUS_DRIVER_ROOT` 让同一测试直接调用真实 `tool_definitions()` 并与卡片 descriptor 比较。
当前带该环境变量的结果为 `Ran 6 tests ... OK`；未提供 checkout 时，producer 比较一项显式 skip，其余 5 项仍可独立运行。

## Native Capture 就绪度快照

当前 Core 工作树包含共享 Android OpenXR 源树 `agent-core/clients/quest-capture-native`（Core 应用根内 `clients/quest-capture-native`）及 `client_kind=native_openxr` 合约。同一份 C++ 代码由 `meta` / `pico` flavor 构建；卡片一致性测试固定默认用户路径为：PC `GET /teleop.html` 生成一次性配对、PC ADB 以 `launch_capture.sh --platform meta|pico` 启动 Native Activity、PC 手工 Acquire/Attach/Pause/HOLD/Release。后续启动分别使用 `launch_capture.sh --platform meta --resume` 或 `launch_capture.sh --platform pico --resume`；文档不要求佩戴者在头显内打开 WebXR 页面或点击应用菜单。`Direct WebXR` 仅为显式 fallback。

在 macOS x86_64 主机使用 Gradle `8.9`、JDK `17`、compileSdk `35`、NDK `27.0.12077973` 与 CMake `3.22.1` 构建并静态检查两个产物：

| flavor | APK / package | bytes | SHA-256 |
|---|---|---:|---|
| Meta | `app/build/outputs/apk/meta/debug/app-meta-debug.apk` / `com.phanthymotus.questcapture` | `2410871` | `2eb14276da161b5945a0984dd2a691a69a3b898ed9ff1000871d9f843ed8a8c0` |
| PICO | `app/build/outputs/apk/pico/debug/app-pico-debug.apk` / `com.phanthymotus.picocapture` | `2411011` | `e6a713af5194cc9e6a9c2538056ada45a726dcb60db248315d63db0b5fdabbac` |

两者均为 versionName `0.2.0` / versionCode `2`、minSdk `29`、targetSdk `35`，仅包含 `arm64-v8a`，使用可验证的 v2 debug 签名，并通过 `zipalign` 与 ELF/依赖检查。只有 PICO manifest 含 `pvr.app.type=vr`；Meta manifest 不含该字段。PICO flavor 只接受 runtime 实际公开且已启用相应 extension 的 PICO 4 `/interaction_profiles/bytedance/pico4_controller` 或 PICO 4 Ultra `/interaction_profiles/bytedance/pico_ultra_controller_bd` profile；两者都没有时 fail-close。这是源码、host test、构建和 APK 静态证据，不是 PICO 真机兼容性声明。

这仍不是设备验收：Quest 当前 ADB 状态为 `unauthorized`，本轮无法取得 Meta APK 的安装/运行证据；PICO APK 尚未安装或运行。Native Activity 也没有开机自启或后台 OpenXR 能力。当前 G1 关机，所有本轮检查均无硬件输出。

## 未验证

- Quest ADB 当前为 `unauthorized`；未取得本轮 Meta APK 安装/运行、首次系统权限提示、OpenXR `FOCUSED` 或真实控制器 tracking 证据。
- PICO APK 尚未安装/运行；未验证 PICO 4 / 4 Ultra 的 OpenXR session、实际 controller profile、双 squeeze、tracking 丢失或 RTC。
- 未连接机器人、DDS 或 vendor SDK；G1 当前关机且无输出。
- `would_apply` 只是 recording 证据，不是物理运动证据。
- 卡片状态仅为 `offline-green`，不表示任何机型已可实机遥操。
