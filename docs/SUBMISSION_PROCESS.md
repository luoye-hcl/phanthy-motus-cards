# 提交流程(SUBMISSION PROCESS)

本库用 **PR + 审核**。提交或更新卡片,统一走下面的流程。

## 前置(一次性)

- 克隆仓库:`git clone https://github.com/luoye-hcl/phanthy-motus-cards.git`。
  - 有写权限:直接开分支提 PR(见下)。
  - 无写权限:先 Fork 到自己名下,再从 Fork 提 PR。
- 读 [SUBMISSION_STANDARD.md](SUBMISSION_STANDARD.md)。

## A. 新增一张卡

1. **开分支**(从最新 main):
   ```
   git checkout main && git pull
   git checkout -b add/<机器人>-<卡片名>        # 例:add/unitree-go1-battery
   ```
2. **复制模板**并填写:
   ```
   cp -r docs/CARD_TEMPLATE cards/<机器人>/<卡片名>
   ```
   逐项填 `CARD.md` / `metadata.json` / `impl/` / `verification/`,`CHANGELOG.md` 写 `1.0.0` 首条。
3. **本地自检**:
   - `python3 -m json.tool cards/<机器人>/<卡片名>/metadata.json`(校验 JSON 合法)。
   - 对照提交标准自检清单逐项过一遍。
   - 确认没有明文口令/密钥。
4. **提交 + 推分支**:
   ```
   git add cards/<机器人>/<卡片名>
   git commit -m "[<机器人>] add <卡片名>: <一句话>"
   git push -u origin add/<机器人>-<卡片名>
   ```
5. **开 PR**(用 PR 模板),标题 `[<机器人>] add <卡片名>: <一句话>`。
6. **更新 README 收录表**(加一行)——可在同 PR 里改。
7. 审核人对照提交标准检查 → 通过后合并到 main。

## B. 更新一张已有卡(**每次更新必写明**)

1. 开分支 `update/<机器人>-<卡片名>`。
2. 改对应文件。
3. **必做三件事**(缺一不可):
   - `metadata.json` 的 `version` 按语义化递增(修字段/加动作=次版本,改行为/破坏兼容=主版本,修文档/证据=修订号)。
   - `CHANGELOG.md` 顶部加一条:`## vX.Y.Z — YYYY-MM-DD — 作者` + 改动点。
   - 若行为/字段变了,同步更新 `CARD.md` 与 `verification/` 证据。
4. 提交信息:`[<机器人>] update <卡片名> vX.Y.Z: <一句话>`;开 PR;PR 描述里写清**改了什么、为什么、影响面**。

## C. 审核人检查(Reviewer)

- 逐条对 [SUBMISSION_STANDARD.md](SUBMISSION_STANDARD.md) 的自检清单。
- 重点:`metadata.json` 合法且 `mcp_tool.name`==目录名;有验收/测试证据;版本+CHANGELOG 已更新;**无口令/密钥**。
- 通过 → Squash 合并到 main;不合格 → 评论打回。

## 分支/提交命名约定

| 动作 | 分支 | 提交信息前缀 |
|---|---|---|
| 新增卡 | `add/<机器人>-<卡片名>` | `[<机器人>] add <卡片名>: …` |
| 更新卡 | `update/<机器人>-<卡片名>` | `[<机器人>] update <卡片名> vX.Y.Z: …` |
| 改文档/标准 | `docs/<主题>` | `docs: …` |
