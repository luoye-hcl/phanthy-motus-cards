# 验收证据 —— imu

## 离线检查

- [ ] `metadata.json` JSON 语法通过
- [ ] 画布工具注册为 `imu`

## 实机检查

- [ ] `rt/lowstate` 有数据
- [ ] `/state/imu` 持续输出姿态、角速度和加速度
- [ ] 四元数顺序确认是 `[w,x,y,z]`
