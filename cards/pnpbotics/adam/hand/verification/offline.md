# 验收证据 —— hand

## 离线检查

- [ ] `metadata.json` JSON 语法通过
- [ ] 画布工具注册为 `hand`

## 实机检查

- [ ] `rt/handstate` 有数据
- [ ] `get_state` 返回左右手 6 维数组
- [ ] 人工确认手部无障碍物后再验证 `open`/`close`
