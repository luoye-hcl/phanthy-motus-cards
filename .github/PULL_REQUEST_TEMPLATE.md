<!-- 标题格式:[<机器人>] add|update <卡片名> [vX.Y.Z]: <一句话> -->

## 本次提交

- 机器人 / 卡片:`<机器人>` / `<卡片名>`
- 动作:`[ ] 新增`  `[ ] 更新(vX.Y.Z)`
- 一句话说明:

## 改了什么(更新卡必填)

<!-- 改了哪些字段/动作/行为/证据,为什么,影响面 -->

## 提交标准自检(对照 docs/SUBMISSION_STANDARD.md)

- [ ] 目录 = `cards/<机器人>/<卡片名>/`,卡片名 = MCP 工具名 snake_case
- [ ] `CARD.md` 六节齐全(能力/基本信息/接口/字段/来源/状态)
- [ ] `metadata.json` 合法 JSON(`python3 -m json.tool` 通过),顶层必填字段齐,`mcp_tool.name` == 目录名
- [ ] `impl/` 有源码摘录 + `source.md`,**无口令/密钥**
- [ ] `verification/` 有离线证据;accepted 卡有实机真实数据样本
- [ ] `CHANGELOG.md` 有本次版本条目,`version` 已递增
- [ ] 已更新 README 收录表(新增卡)
- [ ] 无明文口令/密钥/无关大文件
