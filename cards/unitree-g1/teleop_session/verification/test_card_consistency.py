from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

CARD_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = CARD_ROOT.parents[2]
SHADOW_DIGEST = "3a333966ddb1c146c3852e02e90b59825e6844d6fbd9937502741af3b96a0757"
LIVE_DIGEST = "016f7e83955ec2dd47333b5ae2c33c85c695b43d2d1cc93b4bbdcc4055bfda4c"
PROFILE_ID = "unitree_g1_23_dual_arm_controller_v1"
SOURCE_REVISION = "1afb292ef9b4d7a489024f59180268d9d13ce984"


def _load_impl():
    path = CARD_ROOT / "impl" / "teleop_session.py"
    spec = importlib.util.spec_from_file_location("unitree_g1_teleop_card", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UnitreeG1TeleopCardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metadata = json.loads((CARD_ROOT / "metadata.json").read_text())
        cls.card = (CARD_ROOT / "CARD.md").read_text()
        cls.source = (CARD_ROOT / "impl" / "source.md").read_text()
        cls.offline = (CARD_ROOT / "verification" / "offline.md").read_text()
        cls.changelog = (CARD_ROOT / "CHANGELOG.md").read_text()
        cls.impl = _load_impl()

    def test_shadow_metadata_is_an_exact_real_descriptor(self):
        self.assertEqual("teleop_session", self.metadata["card"])
        self.assertEqual("unitree-g1", self.metadata["robot"])
        self.assertEqual("actuator", self.metadata["category"])
        self.assertEqual("LOWLEVEL", self.metadata["control_level"])
        self.assertEqual("1.0.0", self.metadata["version"])
        self.assertEqual("offline-green", self.metadata["status"])
        self.assertEqual(SOURCE_REVISION, self.metadata["source"]["commit"])
        self.assertEqual(
            self.impl.teleop_session_tool_definition("shadow"),
            self.metadata["mcp_tool"],
        )

    def test_shadow_and_live_are_strict_mode_specific_contracts(self):
        self.assertEqual(SHADOW_DIGEST, self.impl.capability_digest("shadow"))
        self.assertEqual(LIVE_DIGEST, self.impl.capability_digest("live"))
        shadow = self.impl.teleop_session_tool_definition("shadow")
        live = self.impl.teleop_session_tool_definition("live")
        for descriptor in (shadow, live):
            x = descriptor["x-teleop"]
            self.assertEqual("unitree-g1", x["driver_id"])
            self.assertEqual("unitree-g1", x["robot_id"])
            self.assertEqual(PROFILE_ID, x["profile_id"])
            self.assertEqual(10, x["capabilities"]["outputs"]["dual_arm"]["joint_count"])
            self.assertFalse(x["capabilities"]["outputs"]["base"]["enabled"])
            self.assertFalse(x["capabilities"]["outputs"]["hands"]["enabled"])
        self.assertIn("prepare_shadow", shadow["inputSchema"]["properties"]["action"]["enum"])
        self.assertNotIn("prepare_live", shadow["inputSchema"]["properties"]["action"]["enum"])
        self.assertIn("prepare_live", live["inputSchema"]["properties"]["action"]["enum"])
        self.assertNotIn("prepare_shadow", live["inputSchema"]["properties"]["action"]["enum"])
        self.assertFalse(shadow["annotations"]["destructiveHint"])
        self.assertTrue(live["annotations"]["destructiveHint"])

    def test_metadata_variants_match_generated_contracts(self):
        for mode in ("shadow", "live"):
            tool = self.impl.teleop_session_tool_definition(mode)
            descriptor = tool["x-teleop"]
            variant = self.metadata["mode_variants"][mode]
            self.assertEqual(descriptor["protocol"], variant["protocol"])
            self.assertEqual(descriptor["dispatch_contract"], variant["dispatch_contract"])
            self.assertEqual(descriptor["actuation_enabled"], variant["actuation_enabled"])
            self.assertEqual(descriptor["capability_digest"], variant["capability_digest"])
            self.assertIn(
                variant["prepare_action"],
                tool["inputSchema"]["properties"]["action"]["enum"],
            )
        self.assertTrue(self.metadata["mode_variants"]["live"]["requires_explicit_core_confirmation"])

    def test_live_confirmation_and_runtime_evidence_are_visible(self):
        activation = self.impl.live_activation_contract()
        self.assertEqual("awaiting_confirmation", activation["acquire"])
        self.assertFalse(activation["driver_contact_before_confirmation"])
        self.assertFalse(activation["automatic_confirmation"])
        self.assertEqual(PROFILE_ID, activation["confirmation_body"]["profile_id"])
        for mode, sequence in (
            ("shadow", "last_would_apply_sequence"),
            ("live", "last_published_sequence"),
        ):
            evidence = self.impl.runtime_evidence_contract(mode)
            self.assertEqual({"target": 10, "measured": 10}, evidence["joint_vectors"])
            self.assertEqual("max_abs_error_rad", evidence["joint_error_evidence"])
            self.assertEqual(sequence, evidence["sequence_evidence"])
            self.assertIn("rtc_rtt_ms", evidence["transport"])
            self.assertIn("ik", evidence["latency_ms"])
            self.assertIn("robot_follow", evidence["latency_ms"])

    def test_console_action_and_status_projection_match_the_visible_core_contract(self):
        self.assertEqual(
            [self.impl.core_console_action()],
            self.metadata["operator_actions"],
        )
        action = self.metadata["operator_actions"][0]
        self.assertEqual("navigate", action["type"])
        self.assertEqual("GET", action["method"])
        self.assertEqual("/teleop.html", action["path"])
        self.assertFalse(action["direct_driver_call"])
        self.assertNotIn("session_id", action)
        self.assertNotIn("fence", action)

        projection = self.metadata["status_projection"]
        self.assertEqual(
            [
                "receive_to_admit",
                "mailbox_wait",
                "ik",
                "adapter_apply",
                "robot_follow",
            ],
            projection["latency_stages"],
        )
        self.assertEqual(
            "last_would_apply_sequence", projection["shadow_sequence_field"]
        )
        self.assertEqual("last_published_sequence", projection["live_sequence_field"])
        self.assertIn("output.target_joint_positions_rad", projection["output_fields"])
        self.assertIn("output.max_abs_error_rad", projection["output_fields"])
        self.assertEqual("fault", projection["observed_states"]["shadow"][-1])
        self.assertEqual("fault", projection["observed_states"]["live"][-1])

    def test_docs_state_single_owner_and_unverified_target_truthfully(self):
        for claim in (
            "唯一 `rt/arm_sdk` publisher",
            "base=false",
            "hands=false",
            "GET /teleop.html",
            "只进入 Core 控制台",
            "0.5 rad/s",
            "不会自动确认、自动重连或自动重新 Acquire",
            "尚非 `accepted` / `live-ready`",
            "不能冒充本集成 Driver 的验收结果",
            "client_kind=native_openxr",
            "launch_capture.sh --platform meta --resume",
            "launch_capture.sh --platform pico --resume",
            "无需在头显内打开 WebXR 页面",
            "Direct WebXR",
            "Meta/PICO `arm64-v8a` debug APK",
            "Quest 当前 ADB 为 `unauthorized`",
            "当前 G1 关机",
        ):
            with self.subTest(claim=claim):
                self.assertIn(claim, self.card)
        self.assertIn("clients/quest-capture-native", self.source)
        self.assertIn("app-meta-debug.apk", self.offline)
        self.assertIn("app-pico-debug.apk", self.offline)
        self.assertIn(
            "2eb14276da161b5945a0984dd2a691a69a3b898ed9ff1000871d9f843ed8a8c0",
            self.offline,
        )
        self.assertIn(
            "e6a713af5194cc9e6a9c2538056ada45a726dcb60db248315d63db0b5fdabbac",
            self.offline,
        )
        capture = self.metadata["native_capture"]
        self.assertEqual("0.2.0", capture["version_name"])
        self.assertEqual(2, capture["version_code"])
        self.assertEqual("arm64-v8a", capture["abi"])
        self.assertFalse(capture["artifacts"]["meta"]["pvr_app_type"])
        self.assertTrue(capture["artifacts"]["pico"]["pvr_app_type"])
        self.assertEqual(2410871, capture["artifacts"]["meta"]["bytes"])
        self.assertEqual(2411011, capture["artifacts"]["pico"]["bytes"])
        self.assertIn("PICO APK 尚未安装或运行", self.offline)
        for claim in (
            "unitree/g1/teleop/hardware.py:G1ArmSdkPort",
            "60 Hz Pose",
            "linux/arm64",
            "不能标记 `accepted` 或 `live-ready`",
        ):
            with self.subTest(claim=claim):
                self.assertIn(claim, self.source)
        readiness = self.impl.readiness_contract()
        self.assertFalse(readiness["linux_arm64_cold_ik_image"])
        self.assertFalse(readiness["integrated_quest_g1_live"])
        self.assertFalse(readiness["may_claim_live_ready"])

    def test_real_driver_descriptors_when_checkout_is_supplied(self):
        root_value = os.environ.get("PHANTHYMOTUS_DRIVER_G1_ROOT")
        if not root_value:
            self.skipTest("set PHANTHYMOTUS_DRIVER_G1_ROOT for producer comparison")
        driver_root = Path(root_value).resolve()
        probe = """
import json
from teleop.descriptor import tool_definitions
print(json.dumps({
    mode: tool_definitions(
        mode=mode,
        driver_id='unitree-g1',
        robot_id='unitree-g1',
    )[0]
    for mode in ('shadow', 'live')
}, sort_keys=True))
"""
        env = dict(os.environ)
        env["PYTHONPATH"] = str(driver_root)
        result = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=driver_root,
            env=env,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        actual = json.loads(result.stdout)
        self.assertEqual(self.metadata["mcp_tool"], actual["shadow"])
        self.assertEqual(self.impl.teleop_session_tool_definition("live"), actual["live"])

    def test_evidence_changelog_and_catalog_are_consistent(self):
        self.assertIn("688 passed", self.offline)
        self.assertIn("57 tests ... OK", self.offline)
        self.assertIn("108 passed", self.offline)
        self.assertIn("Ran 9 tests ... OK", self.offline)
        self.assertIn('"projected_statuses":15', self.offline)
        verification = self.metadata["verification"]
        self.assertEqual(
            {"passed": 57, "total": 57},
            verification["unitree_g1_tests"],
        )
        self.assertEqual(
            {
                "channel": "conda-forge",
                "channel_policy": "nodefaults",
                "python": "3.10",
                "pinocchio": "3.1.0",
                "casadi": "3.6.7",
                "numpy": "1.26.4",
            },
            verification["runtime_packaging"],
        )
        smoke = verification["ubuntu_x86_64_same_stack"]
        self.assertEqual("offline-pass", smoke["status"])
        self.assertEqual(30, smoke["solve_frames"])
        self.assertFalse(smoke["publisher_created"])
        self.assertEqual("not-built", verification["linux_arm64_cold_ik_image"])
        self.assertEqual(
            "apk-built-adb-unauthorized-g1-powered-off",
            verification["quest_g1_live"],
        )
        self.assertEqual(
            "apk-built-not-installed-or-run-g1-powered-off",
            verification["pico_g1_live"],
        )
        for claim in (
            "warm-up 约 `16.7 ms`",
            "`p50≈1.9 ms`",
            "`p95≈2.2 ms`",
            "`max≈2.18 ms`",
            "最大约 `1.5 mm`",
            "publisher_created=false",
            "不是 Docker 目标镜像构建、linux/arm64 证据",
        ):
            with self.subTest(claim=claim):
                self.assertIn(claim, self.offline)
        self.assertIn("## v1.0.0 — 2026-08-09", self.changelog)
        catalog = (REPO_ROOT / "README.md").read_text()
        self.assertIn("unitree-g1", catalog)
        self.assertIn("cards/unitree-g1/teleop_session/", catalog)

    def test_no_second_state_card_or_secret_material(self):
        self.assertFalse((CARD_ROOT.parent / "teleop_state").exists())
        forbidden = (
            "BEGIN " + "PRIVATE KEY",
            "MOTUS_DRIVER_" + "TOKEN=",
            "password" + "=",
        )
        for path in CARD_ROOT.rglob("*"):
            if (
                not path.is_file()
                or path == Path(__file__)
                or path.suffix not in {".md", ".json", ".py"}
            ):
                continue
            text = path.read_text()
            for value in forbidden:
                with self.subTest(path=path, value=value):
                    self.assertNotIn(value, text)


if __name__ == "__main__":
    unittest.main()
