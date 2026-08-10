"""Review excerpt of the generic recording-only teleoperation Driver.

Source: 4paradigm/phanthymotus-driver@68f07c4fb367effca19ce46007b0bbafce158fa6

This module keeps the exact default ``teleop_session`` descriptor plus small,
pure review helpers.  It is not a deployable Driver and has no hardware path.
"""

SOURCE_REVISION = "68f07c4fb367effca19ce46007b0bbafce158fa6"
CAPABILITY_DIGEST = "0deb8aea9802bfd31b9e43df273ed79000ad7de7de9c1e024abd5da80583ae7e"
DISPATCH_CONTRACT = "motus.teleop.dispatch.recording.v1"
SIGNALING_PROTOCOL = "motus.teleop.webrtc-offer-answer.v1"


def teleop_session_tool_definition(
    driver_id="teleop-shadow-driver",
    driver_name="Generic Teleop Shadow Diagnostics",
    robot_id=None,
):
    """Return the exact default descriptor emitted by the pinned source."""

    identity = {
        "boot_id": {"type": "string", "format": "uuid"},
        "session_id": {"type": "string", "format": "uuid"},
        "epoch": {"type": "integer", "minimum": 1},
        "fence": {"type": "string", "minLength": 24},
    }
    actions = {
        "start": {
            "params": [],
            "description": "Passive lifecycle readiness check; never prepares a session",
        },
        "stop": {
            "params": [],
            "description": "Stop lifecycle and safely release the Shadow session",
        },
        "prepare_shadow": {
            "params": ["session_id", "epoch", "fence"],
            "description": "Install a new Core-issued epoch/fence for a Shadow session",
        },
        "heartbeat": {
            "params": list(identity),
            "description": "Renew the lease from authenticated Agent Core MCP only",
        },
        "pause": {
            "params": list(identity),
            "description": "Pause diagnostics and enter a non-resuming state",
        },
        "release": {
            "params": list(identity),
            "description": "Release the current fenced session",
        },
        "soft_stop": {
            "params": list(identity),
            "description": "Enter HOLD; no hardware action exists",
        },
        "status": {
            "params": [],
            "description": "Read the current session and transport diagnostics",
        },
        "submit_shadow_frame": {
            "params": ["frame"],
            "description": (
                "Submit one strict Frame v1 for diagnostics/replay; "
                "not a production high-rate path"
            ),
        },
    }
    return {
        "name": "teleop_session",
        "type": "actuator",
        "multiInstance": False,
        "description": (
            "Robot-free Quest/WebRTC Shadow diagnostics with a bounded "
            "would-apply/would-stop final-dispatch trace. It can never actuate "
            "hardware; only authenticated MCP heartbeat renews the lease."
        ),
        "annotations": {"destructiveHint": False, "idempotentHint": False},
        "inputSchema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "action": {"type": "string", "enum": list(actions)},
                **identity,
                "frame": {
                    "type": "object",
                    "description": "Strict Teleop Frame v1 object",
                },
            },
            "required": ["action"],
            "x-action-params": actions,
        },
        "x-teleop": {
            "protocol": "motus.teleop.shadow.v1",
            "driver_id": driver_id,
            "driver_name": driver_name,
            "robot_id": robot_id,
            "mode": "shadow",
            "actuation_enabled": False,
            "capability_digest": CAPABILITY_DIGEST,
            "dispatch_contract": DISPATCH_CONTRACT,
            "signaling": {
                "protocol": SIGNALING_PROTOCOL,
                "path": "/offer",
                "access": "authenticated-core-proxy-only",
            },
        },
    }


RTC_PRIVATE_AUTHORITY_FIELDS = frozenset(
    {"boot_id", "session_id", "epoch", "fence"}
)


def bind_browser_frame_for_review(wire_frame, peer_authority):
    """Show that browser data cannot override server-bound authority."""

    supplied_private = RTC_PRIVATE_AUTHORITY_FIELDS.intersection(wire_frame)
    if supplied_private:
        raise ValueError(
            f"browser RTC frame contains private authority: {sorted(supplied_private)}"
        )
    return {
        "boot_id": peer_authority["boot_id"],
        "session_id": peer_authority["session_id"],
        "epoch": peer_authority["epoch"],
        "fence": peer_authority["fence"],
        **wire_frame,
    }


def rtc_control_result_for_review(message_type):
    """Classify the control messages accepted by the recording transport."""

    if message_type in ("peer_ping", "status"):
        return {"ok": True, "read_only": True, "lease_renewed": False}
    if message_type == "heartbeat":
        return {"ok": False, "code": "rtc_cannot_renew_lease"}
    if message_type in ("pause", "soft_stop", "release"):
        return {"ok": False, "code": "rtc_control_requires_core"}
    return {"ok": False, "code": "invalid_control"}


def recording_final_dispatch_contract():
    """Describe observable recording evidence and the permanent zero-output boundary."""

    return {
        "contract": DISPATCH_CONTRACT,
        "kind": "recording",
        "hardware_output": False,
        "motion_mailbox_depth": 1,
        "stop_path": "non-droppable-acknowledged",
        "records": ["would_apply", "would_stop"],
    }
