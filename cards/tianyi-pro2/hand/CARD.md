# hand —— 天轶2.0 Pro 仿生手状态(只读传感器卡)

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `tianyi-pro2` |
| 卡片名(MCP 工具名) | `hand` |
| 类型 | `sensor`(只读,无执行按钮) |
| 控制等级 | `ANY`(高层/低层都出) |
| 作者 | `huangchanglong` |
| 状态 | `draft`(未实机验收) |

## 能力

读取天轶2.0 Pro 双手 inspire_hand 仿生手 6 DOF 状态(位置/速度/力),左右手各一路 ROS2 topic。用于抓取状态监控、力控反馈观察,供大模型或人监控手部当前张合与受力。

> ⚠ **重要**:数据中的 position / velocity / effort **均为百分比**(0–1),不是物理单位。文档明确强调两次。

## 接口

- 输出 topic(2 路):
  - `/inspire_hand/state/left_hand`   格式:`sensor_msgs/msg/JointState`  频率:24.8 Hz
  - `/inspire_hand/state/right_hand`  格式:`sensor_msgs/msg/JointState`  频率:24.8 Hz
- 采样频率:`24.8` Hz(2026-07-28 实测)
- 读取:`{"action":"read"}`(纯只读,`readOnly:true`)

### 实测数据样本(2026-07-28,x86 192.168.41.1,bodycontrol 已激活)

| 手 | 关节 | position(%) | effort(%) | 说明 |
|---|---|---|---|---|
| left | 1-6 | ~1.0 | ~0.2 | 手张开,effort 较低 |
| right | 1-6 | ~1.0 | ~0.2 | 手张开,effort 较低 |

> position ~1.0 表示手完全张开。effort ~0.2 表示无负载。

### 字段(每路 JointState)

| 字段 | 含义 | 单位 |
|---|---|---|
| `header.stamp` | 采样时间戳 | ns |
| `name[]` | 手指关节名,id=1 小指 / id=2 无名指 / id=3 中指 / id=4 食指 / id=5 拇指弯曲 / id=6 拇指旋转 | — |
| `position[]` | 各手指位置(张开百分比) | %(0–1) |
| `velocity[]` | 各手指速度 | %(0–1) |
| `effort[]` | 各手指力 | %(0–1) |

> `name` 数组元素为字符串"id=1"等(参见天轶2.0 SDK"手部关节-全局值说明")。

### 聚合后 JSON 输出结构

```json
{
  "left": {
    "fingers": [
      { "id": 1, "name": "little",     "position": 0.0, "velocity": 0.0, "effort": 0.0 },
      { "id": 2, "name": "ring",       "position": 0.0, "velocity": 0.0, "effort": 0.0 },
      { "id": 3, "name": "middle",     "position": 0.0, "velocity": 0.0, "effort": 0.0 },
      { "id": 4, "name": "fore",       "position": 0.0, "velocity": 0.0, "effort": 0.0 },
      { "id": 5, "name": "thumb_bend", "position": 0.0, "velocity": 0.0, "effort": 0.0 },
      { "id": 6, "name": "thumb_rot",  "position": 0.0, "velocity": 0.0, "effort": 0.0 }
    ]
  },
  "right": { "fingers": [ ... ] },
  "timestamp_ms": 1784025258226,
  "control_level": "ANY"
}
```

## 数据来源 / 实现位置

- 源仓库:`<待建 tianyi-pro2-driver>`(独立新驱动,不复用 tiangong_pro 代码)
- 文件:`plugins/hand.py`  类:`HandStatePlugin`(待实现)
- 依赖:`ros_bridge.py`(ROS2 订阅桥)、`sensor_msgs/msg/JointState`
- 注册:`main.py` 插件聚合;驱动镜像/端口:待定(MCP HTTP server, JSON-RPC 2.0)

> 本卡为 `draft` 阶段,驱动代码尚未编写。接口字段以天轶2.0 SDK 文档(2026-05-21 版)为准。
> 与 `tiangong_pro/plugins/hand.py` 的差异:天轶2.0 文档以 topic 为主读手部状态(service 保留给 set_angle_flexible 等控制接口,见动作卡 `hand_ctrl`)。

## 状态说明

- 离线:未实现(驱动代码待写)。
- 实机:未验收。待真机 `ros2 topic echo /inspire_hand/state/left_hand` 确认字段后升 `offline-green`。
- 升 `accepted` 流程:见 `docs/WEBSITE_VERIFICATION.md`。
