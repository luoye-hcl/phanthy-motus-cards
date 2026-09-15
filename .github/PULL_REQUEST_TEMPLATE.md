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

## 网站验证(升 accepted 必填;未达 accepted 请在标题加 `[pending-web]`,审核不予合并)

- preflight 输出(粘关键几行):
  ```
  <python3 tools/preflight.py cards/<robot>/<card> --host <ip> 的输出>
  ```
- 卡可见截图:<链接>
- 功能实现截图(数据流/执行效果):<链接>
- 实机真实样本:见 `verification/accepted.md`
- MT 验收人 / 日期 / 结论:<...>

## 自检清单

- [ ] `preflight.py` 全绿
- [ ] accepted 卡:网站证据 + MT 验收记录齐(见 docs/WEBSITE_VERIFICATION.md)
- [ ] 未达 accepted 已在 PR 标题加 `[pending-web]`
