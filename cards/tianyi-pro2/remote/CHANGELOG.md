# CHANGELOG — remote

本卡的版本变更记录(倒序)。每次更新必加一条,并同步递增 `metadata.json` 的 `version`。

## v1.1.0 — 2026-07-28 — huangchanglong

- 实机采集(2026-07-28):用 `ros2 topic echo/hz` 在真机上确认两个 SBUS topic 同频 43.3 Hz,远高于文档预估。
- `metadata.json`:`rate_hz` 由 `null` 更新为 `43.3`;`topic_out` 新增 `/sbus_data`(`sensor_msgs/msg/Joy`);版本递增到 `1.1.0`。
- `payload_fields`:新增 `joy.axes`(12 轴数组)与 `joy.buttons`(实机为空数组)说明,按键事件以 `/sbus_data/event` 为准。
- CARD.md:接口段标注双 topic 同频 43.3 Hz;新增 Joy 字段表;追加实机空闲态真实 YAML 样本两份(`/sbus_data` 与 `/sbus_data/event`,后者 H 键被按下、摇杆居中)。
- verification/offline.md:勾选 topic 存在性、频率、字段值域项;保留按键态/摇杆态样本采集等待办。
- 状态仍为 `draft`(驱动代码未实现);待补按键态/摇杆推到位态多场景样本。

## v1.0.0 — 2026-07-28 — huangchanglong

- 首次收录。天轶2.0 Pro 遥控器状态只读传感器卡,订阅 `/sbus_data/event`。
- 覆盖 8 按键(A/B/C/D 按钮 + E/F/G/H 拨片)事件值与实时键值,双摇杆四轴(x1/y1/x2/y2)。
- 状态 `draft`(驱动代码待写,未实机验收)。
