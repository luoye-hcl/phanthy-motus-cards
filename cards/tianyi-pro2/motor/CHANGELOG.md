# CHANGELOG — motor

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.1.0 — 2026-07-28 — huangchanglong

- 实机采集频率:head=400Hz,waist=500Hz,arm=500Hz,leg=500Hz(四路不一致,`metadata.json.rate_hz` 设 null,在 `topic_out` 各项标注)。
- 实机真实数据样本(站立静姿)已采集,写入 `verification/offline.md`,四路 topic 原始 YAML 片段齐全。
- 确认 waist 关节 32(Waist Pitch)在实机数据中存在(此前文档已知,实机验证)。
- 待机现象:waist 与 leg 的 speed/current/temperature 全为 0,仅 pos 有值,推测模组未上电/待机,需上电后复测。
- 字段结构(name/pos/speed/current/temperature/error)与 SDK 文档完全一致,head/arm 温度合理(32–47℃)。
- `metadata.json` 版本递增到 1.1.0,`topic_out` 标注各路频率。
- 实机验收清单部分项打 ✅(频率回填、字段确认、JSON 校验通过)。

## v1.0.0 — 2026-07-28 — huangchanglong

- 首次收录。天轶2.0 Pro 全身 21 电机状态只读传感器卡,聚合 `/head/status` `/waist/status` `/arm/status` `/leg/status` 四路 topic。
- 状态 `draft`(驱动代码待写,未实机验收)。
- 接口字段以天轶2.0 SDK 文档(2026-05-21 版)为准。
