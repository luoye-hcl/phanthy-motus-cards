#!/usr/bin/env python3
"""Execute the real G1 Driver descriptor/status -> Core projection matrix.

This is an offline producer/consumer check.  The Driver subprocess uses its
test fakes for LowState, IK and the arm publisher; it never opens DDS or talks
to a robot.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

CARD_ROOT = Path(__file__).resolve().parents[1]

DRIVER_PROBE = r'''
import json
import time

from teleop.adapter import G1ControllerPoseMapper, G1DualArmAdapter
from teleop.descriptor import tool_definitions
from teleop.hardware import G1ArmSdkPort
from teleop.runtime import G1TeleopRuntime
from tests.helpers import FakeIkSolver, FakeLowStateReader, frame, session
from tests.test_teleop_live import FakeCrc, FakeLowCommand, FakePublisher


class BadIk(FakeIkSolver):
    def solve(self, *args):
        raise RuntimeError("matrix_ik_failure")


def make(mode, *, ik=None, pose_timeout_ms=1000, command_timeout_s=0.5):
    lowstate = FakeLowStateReader()
    port = None
    if mode == "live":
        port = G1ArmSdkPort(
            lowstate,
            control_hz=250,
            ramp_seconds=0,
            release_seconds=0,
            velocity_limit_rad_s=30,
            command_timeout_s=command_timeout_s,
            publisher=FakePublisher(),
            message_factory=FakeLowCommand,
            crc=FakeCrc(),
        )
    adapter = G1DualArmAdapter(
        mode=mode,
        pose_mapper=G1ControllerPoseMapper(),
        ik_solver=ik or FakeIkSolver(),
        low_state_reader=lowstate,
        arm_sdk=port,
    )
    runtime = G1TeleopRuntime(
        mode=mode,
        adapter=adapter,
        driver_id="unitree-g1",
        robot_id="unitree-g1",
        auto_watchdog=False,
        pose_timeout_ms=pose_timeout_ms,
        dispatch_io_timeout_ms=150,
        dispatch_ack_timeout_ms=200,
    )
    return runtime, lowstate


def wait_status(runtime, predicate, timeout=1.0):
    deadline = time.monotonic() + timeout
    last = None
    while time.monotonic() < deadline:
        last = runtime.status()
        if predicate(last):
            return last
        time.sleep(0.002)
    raise RuntimeError(f"matrix wait timed out: {last!r}")


def lifecycle(mode):
    runtime, _ = make(mode)
    identity = session()
    sequence_key = (
        "last_published_sequence" if mode == "live"
        else "last_would_apply_sequence"
    )
    try:
        states = {
            "idle": runtime.status(),
            "prepared": runtime.prepare(mode, identity),
        }
        runtime.submit_frame(
            frame(runtime, identity, sequence=1, clutch_sequence=1, deadman=False),
            source="cards-contract-matrix",
        )
        runtime.submit_frame(
            frame(runtime, identity, sequence=2, clutch_sequence=2, deadman=True),
            source="cards-contract-matrix",
        )
        states["active"] = wait_status(
            runtime,
            lambda status: status["dispatch"].get(sequence_key) == 2,
        )
        runtime.submit_frame(
            frame(runtime, identity, sequence=3, clutch_sequence=2, deadman=False),
            source="cards-contract-matrix",
        )
        states["hold"] = wait_status(
            runtime,
            lambda status: (
                status["state"] == "hold"
                and status["dispatch"]["stop_acknowledged"]
            ),
        )
        states["paused"] = runtime.pause({"boot_id": runtime.boot_id, **identity})
        states["released"] = runtime.release({"boot_id": runtime.boot_id, **identity})
        return states
    finally:
        runtime.close()


def shadow_fault():
    runtime, _ = make("shadow", ik=BadIk())
    identity = session()
    try:
        runtime.prepare("shadow", identity)
        runtime.submit_frame(
            frame(runtime, identity, sequence=1, clutch_sequence=1, deadman=False),
            source="cards-contract-matrix",
        )
        runtime.submit_frame(
            frame(runtime, identity, sequence=2, clutch_sequence=2, deadman=True),
            source="cards-contract-matrix",
        )
        return wait_status(runtime, lambda status: status["state"] == "fault")
    finally:
        runtime.close()


def live_fault():
    runtime, lowstate = make("live")
    identity = session()
    try:
        runtime.prepare("live", identity)
        runtime.submit_frame(
            frame(runtime, identity, sequence=1, clutch_sequence=1, deadman=False),
            source="cards-contract-matrix",
        )
        runtime.submit_frame(
            frame(runtime, identity, sequence=2, clutch_sequence=2, deadman=True),
            source="cards-contract-matrix",
        )
        wait_status(
            runtime,
            lambda status: status["dispatch"].get("last_published_sequence") == 2,
        )
        lowstate.mode_machine = 3
        return wait_status(runtime, lambda status: status["state"] == "fault")
    finally:
        runtime.close()


def live_intent_expired():
    runtime, _ = make("live", pose_timeout_ms=100, command_timeout_s=0.5)
    identity = session()
    try:
        runtime.prepare("live", identity)
        runtime.submit_frame(
            frame(runtime, identity, sequence=1, clutch_sequence=1, deadman=False),
            source="cards-contract-matrix",
        )
        runtime.submit_frame(
            frame(runtime, identity, sequence=2, clutch_sequence=2, deadman=True),
            source="cards-contract-matrix",
        )
        return wait_status(
            runtime,
            lambda status: (
                status["state"] == "hold"
                and status["reason"] == "intent_expired"
                and status["dispatch"]["stop_acknowledged"]
            ),
        )
    finally:
        runtime.close()


result = {}
for mode in ("shadow", "live"):
    result[mode] = {
        "tool": tool_definitions(
            mode=mode,
            driver_id="unitree-g1",
            robot_id="unitree-g1",
        )[0],
        "states": lifecycle(mode),
    }
result["shadow"]["states"]["fault"] = shadow_fault()
result["live"]["states"]["fault"] = live_fault()
result["live"]["states"]["intent_expired"] = live_intent_expired()
print(json.dumps(result, allow_nan=False, separators=(",", ":")))
'''

EXPECTED = {
    "shadow": {
        "idle": ("idle", None),
        "prepared": ("prepared_shadow", None),
        "active": ("active_shadow", None),
        "hold": ("hold", "deadman_released"),
        "paused": ("paused", "operator_pause"),
        "released": ("released", "operator_release"),
        "fault": ("fault", "dispatch_fault"),
    },
    "live": {
        "idle": ("idle", None),
        "prepared": ("prepared_live", None),
        "active": ("active_live", None),
        "hold": ("hold", "deadman_released"),
        "paused": ("paused", "operator_pause"),
        "released": ("released", "operator_release"),
        "fault": ("fault", "dispatch_fault"),
        "intent_expired": ("hold", "intent_expired"),
    },
}

TRANSPORT_FIELDS = {
    "rtc_rtt_ms",
    "pose_age_ms",
    "frame_rate_hz",
    "frames_received",
    "frames_rejected",
    "sequence_gaps",
    "mailbox_replacements",
}
LATENCY_STAGES = {
    "receive_to_admit",
    "mailbox_wait",
    "ik",
    "adapter_apply",
    "robot_follow",
}
LATENCY_SUMMARY_FIELDS = {"last", "p50", "p95", "p99", "count"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_card_impl():
    path = CARD_ROOT / "impl" / "teleop_session.py"
    spec = importlib.util.spec_from_file_location("g1_card_contract", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_driver_probe(driver_root: Path) -> dict:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(driver_root)
    result = subprocess.run(
        [sys.executable, "-c", DRIVER_PROBE],
        cwd=driver_root,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(f"Driver probe failed:\n{result.stderr}")
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--driver-root", required=True, type=Path)
    parser.add_argument("--core-root", required=True, type=Path)
    args = parser.parse_args()
    driver_root = args.driver_root.resolve()
    core_root = args.core_root.resolve()
    require((driver_root / "teleop" / "descriptor.py").is_file(), "invalid G1 Driver root")
    require((core_root / "src" / "teleop" / "contracts.py").is_file(), "invalid Core root")

    matrix = run_driver_probe(driver_root)
    database_root = tempfile.TemporaryDirectory(prefix="teleop-contract-matrix-")
    os.environ["DB_PATH"] = str(Path(database_root.name) / "data.db")
    sys.path.insert(0, str(core_root / "src"))
    from teleop.contracts import project_teleop_descriptor
    from teleop.service import _project_driver_snapshot

    metadata = json.loads((CARD_ROOT / "metadata.json").read_text())
    card_impl = load_card_impl()
    projected_count = 0

    for mode in ("shadow", "live"):
        tool = matrix[mode]["tool"]
        expected_tool = card_impl.teleop_session_tool_definition(mode)
        require(tool == expected_tool, f"{mode} Driver descriptor differs from Card excerpt")
        if mode == "shadow":
            require(tool == metadata["mcp_tool"], "Shadow metadata differs from Driver")
        descriptor = tool["x-teleop"]
        projected_descriptor = project_teleop_descriptor(
            tool,
            expected_driver_id="unitree-g1",
        )
        require(projected_descriptor["robot_id"] == "unitree-g1", f"{mode} robot id")
        require(projected_descriptor["profile_id"] == card_impl.PROFILE_ID, f"{mode} profile")

        for label, raw in matrix[mode]["states"].items():
            expected_state, expected_reason = EXPECTED[mode][label]
            require(raw["state"] == expected_state, f"{mode}/{label} state")
            require(raw["reason"] == expected_reason, f"{mode}/{label} reason")
            projected, _ = _project_driver_snapshot(
                raw,
                driver_id="unitree-g1",
                robot_id="unitree-g1",
                capability_digest=descriptor["capability_digest"],
                action="status",
                expected_mode=mode,
                expected_profile_id=descriptor["profile_id"],
                expected_capabilities=descriptor["capabilities"],
            )
            require(projected["state"] == expected_state, f"{mode}/{label} projected state")
            require(projected["reason"] == expected_reason, f"{mode}/{label} projected reason")

            output = projected["output"]
            require(len(output["target_joint_positions_rad"]) == 10, f"{mode}/{label} target shape")
            require(len(output["measured_joint_positions_rad"]) == 10, f"{mode}/{label} measured shape")
            require(isinstance(output["max_abs_error_rad"], (int, float)), f"{mode}/{label} error")
            dispatch = projected["dispatch"]
            diagnostics = projected["diagnostics"]
            require(set(diagnostics["transport"]) == TRANSPORT_FIELDS, f"{mode}/{label} transport")
            require(set(diagnostics["latency_ms"]) == LATENCY_STAGES, f"{mode}/{label} latency")
            for stage, summary in diagnostics["latency_ms"].items():
                require(set(summary) == LATENCY_SUMMARY_FIELDS, f"{mode}/{label}/{stage} summary")

            if mode == "shadow":
                require(output["hardware_output"] is False, f"{mode}/{label} hardware")
                require(output["arm_sdk_weight"] is None, f"{mode}/{label} weight")
                require("last_published_sequence" not in dispatch, f"{mode}/{label} sequence")
            else:
                require(output["hardware_output"] is True, f"{mode}/{label} hardware")
                require(isinstance(output["arm_sdk_weight"], (int, float)), f"{mode}/{label} weight")
                require("last_would_apply_sequence" not in dispatch, f"{mode}/{label} sequence")
                if expected_state in {"idle", "prepared_live", "hold", "paused", "released", "fault"}:
                    require(output["arm_sdk_weight"] == 0.0, f"{mode}/{label} safe weight")

            if expected_state == "fault":
                require(dispatch["fault_code"], f"{mode}/{label} fault code")
                require(dispatch["fault_code"] == output["fault_reason"], f"{mode}/{label} fault match")
            projected_count += 1

    console_action = metadata["operator_actions"][0]
    require(console_action == card_impl.core_console_action(), "console action differs")
    require(console_action["direct_driver_call"] is False, "console action calls Driver")
    require((core_root / "web" / "teleop.html").is_file(), "Core teleop console missing")
    index = (core_root / "web" / "index.html").read_text()
    require('href="/teleop.html"' in index, "Core dashboard console link missing")

    print(
        json.dumps(
            {
                "result": "PASS",
                "descriptors": 2,
                "projected_statuses": projected_count,
                "joint_shape": "10/10",
                "latency_stages": sorted(LATENCY_STAGES),
                "console_action": "GET /teleop.html",
                "hardware": "fake-only; no DDS/device connection",
            },
            sort_keys=True,
        )
    )
    database_root.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
