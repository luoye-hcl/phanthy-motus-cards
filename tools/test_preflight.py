#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/test_preflight.py — preflight.py 单测(内建 mock MCP,不需要真狗)。"""
from __future__ import annotations

import json
import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

import preflight  # 同目录


class _MockMCP:
    """可编排响应的最小 MCP 服务:tools/list 返回给定 tools;tools/call 返回给定 payload。"""
    def __init__(self, tools, call_payload):
        self.tools = tools
        self.call_payload = call_payload
        self.httpd = HTTPServer(("127.0.0.1", 0), self._make_handler())
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def _make_handler(self):
        server = self
        class H(BaseHTTPRequestHandler):
            def log_message(self, *a):  # 静音
                pass
            def do_POST(self):
                n = int(self.headers.get("Content-Length", 0))
                req = json.loads(self.rfile.read(n).decode("utf-8"))
                method = req.get("method")
                if method == "tools/list":
                    result = {"tools": server.tools}
                elif method == "tools/call":
                    text = json.dumps(server.call_payload)
                    result = {"content": [{"type": "text", "text": text}]}
                else:
                    result = {}
                body = json.dumps({"jsonrpc": "2.0", "id": 1, "result": result}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)
        return H

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *a):
        self.httpd.shutdown()


def _write_card(tmp, meta):
    d = os.path.join(tmp, meta["mcp_tool"]["name"])
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f)
    return d


SENSOR_META = {
    "card": "net", "category": "sensor",
    "payload_fields": {"hostname": "x", "wifi.link_quality": "x"},
    "mcp_tool": {"name": "net", "type": "sensor", "readOnly": True,
                 "topic_out": [{"topic": "/{ns}/state/net", "format": "data/json"}]},
}
SENSOR_TOOL = {"name": "net", "type": "sensor", "readOnly": True,
               "topic_out": [{"topic": "/{ns}/state/net", "format": "data/json"}]}
ACTUATOR_META = {
    "card": "loco", "category": "actuator",
    "mcp_tool": {"name": "loco", "type": "actuator", "readOnly": False,
                 "inputSchema": {"type": "object", "properties": {"action": {}}},
                 "topic_out": []},
}
ACTUATOR_TOOL = {"name": "loco", "type": "actuator", "readOnly": False,
                 "inputSchema": {"type": "object", "properties": {"action": {}}},
                 "topic_out": []}


class TestDescriptor(unittest.TestCase):
    def test_match(self):
        res = preflight.check_descriptor(SENSOR_TOOL, SENSOR_META)
        self.assertTrue(all(l == preflight.PASS for l, _ in res))

    def test_type_mismatch(self):
        bad = dict(SENSOR_TOOL, type="actuator")
        res = preflight.check_descriptor(bad, SENSOR_META)
        self.assertTrue(any(l == preflight.FAIL for l, _ in res))

    def test_topic_mismatch(self):
        bad = dict(SENSOR_TOOL, topic_out=[{"topic": "/wrong"}])
        res = preflight.check_descriptor(bad, SENSOR_META)
        self.assertTrue(any(l == preflight.FAIL for l, _ in res))


class TestSensorRead(unittest.TestCase):
    def test_real_data(self):
        payload = {"hostname": "unitree5990", "wifi": {"link_quality": 85}, "offline": False}
        with _MockMCP([SENSOR_TOOL], payload) as m:
            res = preflight.check_sensor_read("127.0.0.1", m.port, SENSOR_META)
        self.assertFalse(any(l == preflight.FAIL for l, _ in res))
        self.assertTrue(any(l == preflight.PASS for l, _ in res))

    def test_offline_warns(self):
        payload = {"hostname": "x", "wifi": {}, "offline": True}
        with _MockMCP([SENSOR_TOOL], payload) as m:
            res = preflight.check_sensor_read("127.0.0.1", m.port, SENSOR_META)
        self.assertTrue(any(l == preflight.WARN for l, _ in res))

    def test_no_feedback_warns(self):
        payload = {"ok": False, "code": "NO_FEEDBACK", "message": "no fresh"}
        with _MockMCP([SENSOR_TOOL], payload) as m:
            res = preflight.check_sensor_read("127.0.0.1", m.port, SENSOR_META)
        self.assertTrue(any(l == preflight.WARN for l, _ in res))


class TestRunChecks(unittest.TestCase):
    def test_sensor_end_to_end_pass(self):
        payload = {"hostname": "x", "wifi": {"link_quality": 85}, "offline": False}
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_card(tmp, SENSOR_META)
            with _MockMCP([SENSOR_TOOL], payload) as m:
                _res, code = preflight.run_checks(d, "127.0.0.1", m.port)
        self.assertEqual(code, 0)

    def test_tool_not_registered_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_card(tmp, SENSOR_META)
            with _MockMCP([], None) as m:
                _res, code = preflight.run_checks(d, "127.0.0.1", m.port)
        self.assertEqual(code, 1)

    def test_actuator_not_executed(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = _write_card(tmp, ACTUATOR_META)
            with _MockMCP([ACTUATOR_TOOL], None) as m:
                _res, code = preflight.run_checks(d, "127.0.0.1", m.port)
        self.assertEqual(code, 0)

    def test_bad_metadata_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                preflight.load_card_meta(tmp)


if __name__ == "__main__":
    unittest.main()
