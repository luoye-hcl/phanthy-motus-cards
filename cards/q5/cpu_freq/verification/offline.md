# 验收证据 —— cpu_freq

> 实机验证日期: 2026-08-13
> 测试环境: Q5 Jetson 192.168.8.40, 驱动容器 q5-driver-huang (MCP 15794)

## 实机验证结果

### Topic 信息

| 项目 | 值 |
|---|---|
| 数据源 Topic | `/cpu_freq` |
| 消息类型 | `std_msgs/msg/String` |
| 状态 | ✅ 有数据流(CPU 各核心频率,JSON 格式) |

### 真实数据样本

```json
{"cpu_freq":{"cpufreq_name_list":["cpu","cpu_max","cpu_min","cpu_avg","cpu_0","cpu_1","cpu_2","cpu_3","cpu_4","cpu_5","cpu_6","cpu_7","cpu_8","cpu_9","cpu_10"]}}
```

## 完整验收清单

- [x] 插件 `cpu_freq.py` 已实现并部署
- [x] MCP tools/list 确认工具 `cpu_freq` 已注册
- [x] 桥接发现并 bridging `/nvidia_desktop/q5/cpu_freq`
- [ ] core 网页面板呈现该卡数据
- [ ] MT 验收记录(人/日期/结论)
