# 验收证据 —— <卡名>

- 验收日期 / 验收人(MT):<YYYY-MM-DD> / <MT 验收人>
- 环境:狗地址 <ip> · 后端(factory / legged_sdk)· 驱动 commit <hash> · core 版本 <ver>
- preflight:<`python3 tools/preflight.py cards/<robot>/<card> --host <ip>` 全绿输出摘要,或贴关键几行>

## 网站验证证据
- 卡可见:<截图链接>(设备页看到该卡,名称/类型正确)
- 功能实现:<截图/录屏链接>(传感器=DATA STREAMS 数据流+变化前后;执行器=点执行后的真实效果)

## 离线测试
- <测试文件 + 结果摘要,如 `test_mt_ext.py ... 27 OK`>

## 实机真实数据样本
```json
{ "示例": "一段真实返回;传感器最好两态对比(如站立 vs 阻尼)" }
```

## MT 验收结论
- 通过 / 备注:<结论>
