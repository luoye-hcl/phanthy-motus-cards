# 提交标准(SUBMISSION STANDARD)

一张卡片要合并进本库,**必须**满足下面全部要求。审核人对照此清单逐条检查;缺项一律打回。

## 1. 目录与命名

- 卡片放在 `cards/<机器人>/<卡片名>/`。
  - `<机器人>` = `厂商-型号`,小写连字符,如 `unitree-go1`、`unitree-go2`。
  - `<卡片名>` = **MCP 工具名**,小写 snake_case,与 `metadata.json.mcp_tool.name` **完全一致**,如 `feet`、`loco_state`。
- 目录内必须有:`CARD.md`、`metadata.json`、`CHANGELOG.md`、`impl/`、`verification/`。

## 2. `CARD.md`(人读规格)必须包含

- **标题 + 一句话能力**。
- **基本信息**:机器人、作者、类型(`sensor`/`actuator`)、控制等级(`ANY`/`HIGHLEVEL`/`LOWLEVEL`)、状态。
- **接口**:
  - 传感器卡:输出 topic + format;`read` 动作;字段表(字段名 + 含义 + 单位)。
  - 执行器卡:每个 action 名 + 入参(名/类型/范围/单位/是否必填)+ 返回包络 + 错误码 + 是否需 `confirm`。
- **数据来源/实现位置**:源仓库 + 文件路径 + 类名 + 依赖(与 `impl/source.md` 一致)。
- **状态**:`draft`(仅设计)/ `offline-green`(离线测试通过)/ `accepted`(实机验收通过,注明日期)。

## 3. `metadata.json`(机读)必须包含且字段合法

必填顶层字段:`card`、`robot`、`author`、`category`(sensor|actuator)、`control_level`、`version`(语义化,如 `1.0.0`)、`status`、`mcp_tool`、`source`。

- `mcp_tool` = 该卡在 `tools/list` 里的**真实**工具描述符(`name`/`type`/`description`/`inputSchema`;传感器卡带 `readOnly:true` + `topic_out`;执行器卡带 `inputSchema.properties` 描述 action/入参)。
- `mcp_tool.name` == 目录名。
- `source` = `{repo, path, class, commit?}`,指向真实实现。
- 传感器卡另填 `topic`(相对路径)、`rate_hz`、`payload_fields`(字段 → 说明/单位)。

`metadata.json` 必须是**合法 JSON**(提交前用 `python3 -m json.tool` 校验)。

## 4. `impl/`(实现)必须包含

- 卡片**核心实现源码摘录**(能看懂这张卡怎么算出返回值;不要求可独立运行)。
- `source.md`:说明它在真实驱动里的位置(repo/路径/类)、依赖的公共层、如何注册、驱动镜像/端口。**严禁**把明文口令、私钥、内部密钥拷进来。

## 5. `verification/`(证据)必须包含

- **离线**:测试通过证据(测试文件名 + 结果摘要,如 `test_mt_cards.py ... OK`)。
- **实机(若 status=accepted)**:一段**真实返回数据样本**(JSON)+ 采集时间/环境;`accepted.md` 注明验收人/日期/页面呈现是否正常。

## 6. `CHANGELOG.md`

- 倒序;每条:`## vX.Y.Z — YYYY-MM-DD — 作者`,下面列改动点。**首次收录**也要有 `1.0.0` 一条。

## 7. 卫生(硬性)

- **无明文口令/密钥/内网私密地址**(如 SSH 口令、Wi-Fi 密码)。
- 无与本卡无关的大文件/二进制。
- 中文或英文皆可,但同一张卡内保持一致。

## 提交标准自检清单(PR 里逐项打勾)

- [ ] 目录 = `cards/<机器人>/<卡片名>/`,卡片名 = MCP 工具名 snake_case
- [ ] `CARD.md` 六节齐全(能力/基本信息/接口/字段/来源/状态)
- [ ] `metadata.json` 合法 JSON,顶层必填字段齐,`mcp_tool.name` == 目录名
- [ ] `impl/` 有源码摘录 + `source.md`,无口令/密钥
- [ ] `verification/` 有离线证据;accepted 卡有实机真实数据样本
- [ ] `CHANGELOG.md` 有本次版本条目,`version` 已递增
- [ ] 无明文口令/密钥/无关大文件
