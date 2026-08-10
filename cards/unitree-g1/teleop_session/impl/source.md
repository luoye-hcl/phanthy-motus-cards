# 实现来源

本卡摘录自 `phanthymotus-driver` G1 遥操作 Draft PR [#118](https://github.com/4paradigm/phanthymotus-driver/pull/118)，固定源提交为 `1afb292ef9b4d7a489024f59180268d9d13ce984`。

- 仓库：`4paradigm/phanthymotus-driver`
- 根 Driver：`unitree/g1/main.py:G1DeviceBundle`
- MCP/RTC facade：`unitree/g1/teleop/service.py:G1TeleopService`
- 描述符：`unitree/g1/teleop/descriptor.py:tool_definitions`
- 会话状态机：`unitree/g1/teleop/runtime.py:G1TeleopRuntime`
- final dispatch：`unitree/g1/teleop/dispatch.py:FinalDispatchArbiter`
- G1_23 映射与 IK：`unitree/g1/teleop/adapter.py`、`unitree/g1/teleop/ik.py`
- 唯一硬件出口：`unitree/g1/teleop/hardware.py:G1ArmSdkPort`
- 配置组合：`unitree/g1/teleop/factory.py:build_g1_teleop_service`
- 镜像/说明：`unitree/g1/Dockerfile`、`unitree/g1/TELEOP.md`

服务仍使用现有 root G1 MCP 端口 `15701`。启用遥操作时不会构造或暴露固件 `arm` gesture 工具；同一进程只允许一个 `rt/arm_sdk` publisher。Shadow 使用同一 Pose 映射、IK 与 LowState 比较，但根本不构造 publisher。

Core 只负责身份、RBAC、会话租约、fence、可信 Driver 固定、显式 Live 确认、Capture assignment、信令代理与审计。60 Hz Pose 通过 Meta/PICO Native OpenXR 与 Driver 的 WebRTC DataChannel 直连，不通过 MCP 或 Core 转发。Driver Bearer、一次性 SDP-bound ticket 与固定 Core CA 保护控制面；卡片和摘录均不保存凭据。

Core 的真实用户入口是 PC 上的 `GET /teleop.html`，实现见 Core Draft PR [#84](https://github.com/4paradigm/phanthymotus/pull/84)。卡片的 navigation action 只打开该页面；页面再通过 `/api/teleop/*` 管理目录、一次性 Capture 配对、会话、显式 Live 确认、手工 Attach 与 signaling，不会让 Card 直接调用 Driver/MCP。

默认 Android OpenXR 客户端位于 Core 仓库 `4paradigm/phanthymotus` 的 `agent-core/clients/quest-capture-native`（Core 应用根内路径仍为 `clients/quest-capture-native`，路径名仅为兼容保留）。共享 Khronos OpenXR/C++ 代码以 `meta` / `pico` flavor 分别构建 `com.phanthymotus.questcapture` 与 `com.phanthymotus.picocapture`；PICO flavor 支持运行时公开的 PICO 4 和 PICO 4 Ultra controller profile，没有支持的 PICO controller extension 时 fail-close。两种 flavor 都使用 `native_openxr` client kind，由 PC 通过 `scripts/launch_capture.sh --platform meta|pico` 的 ADB 流程首次启动，后续使用对应的 `--platform ... --resume`；佩戴者不需要在头显内打开 WebXR 页面或操作应用菜单。客户端不持有 operator token、Core session、lease、fence、Acquire 或 Live confirmation，卡片也不保存配对秘密或设备凭据。

Native Activity 只有在 Android 前台且 OpenXR 为 `FOCUSED` 时采集；当前实现没有开机自启或后台 OpenXR 能力。`Direct WebXR` 仍是 Core 页面中的显式 fallback，不能在当前会话中从 Native source 静默切换。

第三方 G1_23 标定、IK/arm lifecycle 与 URDF 来自 Apache-2.0 的 Unitree `xr_teleoperate` focused port；归属说明在 Driver 的 `unitree/g1/teleop/NOTICE.md`。未复制 TeleVuer/Vuer 或图像管线。

当前可复验的是纯 descriptor、HTTP、RTC、状态机、fake LowState/IK/publisher、Core projector、Cards 一致性测试，以及 macOS x86_64 主机上的 Meta/PICO `arm64-v8a` debug APK 构建与静态检查。目标 linux/arm64 G1 镜像上的 Pinocchio/CasADi/IPOPT cold solve 仍未运行；Dockerfile 已把 cold import + solve 设置为构建硬门。Quest 当前 ADB 为 `unauthorized`，PICO APK 尚未安装/运行，G1 当前关机且无硬件输出，因此本卡不能标记 `accepted` 或 `live-ready`。
