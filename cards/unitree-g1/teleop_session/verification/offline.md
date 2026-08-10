# 离线验证证据（2026-08-09）

本证据不连接 Meta/PICO 头显、G1、DDS 网络或 SSH 目标，不产生硬件输出。

## Driver

- `generic/teleop_shadow`：`108 passed`，`1 skipped`；skip 是本机无 Docker Compose。
- `unitree/g1`：当前全量为 `57 tests ... OK`。测试含真实本地 aiortc 双 DataChannel，但 LowState、IK 与 publisher 为 fake。
- 覆盖 tools/list、Bearer、TLS/trusted registration、Shadow 零 publisher、Live 唯一 publisher、5 个成功零权重帧、mode/LowState fault、timeout neutral→reclutch、Pause/Release 竞态、RTC ticket/replay/binding、进程异常关闭与错误脱敏、Live health/close 竞态及分段延迟。

## 数值运行时与 Ubuntu x86_64 smoke

- 目标运行时改为 `conda-forge` + `nodefaults` 单一来源：Python `3.10`、Pinocchio `3.1.0`、CasADi `3.6.7`、NumPy `1.26.4`。
- 在真实 Ubuntu x86_64 上使用同版本栈执行 G1_23 current-pose IK：warm-up 约 `16.7 ms`；30 帧 solve 的 `p50≈1.9 ms`、`p95≈2.2 ms`、`max≈2.18 ms`。
- 末端平移误差最大约 `1.5 mm`；smoke 保持 `publisher_created=false`，未构造 `rt/arm_sdk` publisher，不产生硬件输出。

这项证据证明的是 Ubuntu x86_64 同源数值栈可导入、可 warm-up 并连续 solve；它不是 Docker 目标镜像构建、linux/arm64 证据或 Quest→G1 Live 验收。

## Core

- Core Draft PR [#84](https://github.com/4paradigm/phanthymotus/pull/84) 的 `tests/teleop`：`688 passed`。
- Electron-as-Node `test_webxr_frame.mjs`：all tests passed。
- heartbeat 终态 fault snapshot、Live 两步确认/取消竞态、authority guard、joint shape、mode-specific sequence/weight、UI 无自动确认/重连均有确定性测试。

## Native Capture 就绪度快照

Core Draft PR [#84](https://github.com/4paradigm/phanthymotus/pull/84) 包含共享 Android OpenXR 源树 `agent-core/clients/quest-capture-native`（Core 应用根内 `clients/quest-capture-native`）和 `client_kind=native_openxr` 合约。同一份 C++ 代码由 `meta` / `pico` flavor 构建；默认用户路径固定为 PC `GET /teleop.html` 生成一次性配对、PC ADB 以 `launch_capture.sh --platform meta|pico` 启动 Native Activity、PC 手工 Acquire、Live 二次确认、Attach、Pause/HOLD 与 Release。后续启动分别使用 `launch_capture.sh --platform meta --resume` 或 `launch_capture.sh --platform pico --resume`。文档不要求佩戴者在头显内打开 WebXR 页面或点击应用菜单；`Direct WebXR` 只保留为显式 fallback。

在 macOS x86_64 主机使用 Gradle `8.9`、JDK `17`、compileSdk `35`、NDK `27.0.12077973` 与 CMake `3.22.1` 构建并静态检查两个产物：

| flavor | APK / package | bytes | SHA-256 |
|---|---|---:|---|
| Meta | `app/build/outputs/apk/meta/debug/app-meta-debug.apk` / `com.phanthymotus.questcapture` | `2410871` | `2eb14276da161b5945a0984dd2a691a69a3b898ed9ff1000871d9f843ed8a8c0` |
| PICO | `app/build/outputs/apk/pico/debug/app-pico-debug.apk` / `com.phanthymotus.picocapture` | `2411011` | `e6a713af5194cc9e6a9c2538056ada45a726dcb60db248315d63db0b5fdabbac` |

两者均为 versionName `0.2.0` / versionCode `2`、minSdk `29`、targetSdk `35`，仅包含 `arm64-v8a`，使用可验证的 v2 debug 签名，并通过 `zipalign` 与 ELF/依赖检查。只有 PICO manifest 含 `pvr.app.type=vr`；Meta manifest 不含该字段。PICO flavor 只接受 runtime 实际公开且已启用相应 extension 的 PICO 4 `/interaction_profiles/bytedance/pico4_controller` 或 PICO 4 Ultra `/interaction_profiles/bytedance/pico_ultra_controller_bd` profile；两者都没有时 fail-close。这是源码、host test、构建和 APK 静态证据，不是 PICO 真机兼容性声明。

这仍不是 Meta/PICO→G1 实机验收：Quest 当前 ADB 状态为 `unauthorized`，本轮无法取得 Meta APK 的安装/运行证据；PICO APK 尚未安装或运行。Native Activity 也没有开机自启或后台 OpenXR 能力。当前 G1 关机，本轮没有 DDS/device 连接或硬件输出。

## 跨仓矩阵

真实 G1 descriptor 与 fake runtime 状态交给当前 Core strict projector：

- Shadow：descriptor + idle/prepared/active/hold/paused/released/failing-IK fault 全部 PASS。
- Live：descriptor + idle/prepared/active/hold/paused/released/async hardware fault/intent-expired HOLD 全部 PASS。
- 每个 authority/停止状态均为 target/measured 10/10；Shadow weight `null` 且只有 would-apply sequence，Live weight 为数值且只有 published sequence；fault code 与 output reason 一致。

## 尚未取得的证据

- 尚未构建目标 linux/arm64 G1 Docker 镜像，因此该目标架构的 cold import/current-pose solve 构建硬门仍未实证。
- Quest ADB 当前为 `unauthorized`；未取得本轮 Meta APK 安装/运行或 Native Capture 的系统权限、OpenXR `FOCUSED`、控制器 tracking、RTC 证据。
- PICO APK 尚未安装/运行；未验证 PICO 4 / 4 Ultra 的 OpenXR session、实际 controller profile、双 squeeze、tracking 丢失或 RTC。
- 未将本次 root G1 Driver 集成路径部署到机器人；G1 当前关机，也未运行 Meta/PICO→G1 Live。

Dockerfile 已把 cold import + solve 设为构建硬门。取得目标构建与实机 stop/latency 证据前，本卡只能是 `offline-green`，不能标记 `accepted` 或 `live-ready`。

卡片自检命令：

```bash
python3 -m unittest \
  cards/unitree-g1/teleop_session/verification/test_card_consistency.py -v
```

默认结果：`Ran 9 tests ... OK (skipped=1)`。另将本卡 Shadow/Live descriptor 与 Driver
`unitree/g1/teleop/descriptor.py` 逐字段比较，两种模式及其 digest 均 PASS。设置
`PHANTHYMOTUS_DRIVER_G1_ROOT` 时结果为 `Ran 9 tests ... OK`；未设置时真实 producer
比较一项会显式 skip，其余 8 项仍可独立运行。

## 可执行跨仓消费者矩阵

设置两个 checkout 根路径后，在 Cards 仓库根目录运行：

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="$PHANTHYMOTUS_CORE_ROOT/src" \
"$PHANTHYMOTUS_CORE_ROOT/.venv/bin/python" \
  cards/unitree-g1/teleop_session/verification/cross_repo_contract.py \
  --driver-root "$PHANTHYMOTUS_DRIVER_G1_ROOT" \
  --core-root "$PHANTHYMOTUS_CORE_ROOT"
```

当前结果：

```json
{"console_action":"GET /teleop.html","descriptors":2,"hardware":"fake-only; no DDS/device connection","joint_shape":"10/10","latency_stages":["adapter_apply","ik","mailbox_wait","receive_to_admit","robot_follow"],"projected_statuses":15,"result":"PASS"}
```

这不是静态 fixture：脚本调用当前 Driver descriptor，用 fake LowState/IK/publisher 生成 Shadow 7 个和 Live 8 个状态，再逐个交给当前 Core strict projector。脚本同时检查 10/10 关节形状、mode-specific sequence/weight、fault 一致性、transport/分段延迟字段，以及 Core 实际 `/teleop.html` 入口。它不导入 DDS，不连接设备。
