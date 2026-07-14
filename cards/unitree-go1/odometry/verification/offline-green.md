# 验收证据 —— odometry

- **当前状态**:`offline-green`(离线测试全绿 + 实机只读已验证读取;完整 JSON 样本待采后升 `accepted`)

## 离线测试

- `tests/test_mt_ext.py::TestOdometry`:
  - `test_read_structure` —— 返回含 `position_m` / `yaw_rad` / `total_distance_m` / `displacement_m` / `origin_m`
  - `test_reset_origin` —— `reset_origin` 返回 `applied.origin_m`,起点被重置
  - `test_tool_readonly_no_execute` —— 工具声明只读、无 action 按钮(`reset_origin` 仍可经 dispatch 调用)
  - `test_odometer_accumulates` —— 里程累加、异常跳变丢弃(`_odometer_m` 按段累计)
- 运行结果:`Ran 27 tests ... OK`(`test_mt_ext.py` 全绿,2026-07-15 本地复跑)。

## 实机只读验证(2026-07-13)

- 经 factory 后端(HIGHLEVEL,读真实 HighState)实机只读调用 `{"action":"read"}`,读取 OK。
- 同日运动实测印证里程/航向随真实移动变化(`turn_angle` 90°→实测 91.3°、`move_distance` 走位读里程闭环)。
- 参见 `luoye-hcl/go1-driver:docs/WORKLOG_2026-07-13.md`。

## 待补(升 accepted 的条件)

- 狗上电、遥控扶站后现采一段**完整 JSON 返回样本**(`{position_m, yaw_rad, total_distance_m, origin_m, displacement_m:{dx,dy,distance}, offline:false, ...}`)+ 采集时间/环境;
- 最好含"走一段后位移变化"的前后对比,印证里程随真实移动累计;
- core 网页监控页 DATA STREAMS 面板呈现该卡数据流截图/记录。
- 齐备后:新增 `verification/accepted.md`、`metadata.json` 加 `accepted_date` 并把 `status` 改 `accepted`、`version` 递增、`CHANGELOG` 加条。
