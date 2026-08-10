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
EXPECTED_REVISION = "68f07c4fb367effca19ce46007b0bbafce158fa6"
EXPECTED_DIGEST = "0deb8aea9802bfd31b9e43df273ed79000ad7de7de9c1e024abd5da80583ae7e"


def _load_impl_module():
    path = CARD_ROOT / "impl" / "teleop_session.py"
    spec = importlib.util.spec_from_file_location("generic_shadow_card", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load implementation excerpt: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GenericShadowCardConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.metadata = json.loads((CARD_ROOT / "metadata.json").read_text())
        cls.card = (CARD_ROOT / "CARD.md").read_text()
        cls.source = (CARD_ROOT / "impl" / "source.md").read_text()
        cls.offline = (CARD_ROOT / "verification" / "offline.md").read_text()
        cls.changelog = (CARD_ROOT / "CHANGELOG.md").read_text()
        cls.impl = _load_impl_module()

    def test_metadata_is_the_pinned_default_descriptor(self):
        self.assertEqual("teleop_session", self.metadata["card"])
        self.assertEqual("generic-teleop-shadow", self.metadata["robot"])
        self.assertEqual("1.0.0", self.metadata["version"])
        self.assertEqual("offline-green", self.metadata["status"])
        self.assertEqual(EXPECTED_REVISION, self.metadata["source"]["commit"])
        descriptor = self.metadata["mcp_tool"]
        self.assertEqual(self.impl.teleop_session_tool_definition(), descriptor)
        x_teleop = descriptor["x-teleop"]
        self.assertEqual(EXPECTED_DIGEST, x_teleop["capability_digest"])
        self.assertEqual("shadow", x_teleop["mode"])
        self.assertFalse(x_teleop["actuation_enabled"])
        self.assertIsNone(x_teleop["robot_id"])
        self.assertEqual(
            "motus.teleop.dispatch.recording.v1",
            x_teleop["dispatch_contract"],
        )

    def test_browser_authority_and_rtc_control_remain_core_owned(self):
        authority = {
            "boot_id": "boot",
            "session_id": "session",
            "epoch": 4,
            "fence": "server-private-fence-value",
        }
        bound = self.impl.bind_browser_frame_for_review({"sequence": 9}, authority)
        self.assertEqual(authority["fence"], bound["fence"])
        with self.assertRaises(ValueError):
            self.impl.bind_browser_frame_for_review(
                {"sequence": 9, "fence": "browser-value"}, authority
            )
        self.assertTrue(self.impl.rtc_control_result_for_review("status")["read_only"])
        self.assertEqual(
            "rtc_cannot_renew_lease",
            self.impl.rtc_control_result_for_review("heartbeat")["code"],
        )
        self.assertEqual(
            "rtc_control_requires_core",
            self.impl.rtc_control_result_for_review("release")["code"],
        )

    def test_recording_contract_has_permanent_zero_hardware_output(self):
        dispatch = self.impl.recording_final_dispatch_contract()
        self.assertEqual("recording", dispatch["kind"])
        self.assertFalse(dispatch["hardware_output"])
        self.assertEqual(1, dispatch["motion_mailbox_depth"])
        self.assertEqual(["would_apply", "would_stop"], dispatch["records"])
        self.assertFalse(self.metadata["mcp_tool"]["annotations"]["destructiveHint"])

    def test_docs_are_generic_and_pin_only_the_driver_source(self):
        for text in (self.card, self.source, self.offline, self.changelog):
            self.assertIn(EXPECTED_REVISION, text)
        self.assertIn("adapter_io_stalled", self.offline)
        self.assertIn("100/100 PASS", self.offline)
        for claim in (
            "recording-only Shadow",
            "hardware_output=false",
            "robot_id=null",
            "rtc_cannot_renew_lease",
            "would_apply",
            "would_stop",
            "client_kind=native_openxr",
            "launch_capture.sh --platform meta --resume",
            "launch_capture.sh --platform pico --resume",
            "无需打开 WebXR 页面",
            "Direct WebXR",
            "Meta 与 PICO `arm64-v8a` debug APK 已在 macOS x86_64 主机构建成功",
            "Quest 当前 ADB 为 `unauthorized`",
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

        forbidden = (
            "unitree",
            "render_instances",
            "multi_instance_deployment",
            "unitree_go1_high_level",
            "dry_run_profile",
            "Core 提交",
            "Core SHA",
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

    def test_catalog_points_to_the_reference_card(self):
        catalog = (REPO_ROOT / "README.md").read_text()
        self.assertIn("generic-teleop-shadow", catalog)
        self.assertIn("cards/generic-teleop-shadow/teleop_session/", catalog)

    def test_real_driver_descriptor_when_checkout_is_supplied(self):
        driver_root_value = os.environ.get("PHANTHYMOTUS_DRIVER_ROOT")
        if not driver_root_value:
            self.skipTest("set PHANTHYMOTUS_DRIVER_ROOT for producer comparison")
        driver_root = Path(driver_root_value).resolve()
        probe = (
            "import json; "
            "from main import tool_definitions; "
            "print(json.dumps(tool_definitions()[0], sort_keys=True))"
        )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(driver_root / "generic" / "teleop_shadow")
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
        self.assertEqual(self.metadata["mcp_tool"], json.loads(result.stdout))


if __name__ == "__main__":
    unittest.main()
