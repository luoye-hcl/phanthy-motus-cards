# Changelog

## v1.0.0 — 2026-08-09 — luoye-hcl

- 首次收录 recording-only Shadow 参考卡，固定源提交 `68f07c4fb367effca19ce46007b0bbafce158fa6`。
- 收录精确 descriptor、WebRTC authority 边界与 `would_apply` / `would_stop` 零执行证据。
- 不绑定具体机型、硬件路径或 Core 修订；状态为 `offline-green`。
- 默认流程改为 PC 控制的共享 Android OpenXR Capture；同一源树输出 Meta/PICO 两个 flavor，启动必须显式传 `--platform meta|pico`，会话仍由 PC 手工 Acquire/Attach/Pause/HOLD/Release。
- 头显内无需 WebXR 页面或应用菜单；`Direct WebXR` 仅为显式 fallback，不声明开机自启或后台 OpenXR。
- Meta/PICO `arm64-v8a` debug APK（`0.2.0` / code `2`）均已在 macOS x86_64 主机构建并通过 package、manifest、签名和 zipalign 静态检查；PICO 尚未安装/运行，Quest ADB 为 `unauthorized`，G1 关机且无硬件输出。
