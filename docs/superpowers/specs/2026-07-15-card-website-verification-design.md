# 卡片库网站验证方案 + 入库门槛收紧 — 设计文档

- 日期:2026-07-15
- 仓库:`phanthy-motus-cards`(卡片库)
- 状态:设计已对齐,待写实现计划

## 1. 背景与目标

卡片库目前靠"离线测试 + 实机只读 + 人工判断"收录卡片,门槛不统一,`accepted` 到底要满足什么没有强制流程。

**目标**:给提交者一套**通用的、可自测的**验证方案,让其在**公司 core 网站上**证明卡片功能真的实现;并把入库门槛收紧为——**只有"网站上看得到功能实现 + MT 验收通过"的卡才能合并进卡片库 main**。

**非目标(YAGNI)**:
- 不写环境拉起(部署驱动/让路/转发器/断网恢复)——那是各驱动仓库的事,本方案只从"卡已注册进 core、网站能打开"开始。
- 不做多机器人验证附录拆分(现在只有 Go1),等真有第二种机器人再拆。
- 不依赖 core 网站的"智能控制"大模型链路(该链路因 `decision_core` runaway 目前不可用,是 MT 侧 bug)——验证一律走**手动点执行 / 看数据流**。

## 2. 关键约束(已与用户对齐的决策)

1. **入库门槛(最严)**:main 只收 `accepted`。`offline-green` 不能合并。
2. **验证方式**:网站上靠**手动"执行"按钮 / DATA STREAMS 数据流面板**验证,不靠大模型。
3. **文档范围**:通用方案只写"卡已注册、网站能打开"之后的网站验证步骤;环境拉起给前提清单 + 指向驱动仓库。
4. **交付形式**:文档化验收清单 **+** 自动化前置检查脚本。
5. **结构**:方案 A —— 一份权威验证文档 + 一个前置脚本,标准/流程/PR 模板只加指针,不重复内容。

## 3. 状态模型与入库门槛

三种状态,**只有 `accepted` 能合入 main**:

| 状态 | 含义 | 能进 main? |
|---|---|---|
| `draft` | 仅设计,未实现/未测 | ❌ |
| `offline-green` | 离线测试全绿(可含实机只读碎片) | ❌ 只能待在分支 / 开着的 PR |
| `accepted` | 网站验证通过 + MT 验收通过 + 完整真实样本 + 证据齐 | ✅ 唯一可合 |

- PR 要合并,必须 `metadata.status == accepted` 且 `verification/accepted.md` 齐备(网站证据 + MT 验收记录 + 真实样本)。
- `offline-green` 的 PR **可以开着**(方便协作/审阅),标题带 `[pending-web]`,审核**不予合并**。

**对现有 pending 分支的处置**:`add/unitree-go1-readonly-verified-3cards`(fall_alarm/net/odometry,offline-green)保持开着不合,标 `[pending-web]`;待狗上电、上网站验证 + MT 验收后升 `accepted` 再合。当前 main 仍只有 feet/imu/loco_state 三张 accepted。

## 4. 文件清单(落地在 `phanthy-motus-cards`)

| 文件 | 动作 | 内容 |
|---|---|---|
| `docs/WEBSITE_VERIFICATION.md` | 新建 | 唯一权威的"怎么在 core 网站上证明卡片真能用"流程 |
| `tools/preflight.py` | 新建 | 纯标准库前置检查脚本(查驱动 MCP 契约 + 真数据) |
| `docs/CARD_TEMPLATE/verification/accepted.md` | 新建 | accepted 证据模板(现模板缺 `verification/`) |
| `docs/SUBMISSION_STANDARD.md` | 改 | 加"状态与入库门槛"节 + 验证证据要求,指向验证文档 |
| `docs/SUBMISSION_PROCESS.md` | 改 | PR 与合并之间插入"网站验证 + MT 验收"步骤 |
| `.github/PULL_REQUEST_TEMPLATE.md` | 改 | 加网站验证区块 + 证据链接 + preflight 输出 |
| `README.md` | 改(小) | 状态图例已加,补一句入库门槛 |

## 5. 通用网站验证流程(`docs/WEBSITE_VERIFICATION.md` 大纲)

> 开篇声明:本文从"卡已注册进 core、网站能打开"开始;环境拉起不在范围,见所在驱动仓库部署文档。

- **§0 前提清单**(勾选式):狗上电 · 驱动部署并注册进 core · 转发器带 `--ipc=host` 在跑(数据流前提) · core 网站能打开。任一不满足先回驱动仓库解决。
- **§1 自动前置检查**:跑 `tools/preflight.py`。机器能判的先全绿(注册/契约/真数据),再上网站费人力。
- **§2 网站"看得到"**:打开 core 网站 → 设备里能看到这张卡,名称/描述/类型/控制等级与 `metadata.json` 一致。
- **§3 网站"验功能"**(分卡型):
  - 传感器卡:DATA STREAMS 面板出现该卡 topic,数据在跳动;**制造一个真实变化**证明非伪造(动一下狗看 IMU/里程值变、遮挡改读数等)。
  - 执行器卡:点该卡"执行"按钮发一个动作 → 观察机器人产生**对应真实效果**(或配套状态卡的值随之变);⚠️ 让狗动前置安全:空旷、站稳、留急停 `damp`。
- **§4 留证**:截图(卡可见 + 数据流/执行效果)+ 一段真实返回 JSON + 采集时间/环境/后端。截图等二进制**不入库**,用链接 / PR 附图,正文只留指针。
- **§5 MT 验收**:请 MT 在网站上确认功能实现 → 记录验收人/日期/结论。
- **§6 通过后**:证据写入 `verification/accepted.md`,`metadata.status→accepted`,提 PR 请求合并。

## 6. `tools/preflight.py` 设计

- **运行**:`python3 tools/preflight.py <卡目录> --host <驱动IP> [--port 15704]`
  - 例:`python3 tools/preflight.py cards/unitree-go1/net --host 10.100.130.4`
- **依赖**:仅标准库 `urllib` / `json` / `argparse`,无第三方库,任何人可跑。
- **MCP 线格式**(与驱动 `tests/call.sh` 一致):
  - 端点 `POST http://<host>:<port>/mcp`,`Content-Type: application/json`。
  - `tools/list`:`{"jsonrpc":"2.0","id":1,"method":"tools/list"}` → 响应 `result.tools[]`(每项 = 卡的 `get_tool()` 描述符)。
  - `tools/call`:`{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"<卡>","arguments":{"action":"read"}}}` → 响应 `result.content[0].text` 是卡返回的 JSON 字符串。
- **检查项**(逐项 PASS / WARN / FAIL):
  1. 读 `<卡目录>/metadata.json`,取 `mcp_tool.name/type/readOnly/topic_out`、`payload_fields`、`category`。
  2. `tools/list`:断言 `result.tools[]` 含 `name == 目录名`,且描述符 `type` / `readOnly` / `topic_out[].topic` 与 metadata 一致。
  3. **传感器卡**(`category==sensor`):`tools/call ... action:read` → 解析 `result.content[0].text`;断言含声明的 `payload_fields` 关键字段;若含 `offline:true` 或返回错误码 `NO_FEEDBACK` → **WARN**"后端离线/无新帧,不是真数据,先让驱动接真机"。
  4. **执行器卡**(`category==actuator`):**不自动执行动作**(会让狗动,不安全)→ 只校"已注册 + descriptor 有 `inputSchema`",打印"执行器卡请人到网站点执行验证,脚本不代劳"。
- **输出**:逐项结果 + 汇总;`exit 0` = 机器判的全绿、可上网站,非 0 = 先修。
- **边界声明**(脚本结尾打印一行):preflight 查的是**驱动 MCP 层的契约与真数据**,**不能替代**网站可见性 / 数据流 / MT 验收——那三步机器判不了,必须人上网站。
- **错误处理**:连不上/超时 → FAIL 并提示"驱动没在跑或地址错,先按驱动仓库把驱动起起来";metadata.json 不存在/非法 → FAIL 指出问题;`tools/call` 返回非预期结构 → FAIL 并打印原始响应片段。

## 7. 对标准 / 流程 / PR 模板的改动

**`docs/SUBMISSION_STANDARD.md`**
- 新增 §8"状态与入库门槛":三状态定义 + "只有 accepted 能合入 main"。
- 改 §5(verification):accepted 卡必须含 ①网站验证证据(卡可见截图 + 数据流/执行效果截图)②MT 验收记录(人/日期/结论)③完整真实 JSON 样本;指向 `WEBSITE_VERIFICATION.md`。
- 自检清单加 2 条:`[ ] preflight.py 全绿`、`[ ] accepted 卡:网站证据 + MT 验收记录齐`。

**`docs/SUBMISSION_PROCESS.md`**
- A 流程(新增卡)在"开 PR"与"合并"间插入:`跑 preflight → 网站按 WEBSITE_VERIFICATION 验 → MT 验收 → 齐证据 → 状态升 accepted → 才合并`。
- 明写:offline-green 的 PR 可开着(标 `[pending-web]`)但不合并。
- C(审核人检查)加一条:合并前确认 `status==accepted` 且证据齐。

**`.github/PULL_REQUEST_TEMPLATE.md`**
- 加"网站验证"区块:粘 preflight 输出摘要、网站截图链接、真实样本 JSON、MT 验收人/日期/结论。
- 自检清单加对应勾选项;顶部提示"未达 accepted 请在标题加 `[pending-web]`,审核不予合并"。

## 8. accepted 证据模板(`docs/CARD_TEMPLATE/verification/accepted.md`)

```markdown
# 验收证据 —— <卡名>

- 验收日期 / 验收人(MT):
- 环境:狗地址 · 后端(factory / legged_sdk)· 驱动 commit · core 版本
- preflight:<全绿输出摘要,或贴关键几行>

## 网站验证证据
- 卡可见:<截图路径/链接>(设备页看到该卡,名称/类型正确)
- 功能实现:<截图/链接>(传感器=DATA STREAMS 数据流;执行器=点执行后的真实效果)

## 离线测试
- <测试文件 + 结果摘要,如 test_mt_ext.py ... 27 OK>

## 实机真实数据样本
​```json
{ ...一段真实返回;传感器最好两态对比... }
​```

## MT 验收结论
- 通过 / 备注:
```

## 9. 分节测试策略

- `preflight.py`:对**离线 fake 驱动**跑(Mac 上起一份 `mode:fake` 的 go1 驱动,或用一个最小 mock MCP)验证:①注册校验能过 ②契约不符能报 FAIL ③传感器 offline 数据能 WARN ④连不上能 FAIL。不需要真狗。
- 文档类改动:人工过一遍自检清单 + 确认交叉指向不断链。
- 端到端(网站验证流程本身)只能等狗上电时用一张真卡走一遍确认可操作——列为实机待办,不阻塞本次文档/脚本落地。

## 10. 交付顺序(供写实现计划参考)

1. `docs/WEBSITE_VERIFICATION.md`(核心流程,其它文件都指向它)。
2. `tools/preflight.py` + 对 fake 驱动的自测。
3. `docs/CARD_TEMPLATE/verification/accepted.md` 模板。
4. 改 `SUBMISSION_STANDARD.md` / `SUBMISSION_PROCESS.md` / PR 模板 / README。
5. 把 pending 分支标 `[pending-web]`(改 PR 标题即可,不动卡内容)。
