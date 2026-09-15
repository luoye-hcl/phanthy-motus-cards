# 网站验证方案(WEBSITE VERIFICATION)

一张卡要升到 `accepted`(唯一能合入 main 的状态),必须在**公司 core 网站**上被证明"功能真的实现了",并经 **MT 验收通过**。本文是通用、可自测的验证流程。

> 本文从"**卡已注册进 core、网站能打开**"开始。环境怎么拉起(部署驱动 / 让路 / 转发器 `--ipc=host` / 断网恢复)**不在本文范围**——见你所在驱动仓库的部署文档(如 Go1:`luoye-hcl/go1-driver`)。
>
> ⚠️ 不依赖网站"智能控制"大模型链路(该链路目前因 core 侧 `decision_core` 问题不可用)。验证一律走**手动点执行 / 看数据流**。

## §0 前提清单(逐项确认)

- [ ] 机器人上电、可连
- [ ] 驱动已部署并**注册进 core**(设备在网站上可见)
- [ ] 数据转发器已在跑(如 Go1 的 ROS republisher,**带 `--ipc=host`**)——DATA STREAMS 出数据的前提
- [ ] core 网站能打开(如 `https://<core-ip>:15678`)

任一不满足,先回驱动仓库解决,别急着往下。

## §1 自动前置检查(机器先判)

跑前置脚本,把"机器能判"的先跑绿,再上网站费人力:

```
python3 tools/preflight.py <卡目录> --host <驱动IP> [--port 15704]
```

例:`python3 tools/preflight.py cards/unitree-go1/net --host 10.100.130.4`

- 全绿(`exit 0`)→ 卡已注册、MCP 契约与 `metadata.json` 一致、传感器卡 `read` 返真数据 → 进 §2。
- 有 `FAIL` → 先修(卡没注册/契约不符/连不上驱动)。
- `WARN`(如后端离线、`offline:true`、`NO_FEEDBACK`)→ 说明驱动没接真机,先接真机再验。

> preflight **不能**替代下面的网站步骤——可见性 / 数据流 / 执行效果 / MT 验收,机器判不了,必须人上网站。

## §2 网站"看得到"

打开 core 网站 → 在设备下找到这张卡。确认:名称、描述、类型(sensor/actuator)、控制等级(ANY/HIGHLEVEL/LOWLEVEL)与 `metadata.json` **一致**。截图留证(卡可见)。

## §3 网站"验功能"(分卡型)

**传感器卡(sensor)**
- 在 DATA STREAMS(数据流)面板找到该卡的 topic,确认**数据在跳动**。
- **制造一个真实变化**证明不是伪造:如动一下狗看 IMU/里程值随之变、遮挡/触碰改变读数。
- 截图留证(数据流 + 变化前后)。

**执行器卡(actuator)**
- ⚠️ 安全前置:场地空旷、狗已站稳、随时能发急停 `damp`;让狗动前口头提醒在场的人。
- 在网站上点该卡的"**执行**"按钮发一个动作 → 观察机器人产生**对应真实效果**(或配套状态卡的值随之变化)。
- 截图/录屏留证(执行 + 真实效果)。

## §4 留证

收集:①卡可见截图 ②功能实现截图(数据流 / 执行效果)③一段**真实返回 JSON**(传感器最好两态对比)④采集时间 / 环境 / 后端。

> 截图等二进制**不入库**(仓库禁无关大文件)。用链接(内网图床)或贴在 PR 里,`verification/accepted.md` 正文只留指针。

## §5 MT 验收

请 MT 在网站上确认该卡功能实现 → 记录**验收人 / 日期 / 结论**。这是升 `accepted` 的必要一步。

## §6 通过后

- 把上面证据按 `docs/CARD_TEMPLATE/verification/accepted.md` 模板写入卡的 `verification/accepted.md`。
- `metadata.json`:`status` 改 `accepted`、加 `accepted_date`、`version` 递增。
- `CHANGELOG.md` 加一条。
- 提 PR 请求合并(见 `SUBMISSION_PROCESS.md`)。未达 accepted 的卡,PR 标题加 `[pending-web]`,审核不予合并。
