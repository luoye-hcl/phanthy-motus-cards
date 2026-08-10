# Changelog

## v1.0.0 — 2026-08-09 — luoye-hcl

- 首次收录 root Unitree G1_23 双臂 Shadow/Live `teleop_session`。
- 固定来源为 Driver Draft PR #118 的提交 `1afb292ef9b4d7a489024f59180268d9d13ce984`。
- 固化 `unitree-g1` 身份、十关节/禁用 base+hands 能力、两种 capability digest 与显式 Live 二次确认。
- 收录单一 `rt/arm_sdk` publisher、超时重握、fault、零权重停止和分段延迟证据。
- 状态保持 `offline-green`：linux/arm64 cold IK 镜像与本集成路径 Meta/PICO→G1 Live 尚未实证。
- 默认流程改为 PC 控制的共享 Android OpenXR Capture；同一源树输出 Meta/PICO 两个 flavor，启动必须显式传 `--platform meta|pico`，会话仍由 PC 手工 Acquire/Live 二次确认/Attach/Pause/HOLD/Release。
- 头显内无需 WebXR 页面或应用菜单；`Direct WebXR` 仅为显式 fallback，不声明开机自启或后台 OpenXR。
- Meta/PICO `arm64-v8a` debug APK（`0.2.0` / code `2`）均已在 macOS x86_64 主机构建并通过 package、manifest、签名和 zipalign 静态检查；PICO 尚未安装/运行，Quest ADB 为 `unauthorized`，G1 关机且无硬件输出。
