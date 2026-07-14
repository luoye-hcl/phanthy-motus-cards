# <卡片名> —— <一句话能力>

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `<厂商-型号>` |
| 卡片名(MCP 工具名) | `<card_name>` |
| 类型 | `sensor` 或 `actuator` |
| 控制等级 | `ANY` / `HIGHLEVEL` / `LOWLEVEL` |
| 作者 | `<github-id>` |
| 状态 | `draft` / `offline-green` / `accepted(YYYY-MM-DD)` |

## 能力

<!-- 这张卡做什么,给谁用(大模型/人),典型场景 -->

## 接口

<!-- 传感器卡:输出 topic + format;read 动作;下面字段表。
     执行器卡:改成 action 列表(动作名/入参名/类型/范围/单位/必填/是否需 confirm)/返回包络/错误码。 -->

- 输出 topic:`/{ns}/<topic>`  格式:`data/json`
- 采样频率:`<hz>` Hz
- 读取:`{"action":"read"}`

### 字段

| 字段 | 含义 | 单位 |
|---|---|---|
| … | … | … |

## 数据来源 / 实现位置

- 源仓库:`<owner/repo>`
- 文件:`<path>`  类:`<ClassName>`
- 依赖:`<公共层/控制核心>`
- 注册:`<在哪注册>`;驱动镜像/端口:`<image / port>`

## 状态说明

<!-- 离线测试情况;若已实机验收,写清验收日期/环境/页面是否正常(与 verification/ 对应) -->
