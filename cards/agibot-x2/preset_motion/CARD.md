# preset_motion —— AgiBot X2 actuator 卡

## 基本信息

| 项 | 值 |
|---|---|
| 机器人 | `agibot-x2` |
| MCP 工具名 | `preset_motion` |
| 类型 | `actuator` |
| 状态 | `draft` |

## 能力

播放预设动作库（SetMcPresetMotion）

## 接口

- 无 ROS topic 输出；通过 MCP 服务响应返回数据。

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": [
        "raise_hand",
        "wave_hand",
        "shake_hand",
        "flying_kiss_hand",
        "clap_hand",
        "clipfist",
        "salute",
        "turn_wave_hand",
        "interaction_bow",
        "interaction_like",
        "interaction_ye",
        "interaction_sweatheart",
        "interaction_sad",
        "interaction_lightwave",
        "interaction_hug",
        "interaction_handx",
        "interaction_chestwave",
        "interaction_cheer",
        "interaction_blowkiss",
        "interaction_bassdance1",
        "interaction_bassdance2",
        "hitclap",
        "interaction_speak",
        "interaction_photoposture",
        "interaction_phototrippleposture",
        "point_head",
        "shake_head"
      ],
      "description": "Action to perform"
    },
    "area": {
      "type": "string",
      "enum": [
        "left_hand",
        "right_hand"
      ],
      "description": "受控手臂；仅 raise_hand/wave_hand/shake_hand 等单臂动作需要，必须传 left_hand 或 right_hand"
    },
    "interrupt": {
      "type": "boolean",
      "default": true,
      "description": "是否打断当前动作"
    }
  },
  "required": [
    "action"
  ],
  "x-action-params": {
    "raise_hand": {
      "params": [
        "area",
        "interrupt"
      ],
      "description": "播放预设动作 raise_hand（单臂动作，area 必须传 left_hand/right_hand，否则返回 code=1 失败）"
    },
    "wave_hand": {
      "params": [
        "area",
        "interrupt"
      ],
      "description": "播放预设动作 wave_hand（单臂动作，area 必须传 left_hand/right_hand，否则返回 code=1 失败）"
    },
    "shake_hand": {
      "params": [
        "area",
        "interrupt"
      ],
      "description": "播放预设动作 shake_hand（单臂动作，area 必须传 left_hand/right_hand，否则返回 code=1 失败）"
    },
    "flying_kiss_hand": {
      "params": [
        "area",
        "interrupt"
      ],
      "description": "播放预设动作 flying_kiss_hand（单臂动作，area 必须传 left_hand/right_hand，否则返回 code=1 失败）"
    },
    "clap_hand": {
      "params": [
        "area",
        "interrupt"
      ],
      "description": "播放预设动作 clap_hand（单臂动作，area 必须传 left_hand/right_hand，否则返回 code=1 失败）"
    },
    "clipfist": {
      "params": [
        "area",
        "interrupt"
      ],
      "description": "播放预设动作 clipfist（单臂动作，area 必须传 left_hand/right_hand，否则返回 code=1 失败）"
    },
    "salute": {
      "params": [
        "area",
        "interrupt"
      ],
      "description": "播放预设动作 salute（单臂动作，area 必须传 left_hand/right_hand，否则返回 code=1 失败）"
    },
    "turn_wave_hand": {
      "params": [
        "area",
        "interrupt"
      ],
      "description": "播放预设动作 turn_wave_hand（单臂动作，area 必须传 left_hand/right_hand，否则返回 code=1 失败）"
    },
    "interaction_bow": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_bow"
    },
    "interaction_like": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_like"
    },
    "interaction_ye": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_ye"
    },
    "interaction_sweatheart": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_sweatheart"
    },
    "interaction_sad": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_sad"
    },
    "interaction_lightwave": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_lightwave"
    },
    "interaction_hug": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_hug"
    },
    "interaction_handx": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_handx"
    },
    "interaction_chestwave": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_chestwave"
    },
    "interaction_cheer": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_cheer"
    },
    "interaction_blowkiss": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_blowkiss"
    },
    "interaction_bassdance1": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_bassdance1"
    },
    "interaction_bassdance2": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_bassdance2"
    },
    "hitclap": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 hitclap"
    },
    "interaction_speak": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_speak"
    },
    "interaction_photoposture": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_photoposture"
    },
    "interaction_phototrippleposture": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 interaction_phototrippleposture"
    },
    "point_head": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 point_head"
    },
    "shake_head": {
      "params": [
        "interrupt"
      ],
      "description": "播放预设动作 shake_head"
    }
  }
}
```

## 使用约束

- 会触发真实肢体动作。`raise_hand`、`wave_hand`、`shake_hand`、`flying_kiss_hand`、`clap_hand`、`clipfist`、`salute`、`turn_wave_hand` 必须传 `area=left_hand` 或 `right_hand`，否则 vendor 返回 `code=1`。
- `draft` 阶段不以执行动作作为画布验收手段。

## 数据来源

- 运行时驱动：AgiBot AimDK X2，ROS 2 Humble + `aimdk_msgs`。
- 实时依据：2026-09-04 对 X2 MCP `tools/list` 的返回。
- 实现：`agibot/x2/device.py`。
