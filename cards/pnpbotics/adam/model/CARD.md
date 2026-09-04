# model —— Adam 3D 模型资源卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `pnpbotics-adam` |
| 卡片名 | `model` |
| 类型 | `system`(只读资源) |
| 控制等级 | `ANY` |
| 状态 | `draft` |

## 能力

返回当前配置机型对应的 Adam URDF，用于画布 3D 骨架可视化。支持 `lite`、`sp` 和 `pro` 机型。

## 接口

- MCP 工具：`model`
- 返回：`urdf` 字符串

## 数据来源

驱动文件：`pnpbotics/adam/device.py`，类：`ModelPlugin`；资源目录：`pnpbotics/adam/resource/`。

## 验收状态

待镜像构建后在画布确认模型可加载且与关节数据对应。
