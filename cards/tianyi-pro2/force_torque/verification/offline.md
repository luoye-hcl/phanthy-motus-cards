# 验收证据 —— force_torque

> 本卡为 `draft` 阶段,驱动代码尚未实现。以下为验收清单,部分实机项已于 2026-07-28 完成采集(见下文)。

## 离线测试(待补)

- [ ] 编写 `tests/test_force_torque.py`:覆盖左右臂 WrenchStamped 解析、force/torque 三轴映射
- [ ] `bash tests/run_all.sh` 全绿
- [ ] `python3 -m json.tool metadata.json` 通过

## 实机验收(部分完成)

- [x] 真机环境:`ros2 topic echo /arm_6dof_left` 确认字段与坐标系方向 ✅ (2026-07-28)
- [x] `ros2 topic hz /arm_6dof_left` 确认 100Hz ✅ (2026-07-28,实测 100 Hz,与文档一致)
- [x] `ros2 topic echo /arm_6dof_right` 确认字段与坐标系方向 ✅ (2026-07-28)
- [x] `ros2 topic hz /arm_6dof_right` 确认 100Hz ✅ (2026-07-28,实测 100 Hz)
- [x] 消息类型 `geometry_msgs/msg/WrenchStamped` 确认 ✅ (2026-07-28)
- [x] frame_id 确认:`6dof_left_link` / `6dof_right_link` ✅ (2026-07-28)
- [x] 单位确认:力 N,力矩 N·m ✅ (2026-07-28)
- [ ] 验证坐标系方向(X 前/Y 左/Z 上)与力正负号(仅完成站立态,缺接触态/受力态对照)
- [ ] `tools/preflight.py cards/tianyi-pro2/force_torque --host <天轶IP>` 全绿
- [ ] core 网页 DATA STREAMS 面板呈现该卡实时数据流
- [ ] 完整真实 JSON 样本(自由态/接触态/受力态多场景,当前仅站立自然下垂态)
- [ ] MT 验收记录(人/日期/结论)

## 实机真实数据样本(2026-07-28 采集)

> 采集条件:机器人站立状态,手臂自然下垂。
> 话题:`/arm_6dof_left`、`/arm_6dof_right`(均 100 Hz)
> 消息类型:`geometry_msgs/msg/WrenchStamped`
> frame_id:`6dof_left_link` / `6dof_right_link`
> 单位:力 N,力矩 N·m

### /arm_6dof_left (100 Hz)

```yaml
header:
  stamp:
    sec: 1785235600
    nanosec: 347804381
  frame_id: 6dof_left_link
wrench:
  force:
    x: 2.015584707260132
    y: 22.425914764404297
    z: 0.6905168294906616
  torque:
    x: 0.3446711301803589
    y: 0.1496451497077942
    z: 0.14255505800247192
```

### /arm_6dof_right (100 Hz)

```yaml
header:
  stamp:
    sec: 1785235601
    nanosec: 409433664
  frame_id: 6dof_right_link
wrench:
  force:
    x: -7.082237243652344
    y: 15.675399780273438
    z: -1.5449143648147583
  torque:
    x: 0.22283485531806946
    y: 0.0500481054186821
    z: 0.2757679522037506
```

### 聚合 JSON 样本(站立态)

```json
{
  "left":  { "force": {"x":2.015584707260132,"y":22.425914764404297,"z":0.6905168294906616}, "torque":{"x":0.3446711301803589,"y":0.1496451497077942,"z":0.14255505800247192} },
  "right": { "force": {"x":-7.082237243652344,"y":15.675399780273438,"z":-1.5449143648147583}, "torque":{"x":0.22283485531806946,"y":0.0500481054186821,"z":0.2757679522037506} },
  "timestamp_ms": 1785235600347,
  "control_level": "ANY"
}
```
