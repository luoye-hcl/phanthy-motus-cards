# teleop_session —— Meta/PICO OpenXR 驱动的 Unitree G1_23 双臂遥操作

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `unitree-g1`（G1_23，塑胶假手；V1 不控制手） |
| MCP 工具 | `teleop_session` |
| 类型 / 控制等级 | `actuator` / `LOWLEVEL` |
| profile | `unitree_g1_23_dual_arm_controller_v1` |
| 作者 | `luoye-hcl` |
| 状态 | `offline-green`（2026-08-09；尚非 `accepted` / `live-ready`） |

这是一张真实 root G1 Driver 的垂直卡：共享 Android Native OpenXR 客户端分别构建 Meta/PICO flavor，头部、左右控制器 Pose 经 WebRTC 直达同一 Driver，映射为 G1_23 十个手臂关节目标。`base=false`、`hands=false`；塑胶假手不需要额外 hand Driver。Card 本身不保存 fence、不发 60 Hz 帧，也不调用 Unitree SDK。

## 打开真实控制台

运行 Agent Core 后，只在 PC 浏览器的同一 origin 打开 `GET /teleop.html`（Core 主页也有此链接）。使用 operator 或 owner 登录，在目录中选择 `driver_id=robot_id=unitree-g1`，再选 Shadow 或 Live Acquire。`metadata.json.operator_actions[0]` 就是这个 navigation action；它只进入 Core 控制台，不直接调用 Driver/MCP，也不会自动 Acquire。

## 默认推荐流程：PC 控制 Native Capture

1. PC 操作者在 `/teleop.html` 手工生成一次性 Capture 配对。首次 APK 安装后，由 PC 通过 ADB 调用 Core 源树 `clients/quest-capture-native/scripts/launch_capture.sh --platform meta|pico`，启动 `client_kind=native_openxr`；后续使用仍由 PC 显式执行 `launch_capture.sh --platform meta --resume` 或 `launch_capture.sh --platform pico --resume`。`--platform` 是必填项，分别选择 `com.phanthymotus.questcapture` 与 `com.phanthymotus.picocapture`。
2. Native Activity 必须保持 Android 前台并取得 OpenXR `FOCUSED` 输入所有权。它可以在 runtime 进入 `READY` 时自动开始 session，但不是开机自启服务，也不能在后台持续采集。佩戴者无需在头显内打开 WebXR 页面或点击应用菜单；首装仍可能出现尚未真机验收的 Android/OpenXR 系统权限提示。
3. PC 手工 Acquire Shadow 或 Live。Live 的第一次 Acquire 仍停在 `awaiting_confirmation`；必须由 PC 再次明确确认，Driver 才会 prepare。Capture 显示 ready 且会话为当前 PC 标签页拥有的 Active session 后，PC 再手工 Attach。
4. 佩戴者戴好 Quest 或 PICO 并使用双手 squeeze deadman 控制动作。PC 负责 Pause/HOLD 和 Release；刷新、WSS/RTC/FOCUSED/tracking 丢失或重新佩戴都不会自动确认、自动重新 Acquire、自动 Attach 或自动恢复，丢失路径会 fail-close 到 HOLD。

`Direct WebXR` 只作为操作者显式选择的 fallback，不属于上述推荐流程。Native Capture 与 Direct source 在一个会话中互斥且不会静默切换；切换前必须先 HOLD/Release，再新建会话。

## 可见模式

`metadata.json.mcp_tool` 是可直接复验的 Shadow 配置真实 descriptor。相同工具在显式 Live 配置下只改变 mode-specific 合约：

| 模式 | prepare | protocol / dispatch | hardware | digest |
|---|---|---|---|---|
| Shadow | `prepare_shadow` | `motus.teleop.shadow.v1` / `motus.teleop.dispatch.recording.v1` | 永远 false；只有 would-apply | `3a333966ddb1c146c3852e02e90b59825e6844d6fbd9937502741af3b96a0757` |
| Live | `prepare_live` | `motus.teleop.live.v1` / `motus.teleop.dispatch.hardware.v1` | true；唯一 `rt/arm_sdk` publisher | `016f7e83955ec2dd47333b5ae2c33c85c695b43d2d1cc93b4bbdcc4055bfda4c` |

Live 不是把 Shadow 开关直接改成 true。Core 的第一次 Acquire 只进入 `awaiting_confirmation`，不联系 Driver、不建持久 guard；操作者必须再次提交精确确认体 `{"confirm_live_actuation":true,"profile_id":"unitree_g1_23_dual_arm_controller_v1"}`。确认后才依次固定 Driver、写 authority guard、调用 `prepare_live` 并开始 Core heartbeat。页面不会自动确认、自动重连或自动重新 Acquire。

## MCP 接口

Driver MCP/offer 端点只接受精确 Driver Bearer。参数 schema 为 `additionalProperties=false`。

| action | 入参 | 类型 / 范围 | 必填 | confirm | 行为 |
|---|---|---|---|---|---|
| `stop` | — | — | — | 否 | lifecycle 安全释放并关闭 RTC。 |
| `prepare_shadow` / `prepare_live` | `session_id`,`epoch`,`fence` | canonical UUID；integer `>=1`；URL-safe 24–128 字符 | 是 | Live 需先在 Core 二次确认 | final-output safe-stop ack 后安装新 authority。部署时只声明其中一个 prepare。 |
| `heartbeat` | `boot_id`,`session_id`,`epoch`,`fence` | 完整精确 identity | 是 | 否 | 唯一续租入口；RTC heartbeat 无权续租。 |
| `pause` | 完整 identity | 同上 | 是 | 否 | 进入 `paused`，等待零权重停止证据并关闭 RTC。 |
| `soft_stop` | 完整 identity | 同上 | 是 | 否 | 进入 HOLD；不能靠旧帧恢复。 |
| `release` | 完整 identity | 同上 | 是 | 否 | 撤销 authority，确认安全输出并关闭 RTC。 |
| `status` | — | — | — | 否 | 返回脱敏会话、十关节输出、RTC、故障与延迟。 |

成功返回是标准 MCP text content，其中 JSON 快照不包含 fence。稳定协议错误在 JSON-RPC `error.data.code` 中返回；身份/租约常见值包括 `boot_mismatch`、`session_mismatch`、`epoch_mismatch`、`fence_mismatch`、`session_expired` 与 `session_inactive`。HTTP `401` 表示 Driver Bearer 不匹配。

## 状态与延迟字段

Core 控制台显示 descriptor 的 mode/profile/effectors，并严格投影 Driver 状态：

- 连接：`rtc.connected` 以及 `teleop-control` / `teleop-pose` channel open/closed；页面不会把断开显示为正常。
- 会话：`state`、`reason`、`authority_valid`、`lease.fresh`、`pose.fresh`；`hold` 会保留具体 reason，需操作员按页面提示 neutral→重握，不会自动恢复。
- `output.target_joint_positions_rad` 和 `output.measured_joint_positions_rad` 始终为 10 维；误差以 `output.max_abs_error_rad` 标量显示。Shadow 的 `arm_sdk_weight=null`，Live 为有限 `[0,1]`，fault 时必须为 `0`。
- Shadow 只报告 `last_would_apply_sequence`；Live 只报告 `last_published_sequence`，不会把“已发布”伪装成“机器人已执行”。
- transport：`rtc_rtt_ms`、`pose_age_ms`、`frame_rate_hz`、received/rejected、sequence gaps、mailbox replacements。
- 同一时钟的分段延迟：`receive_to_admit`、`mailbox_wait`、`ik`、`adapter_apply`、`robot_follow`，每段显示 last/p50/p95/p99/count。
- `fault / dispatch_fault` 会以 `dispatch.fault_code` 与 `output.fault_reason` 一致的 snapshot 显示，不会伪装成 released。

这些指标用来区分网络/帧龄、排队、IK、发布与机器人跟随延迟。V1 关节速度上限固定为 `0.5 rad/s`，它本身可能造成明显跟随滞后；不能为了“看起来更快”在现场绕过 profile 修改。

## Driver 与安全边界

- 默认 `unitree/g1/config.yaml` 保持 `teleop.enabled=false`、旧 `arm` gesture 可用；Shadow 示例显式设为 teleop true、arm false。
- teleop 与 `plugins.arm.enabled=true` 冲突会在任何 IK/LowState/publisher 构造前失败。启用后不构造 `G1ArmActionClient`，也不应同时运行 `xr_teleoperate`。
- Live 还需 `teleop.mode=live` 与 `teleop.live.enabled=true` 双开关、fresh 35-motor LowState、`mode_machine=4`、真实 current-pose IK warm-up成功；publisher 只在这些检查后构造。
- release/timeout 需实际成功写出 5 个零权重帧才确认；mode change、stale/missing LowState 或异步发布错误锁存 fault。command timeout/intent expiry 进入 HOLD，必须先 neutral 再用更大的 clutch sequence 重握。
- Native Capture 控制器帧不能携带 `boot_id/session_id/epoch/fence`；authority 由一次性、SDP-bound ticket 在 Driver 端注入。60 Hz 热路径是 Meta/PICO Native OpenXR ↔ Driver DataChannel，Core 只处理控制面、Capture assignment 和信令。

## 部署与验收

1. 先用 `config.teleop-shadow.example.yaml` 部署同一个 root G1 Driver；确认注册身份 `driver_id == robot_id == unitree-g1`、Core 目录 ready、PC 手工 Shadow Acquire/Native Capture Attach/RTC 与十关节 would-apply 可见。
2. 通过 Driver、Core 和本卡离线测试及跨仓全状态矩阵。
3. 必须在目标 linux/arm64 镜像执行 Dockerfile 的 Pinocchio/CasADi/IPOPT cold import + current-pose solve 硬门；本地 x86_64 无 Docker，当前尚无这项证据。
4. Live 实机前停止旧 `xr_teleoperate`，确认只有 root G1 Driver、`mode_machine=4` 与唯一 publisher；再由 PC 页面人工 Acquire、二次确认 Live、手工 Attach Native Capture，并由 PC 管理 Pause/HOLD/Release。
5. 实测并留存 tracking/deadman/RTC/lease 丢失后的 HOLD/零权重证据，以及延迟 p50/p95。完成这些才可把本卡升级为 `accepted`。

Meta/PICO `arm64-v8a` debug APK（`0.2.0` / code `2`）均已在 macOS x86_64 主机构建并通过静态检查；Quest 当前 ADB 为 `unauthorized`，PICO 尚未安装或运行，二者均未完成本轮头显运行验收。当前 G1 关机。本轮没有部署、连接或控制机器人，没有任何硬件输出。此前成功的 Quest→G1 原型实测属于另一条 `xr_teleoperate` 路径，不能冒充本集成 Driver 的验收结果。

## 数据来源 / 实现位置

详见 [impl/source.md](impl/source.md)。核心实现位于 `4paradigm/phanthymotus-driver` 的 `unitree/g1/main.py` 与 `unitree/g1/teleop/`；Card 摘录只用于审阅与一致性测试，不是可运行 Driver。
