"""Review excerpt for the Unitree G1 root Driver teleoperation contract.

The deployable implementation lives in ``phanthymotus-driver/unitree/g1``.
This hardware-free excerpt keeps its exact descriptors and review invariants;
it is not a second Driver and cannot publish DDS commands.
"""

from __future__ import annotations

import copy
import hashlib
import json

PROFILE_ID = "unitree_g1_23_dual_arm_controller_v1"
SHADOW_DIGEST = "3a333966ddb1c146c3852e02e90b59825e6844d6fbd9937502741af3b96a0757"
LIVE_DIGEST = "016f7e83955ec2dd47333b5ae2c33c85c695b43d2d1cc93b4bbdcc4055bfda4c"

CAPABILITIES = {
    "profile_id": PROFILE_ID,
    "input_bindings": {
        "head": {"required": True, "role": "reference"},
        "left_controller": {"required": True, "role": "left_end_effector"},
        "right_controller": {"required": True, "role": "right_end_effector"},
    },
    "outputs": {
        "dual_arm": {"enabled": True, "joint_count": 10},
        "base": {"enabled": False},
        "hands": {"enabled": False},
    },
    "effectors": ["dual_arm"],
}


def _binding(mode: str) -> dict:
    if mode not in {"shadow", "live"}:
        raise ValueError("mode must be shadow or live")
    live = mode == "live"
    return {
        "protocol": "motus.teleop.live.v1" if live else "motus.teleop.shadow.v1",
        "mode": mode,
        "profile_id": PROFILE_ID,
        "capabilities": copy.deepcopy(CAPABILITIES),
        "dispatch_contract": (
            "motus.teleop.dispatch.hardware.v1"
            if live
            else "motus.teleop.dispatch.recording.v1"
        ),
        "signaling": {
            "protocol": "motus.teleop.webrtc-offer-answer.v1",
            "path": "/offer",
            "access": "authenticated-core-proxy-only",
            "audience": "motus-teleop-rtc",
        },
    }


def capability_digest(mode: str) -> str:
    encoded = json.dumps(
        _binding(mode),
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def teleop_session_tool_definition(mode: str = "shadow") -> dict:
    """Return the exact mode-specific tool emitted by the root G1 Driver."""

    live = mode == "live"
    binding = _binding(mode)
    identity = {
        "boot_id": {"type": "string", "format": "uuid"},
        "session_id": {"type": "string", "format": "uuid"},
        "epoch": {"type": "integer", "minimum": 1},
        "fence": {"type": "string", "minLength": 24},
    }
    prepare = "prepare_live" if live else "prepare_shadow"
    actions = {
        "stop": {"params": [], "description": "Release the teleoperation lifecycle safely"},
        prepare: {
            "params": ["session_id", "epoch", "fence"],
            "description": (
                "Prepare explicitly enabled G1 arm_sdk hardware control"
                if live
                else "Prepare a zero-output G1 dual-arm Shadow session"
            ),
        },
        "heartbeat": {"params": list(identity), "description": "Renew the Core-owned lease"},
        "pause": {"params": list(identity), "description": "Pause and confirm safe output"},
        "release": {"params": list(identity), "description": "Release authority and confirm safe output"},
        "soft_stop": {"params": list(identity), "description": "Latch safe output until a newer prepare"},
        "status": {"params": [], "description": "Read bounded session and output diagnostics"},
    }
    return {
        "name": "teleop_session",
        "type": "actuator",
        "multiInstance": False,
        "description": (
            "Unitree G1_23 dual-arm controller teleoperation. Base and hands are "
            "disabled; only the root G1 Driver may own the arm_sdk publisher."
        ),
        "annotations": {"destructiveHint": live, "idempotentHint": False},
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "action": {"type": "string", "enum": list(actions)},
                **identity,
            },
            "required": ["action"],
            "x-action-params": actions,
        },
        "x-teleop": {
            **binding,
            "driver_id": "unitree-g1",
            "driver_name": "Unitree G1 Bundle",
            "robot_id": "unitree-g1",
            "actuation_enabled": live,
            "capability_digest": capability_digest(mode),
        },
    }


def live_activation_contract() -> dict:
    """Review-visible two-step authority boundary outside the 60 Hz path."""

    return {
        "acquire": "awaiting_confirmation",
        "driver_contact_before_confirmation": False,
        "confirmation_body": {
            "confirm_live_actuation": True,
            "profile_id": PROFILE_ID,
        },
        "after_confirmation": [
            "pinned_driver_status",
            "durable_authority_guard",
            "prepare_live",
            "core_heartbeat",
        ],
        "automatic_confirmation": False,
    }


def runtime_evidence_contract(mode: str) -> dict:
    """Fields rendered by the Core console for lag and output diagnosis."""

    if mode not in {"shadow", "live"}:
        raise ValueError("mode must be shadow or live")
    return {
        "identity": {"driver_id": "unitree-g1", "robot_id": "unitree-g1"},
        "joint_vectors": {"target": 10, "measured": 10},
        "joint_error_evidence": "max_abs_error_rad",
        "sequence_evidence": (
            "last_published_sequence" if mode == "live" else "last_would_apply_sequence"
        ),
        "hardware_weight": "finite_0_to_1" if mode == "live" else None,
        "transport": [
            "rtc_rtt_ms",
            "pose_age_ms",
            "frame_rate_hz",
            "frames_received",
            "frames_rejected",
            "sequence_gaps",
            "mailbox_replacements",
        ],
        "latency_ms": [
            "receive_to_admit",
            "mailbox_wait",
            "ik",
            "adapter_apply",
            "robot_follow",
        ],
    }


def core_console_action() -> dict:
    """Return the real navigation action; it never calls Driver/MCP directly."""

    return {
        "id": "open_core_teleop_console",
        "type": "navigate",
        "method": "GET",
        "path": "/teleop.html",
        "label": "打开遥操控制台",
        "minimum_control_role": "operator",
        "direct_driver_call": False,
    }


def readiness_contract() -> dict:
    return {
        "card_status": "offline-green",
        "offline_contract_matrix": True,
        "linux_arm64_cold_ik_image": False,
        "integrated_quest_g1_live": False,
        "may_claim_live_ready": False,
    }
