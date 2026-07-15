# PhanthyMotus 卡片库(Card Library)

PhanthyMotus 机器人**能力卡片**的统一收录仓库。卡片按**统一标准**提交、审核与版本追踪,便于检索、复用与维护。

> 一张"卡片"= 一个通过 MCP over HTTP 暴露给 Agent Core 的能力单元(传感器只读卡 `sensor` 或执行器控制卡 `actuator`),在 core 网页上呈现为一张可交互/可看数据流的卡。

## 仓库结构

```
cards/<机器人>/<卡片名>/         # 每张卡一个完整目录(卡片名 = MCP 工具名)
  ├── CARD.md                    # 卡片规格(人读):能力/接口/字段/来源/状态
  ├── metadata.json              # 卡片元数据(机读):MCP 工具 schema + 目录字段
  ├── CHANGELOG.md               # 该卡的版本变更记录(每次更新必写)
  ├── impl/                      # 实现源码摘录 + source.md(指向真实驱动的 repo/路径/commit)
  └── verification/              # 验收/测试证据(离线测试结果 + 实机真实数据样本)
docs/
  ├── SUBMISSION_STANDARD.md     # 提交标准(一张卡必须满足什么才算合格)
  ├── SUBMISSION_PROCESS.md      # 提交流程(一步步怎么走 PR)
  └── CARD_TEMPLATE/             # 新卡模板:复制到 cards/<机器人>/<卡片名>/ 后逐项填写
.github/PULL_REQUEST_TEMPLATE.md # PR 模板(强制对齐提交标准)
```

## 快速开始(提交一张新卡)

1. 读 [docs/SUBMISSION_STANDARD.md](docs/SUBMISSION_STANDARD.md) 和 [docs/SUBMISSION_PROCESS.md](docs/SUBMISSION_PROCESS.md)。
2. 复制 `docs/CARD_TEMPLATE/` 到 `cards/<机器人>/<卡片名>/`,逐项填。
3. 开分支 → 提 PR(用 PR 模板)→ 审核合并。
4. **每次更新卡片**:`metadata.json` 里 `version` 递增 + `CHANGELOG.md` 加一条 + PR 里写明改了什么。

## 已收录卡片

| 机器人 | 卡片 | 类型 | 控制等级 | 状态 | 作者 |
|---|---|---|---|---|---|
| unitree-go1 | [feet](cards/unitree-go1/feet/) | sensor | ANY | ✅ 已验收 2026-07-14 | luoye-hcl |
| unitree-go1 | [imu](cards/unitree-go1/imu/) | sensor | ANY | ✅ 已验收 2026-07-14 | luoye-hcl |
| unitree-go1 | [loco_state](cards/unitree-go1/loco_state/) | sensor | HIGHLEVEL | ✅ 已验收 2026-07-14 | luoye-hcl |

> 收录一张卡后,请在此表加一行。
> **入库门槛**:只有 `accepted`(网站验证 + MT 验收通过)的卡才合入 main;`offline-green` 卡的 PR 可开着(标 `[pending-web]`)但不合并。见 [docs/WEBSITE_VERIFICATION.md](docs/WEBSITE_VERIFICATION.md)。
