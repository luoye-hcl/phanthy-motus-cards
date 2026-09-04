# mc_mode —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `mc_mode` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

切换 MC 运控状态机模式（SetMcAction）

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": [
        "passive_default",
        "soft_emergency_stop",
        "damping_default",
        "zero_torque_default",
        "joint_default",
        "joint_freeze",
        "stand_default",
        "stand_body_control",
        "locomotion_default",
        "run_default",
        "locomotion_step",
        "vr_remote_controller",
        "sit_down_default",
        "crouch_down_default",
        "lie_down_default",
        "stand_up_default",
        "ascend_stairs",
        "descend_stairs"
      ],
      "description": "Action to perform"
    }
  },
  "required": [
    "action"
  ],
  "x-action-params": {
    "passive_default": {
      "params": [],
      "description": "切换到 passive_default 模式"
    },
    "soft_emergency_stop": {
      "params": [],
      "description": "切换到 soft_emergency_stop 模式"
    },
    "damping_default": {
      "params": [],
      "description": "切换到 damping_default 模式"
    },
    "zero_torque_default": {
      "params": [],
      "description": "切换到 zero_torque_default 模式"
    },
    "joint_default": {
      "params": [],
      "description": "切换到 joint_default 模式"
    },
    "joint_freeze": {
      "params": [],
      "description": "切换到 joint_freeze 模式"
    },
    "stand_default": {
      "params": [],
      "description": "切换到 stand_default 模式"
    },
    "stand_body_control": {
      "params": [],
      "description": "切换到 stand_body_control 模式"
    },
    "locomotion_default": {
      "params": [],
      "description": "切换到 locomotion_default 模式"
    },
    "run_default": {
      "params": [],
      "description": "切换到 run_default 模式"
    },
    "locomotion_step": {
      "params": [],
      "description": "切换到 locomotion_step 模式"
    },
    "vr_remote_controller": {
      "params": [],
      "description": "切换到 vr_remote_controller 模式"
    },
    "sit_down_default": {
      "params": [],
      "description": "切换到 sit_down_default 模式"
    },
    "crouch_down_default": {
      "params": [],
      "description": "切换到 crouch_down_default 模式"
    },
    "lie_down_default": {
      "params": [],
      "description": "切换到 lie_down_default 模式"
    },
    "stand_up_default": {
      "params": [],
      "description": "切换到 stand_up_default 模式"
    },
    "ascend_stairs": {
      "params": [],
      "description": "切换到 ascend_stairs 模式"
    },
    "descend_stairs": {
      "params": [],
      "description": "切换到 descend_stairs 模式"
    }
  }
}
```

## 使用约束

- 切换模式会改变姿态、阻尼或控制权；只有现场安全且用户明确授权后才能调用。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
