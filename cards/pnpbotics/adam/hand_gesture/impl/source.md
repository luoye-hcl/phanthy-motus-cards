# 实现来源 —— hand_gesture

- 源仓库：`4paradigm/phanthymotus-driver`
- 文件：`pndbotics/adam/device.py`
- 类：`HandGesturePlugin`
- 控制接口：共享 `HandPlugin` 的 DDS `rt/handcmd` 发布线程
- 发布频率：约 `400Hz`
- 状态来源：共享 DDS `rt/handstate` 缓存和最近目标
