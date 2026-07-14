# 卡片库网站验证方案 + 入库门槛收紧 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 给卡片库加一套通用的、可自测的网站验证方案(权威文档 + 前置检查脚本 + 证据模板),并把入库门槛收紧为"只有网站验过 + MT 验收的 accepted 卡才能合入 main"。

**Architecture:** 方案 A —— 一份权威文档 `docs/WEBSITE_VERIFICATION.md` 是唯一事实源;`tools/preflight.py` 自动化"机器能判"的前置检查(驱动 MCP 契约 + 传感器真数据);标准/流程/PR 模板只加指针指向文档,不重复内容。

**Tech Stack:** Python 3(纯标准库:`urllib`/`json`/`argparse`/`http.server` 仅测试用);Markdown 文档。

**仓库:** `phanthy-motus-cards`(本计划所有路径相对该仓库根)。设计见 `docs/superpowers/specs/2026-07-15-card-website-verification-design.md`。

## Global Constraints

- **纯标准库**:`preflight.py` 与其测试不得引入任何第三方依赖(提交者随手可跑)。
- **Python 3.7+ 兼容**:所有 `.py` 顶部加 `from __future__ import annotations`。
- **MCP 线格式**(与驱动 `tests/call.sh` 一致):端点 `POST http://<host>:<port>/mcp`;`tools/list` → `result.tools[]`;`tools/call {params:{name, arguments}}` → `result.content[0].text`(卡返回 JSON 串)。
- **中文**:文档与注释用中文,与仓库现有风格一致。
- **卫生**:仓库不入库截图等二进制;证据用链接/PR 附图。metadata.json 必须合法 JSON。
- **状态门槛**:`draft` / `offline-green` 不合 main;仅 `accepted`(网站验过+MT验收+证据齐)可合。

---

### Task 1: `tools/preflight.py` 前置检查脚本(TDD)

**Files:**
- Create: `tools/preflight.py`
- Test: `tools/test_preflight.py`

**Interfaces:**
- Produces(供文档/PR 模板引用的 CLI):`python3 tools/preflight.py <卡目录> --host <IP> [--port 15704]`,`exit 0`=机器判的全绿,非 0=有 FAIL。
- Produces(供测试 import 的函数):
  - `load_card_meta(card_dir) -> dict`(无/非法 metadata → 抛 `ValueError`)
  - `rpc(host, port, method, params=None, timeout=5) -> dict`(传输失败抛 `RuntimeError`)
  - `find_tool(tools, name) -> dict|None`
  - `check_descriptor(tool, meta) -> list[(level, msg)]`
  - `check_sensor_read(host, port, meta) -> list[(level, msg)]`
  - `run_checks(card_dir, host, port) -> (results:list[(level,msg)], exit_code:int)`
  - `main(argv=None) -> int`
  - 常量 `PASS="PASS"`, `WARN="WARN"`, `FAIL="FAIL"`

- [ ] **Step 1: 写失败测试** `tools/test_preflight.py`

```python
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
```

- [ ] **Step 2: 跑测试确认失败**

Run: `cd tools && python3 -m pytest test_preflight.py -q` (或 `python3 test_preflight.py`)
Expected: FAIL —— `ModuleNotFoundError: No module named 'preflight'`(还没建脚本)。

- [ ] **Step 3: 写最小实现** `tools/preflight.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/preflight.py — 卡片入库前置检查(纯标准库,不需要第三方)。

用法:
    python3 tools/preflight.py <卡目录> --host <驱动IP> [--port 15704]
例:
    python3 tools/preflight.py cards/unitree-go1/net --host 10.100.130.4

查的是"驱动 MCP 层契约 + 传感器真数据"。查不了网站可见性/数据流/MT 验收——
那三步机器判不了,必须人到 core 网站按 docs/WEBSITE_VERIFICATION.md 走。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"


def load_card_meta(card_dir):
    """读 <card_dir>/metadata.json;不存在/非法 → 抛 ValueError(带人话)。"""
    path = os.path.join(card_dir, "metadata.json")
    if not os.path.isfile(path):
        raise ValueError("找不到 %s —— 卡目录对吗?" % path)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except ValueError as e:
        raise ValueError("%s 不是合法 JSON:%s" % (path, e))


def rpc(host, port, method, params=None, timeout=5):
    """发一个 JSON-RPC 到驱动 /mcp,返回解析后的 dict。传输失败抛 RuntimeError。"""
    url = "http://%s:%d/mcp" % (host, port)
    body = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params is not None:
        body["params"] = params
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        raise RuntimeError("连不上驱动 %s(%s)—— 驱动没在跑或地址/端口错。"
                           "先按驱动仓库把驱动起起来再重试。" % (url, e))


def find_tool(tools, name):
    for t in tools or []:
        if t.get("name") == name:
            return t
    return None


def check_descriptor(tool, meta):
    """比对 tools/list 描述符与 metadata.mcp_tool。返回 [(level, msg)]。"""
    out = []
    mt = meta.get("mcp_tool", {})
    if tool.get("type") == mt.get("type"):
        out.append((PASS, "type 一致:%s" % tool.get("type")))
    else:
        out.append((FAIL, "type 不一致:实机 %s vs metadata %s"
                    % (tool.get("type"), mt.get("type"))))
    if bool(tool.get("readOnly")) == bool(mt.get("readOnly")):
        out.append((PASS, "readOnly 一致:%s" % bool(tool.get("readOnly"))))
    else:
        out.append((FAIL, "readOnly 不一致:实机 %s vs metadata %s"
                    % (tool.get("readOnly"), mt.get("readOnly"))))
    live = sorted(x.get("topic") for x in (tool.get("topic_out") or []))
    want = sorted(x.get("topic") for x in (mt.get("topic_out") or []))
    if live == want:
        out.append((PASS, "topic_out 一致:%s" % live))
    else:
        out.append((FAIL, "topic_out 不一致:实机 %s vs metadata %s" % (live, want)))
    return out


def _parse_call_payload(resp):
    """从 tools/call 响应取卡返回 dict(result.content[0].text 是 JSON 串)。"""
    result = resp.get("result", {})
    content = result.get("content") or []
    if not content:
        raise ValueError("tools/call 响应无 content:%s" % json.dumps(resp)[:200])
    return json.loads(content[0].get("text", ""))


def check_sensor_read(host, port, meta):
    """对传感器卡发 read,校真数据。返回 [(level, msg)]。"""
    name = meta["mcp_tool"]["name"]
    try:
        resp = rpc(host, port, "tools/call",
                   {"name": name, "arguments": {"action": "read"}})
        payload = _parse_call_payload(resp)
    except Exception as e:  # noqa: BLE001
        return [(FAIL, "read 调用/解析失败:%s" % e)]
    if not isinstance(payload, dict):
        return [(FAIL, "read 返回不是对象:%r" % payload)]
    if payload.get("ok") is False or payload.get("code") == "NO_FEEDBACK":
        return [(WARN, "read 返回无数据(%s)—— 后端可能离线/无新帧,不是真数据。"
                 "先让驱动接真机再验。" % payload.get("code", "?"))]
    out = []
    fields = list((meta.get("payload_fields") or {}).keys())
    top = list(dict.fromkeys(f.split(".")[0] for f in fields))  # net 有 wifi.xxx,取顶层去重
    missing = [f for f in top if f not in payload]
    if missing:
        out.append((WARN, "read 返回缺声明字段:%s(实返回键:%s)"
                    % (missing, sorted(payload.keys()))))
    else:
        out.append((PASS, "read 返回含全部声明的顶层字段"))
    if payload.get("offline") is True:
        out.append((WARN, "read 返回 offline:true —— 不是真机数据,先让驱动接真机。"))
    else:
        out.append((PASS, "read 返回非 offline(疑似真数据)"))
    return out


def run_checks(card_dir, host, port):
    """跑全部检查,返回 (results, exit_code)。"""
    results = []
    meta = load_card_meta(card_dir)
    name = meta.get("mcp_tool", {}).get("name")
    dir_name = os.path.basename(os.path.normpath(card_dir))
    if name == dir_name:
        results.append((PASS, "目录名 == 工具名:%s" % name))
    else:
        results.append((FAIL, "目录名 %s != mcp_tool.name %s" % (dir_name, name)))
    resp = rpc(host, port, "tools/list")
    tools = resp.get("result", {}).get("tools", [])
    tool = find_tool(tools, name)
    if tool is None:
        results.append((FAIL, "驱动 tools/list 里没有 '%s' —— 卡没注册/没起。" % name))
        return results, 1
    results.append((PASS, "驱动 tools/list 含 '%s'" % name))
    results += check_descriptor(tool, meta)
    if meta.get("category") == "sensor":
        results += check_sensor_read(host, port, meta)
    else:
        results.append((PASS, "执行器卡:脚本不自动执行动作(会让狗动)。"
                        "请人到 core 网站点'执行'按钮看真实效果。"))
        if not tool.get("inputSchema"):
            results.append((WARN, "descriptor 无 inputSchema —— 执行器卡应声明入参。"))
    code = 1 if any(lvl == FAIL for lvl, _ in results) else 0
    return results, code


def main(argv=None):
    ap = argparse.ArgumentParser(description="卡片入库前置检查(查驱动 MCP 契约+真数据)")
    ap.add_argument("card_dir", help="卡目录,如 cards/unitree-go1/net")
    ap.add_argument("--host", required=True, help="驱动 IP,如 10.100.130.4")
    ap.add_argument("--port", type=int, default=15704, help="驱动 MCP 端口(默认 15704)")
    args = ap.parse_args(argv)
    try:
        results, code = run_checks(args.card_dir, args.host, args.port)
    except (ValueError, RuntimeError) as e:
        print("FAIL  %s" % e)
        return 1
    for lvl, msg in results:
        print("%-5s %s" % (lvl, msg))
    n_fail = sum(1 for lvl, _ in results if lvl == FAIL)
    n_warn = sum(1 for lvl, _ in results if lvl == WARN)
    print("\n汇总:%d FAIL / %d WARN / %d 项" % (n_fail, n_warn, len(results)))
    print("—— preflight 只查驱动 MCP 契约+真数据;网站可见性/数据流/MT 验收机器判不了,"
          "必须人按 docs/WEBSITE_VERIFICATION.md 上网站走。")
    print("✓ 机器判的检查通过,可上网站做人眼验证。" if code == 0
          else "✗ 有 FAIL,先修再上网站。")
    return code


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 跑测试确认通过**

Run: `cd tools && python3 test_preflight.py`
Expected: `Ran 9 tests ... OK`

- [ ] **Step 5: 提交**

```bash
git add tools/preflight.py tools/test_preflight.py
git commit -m "feat(tools): 卡片入库前置检查脚本 preflight.py + 单测(mock MCP)"
```

---

### Task 2: `docs/WEBSITE_VERIFICATION.md` 通用网站验证方案

**Files:**
- Create: `docs/WEBSITE_VERIFICATION.md`

**Interfaces:**
- Consumes:Task 1 的 `tools/preflight.py` CLI(在 §1 引用其用法)。
- Produces:被 `SUBMISSION_STANDARD.md` / `SUBMISSION_PROCESS.md` / PR 模板引用的权威流程文档。

- [ ] **Step 1: 建文档(完整内容)**

写入 `docs/WEBSITE_VERIFICATION.md`:

````markdown
# 网站验证方案(WEBSITE VERIFICATION)

一张卡要升到 `accepted`(唯一能合入 main 的状态),必须在**公司 core 网站**上被证明"功能真的实现了",并经 **MT 验收通过**。本文是通用、可自测的验证流程。

> 本文从"**卡已注册进 core、网站能打开**"开始。环境怎么拉起(部署驱动 / 让路 / 转发器 `--ipc=host` / 断网恢复)**不在本文范围**——见你所在驱动仓库的部署文档(如 Go1:`luoye-hcl/go1-driver`)。
>
> ⚠️ 不依赖网站"智能控制"大模型链路(该链路目前因 core 侧 `decision_core` 问题不可用)。验证一律走**手动点执行 / 看数据流**。

## §0 前提清单(逐项确认)

- [ ] 机器人上电、可连
- [ ] 驱动已部署并**注册进 core**(设备在网站上可见)
- [ ] 数据转发器已在跑(如 Go1 的 ROS republisher,**带 `--ipc=host`**)——DATA STREAMS 出数据的前提
- [ ] core 网站能打开(如 `https://<core-ip>:15678`)

任一不满足,先回驱动仓库解决,别急着往下。

## §1 自动前置检查(机器先判)

跑前置脚本,把"机器能判"的先跑绿,再上网站费人力:

```
python3 tools/preflight.py <卡目录> --host <驱动IP> [--port 15704]
```

例:`python3 tools/preflight.py cards/unitree-go1/net --host 10.100.130.4`

- 全绿(`exit 0`)→ 卡已注册、MCP 契约与 `metadata.json` 一致、传感器卡 `read` 返真数据 → 进 §2。
- 有 `FAIL` → 先修(卡没注册/契约不符/连不上驱动)。
- `WARN`(如后端离线、`offline:true`、`NO_FEEDBACK`)→ 说明驱动没接真机,先接真机再验。

> preflight **不能**替代下面的网站步骤——可见性 / 数据流 / 执行效果 / MT 验收,机器判不了,必须人上网站。

## §2 网站"看得到"

打开 core 网站 → 在设备下找到这张卡。确认:名称、描述、类型(sensor/actuator)、控制等级(ANY/HIGHLEVEL/LOWLEVEL)与 `metadata.json` **一致**。截图留证(卡可见)。

## §3 网站"验功能"(分卡型)

**传感器卡(sensor)**
- 在 DATA STREAMS(数据流)面板找到该卡的 topic,确认**数据在跳动**。
- **制造一个真实变化**证明不是伪造:如动一下狗看 IMU/里程值随之变、遮挡/触碰改变读数。
- 截图留证(数据流 + 变化前后)。

**执行器卡(actuator)**
- ⚠️ 安全前置:场地空旷、狗已站稳、随时能发急停 `damp`;让狗动前口头提醒在场的人。
- 在网站上点该卡的"**执行**"按钮发一个动作 → 观察机器人产生**对应真实效果**(或配套状态卡的值随之变化)。
- 截图/录屏留证(执行 + 真实效果)。

## §4 留证

收集:①卡可见截图 ②功能实现截图(数据流 / 执行效果)③一段**真实返回 JSON**(传感器最好两态对比)④采集时间 / 环境 / 后端。

> 截图等二进制**不入库**(仓库禁无关大文件)。用链接(内网图床)或贴在 PR 里,`verification/accepted.md` 正文只留指针。

## §5 MT 验收

请 MT 在网站上确认该卡功能实现 → 记录**验收人 / 日期 / 结论**。这是升 `accepted` 的必要一步。

## §6 通过后

- 把上面证据按 `docs/CARD_TEMPLATE/verification/accepted.md` 模板写入卡的 `verification/accepted.md`。
- `metadata.json`:`status` 改 `accepted`、加 `accepted_date`、`version` 递增。
- `CHANGELOG.md` 加一条。
- 提 PR 请求合并(见 `SUBMISSION_PROCESS.md`)。未达 accepted 的卡,PR 标题加 `[pending-web]`,审核不予合并。
````

- [ ] **Step 2: 校验交叉指向**

Run: `grep -n "WEBSITE_VERIFICATION\|preflight.py\|CARD_TEMPLATE/verification" docs/WEBSITE_VERIFICATION.md`
Expected: 引用到 `tools/preflight.py` 与 `docs/CARD_TEMPLATE/verification/accepted.md`(后者在 Task 3 建);确认无断链笔误。

- [ ] **Step 3: 提交**

```bash
git add docs/WEBSITE_VERIFICATION.md
git commit -m "docs: 通用网站验证方案 WEBSITE_VERIFICATION.md"
```

---

### Task 3: accepted 证据模板

**Files:**
- Create: `docs/CARD_TEMPLATE/verification/accepted.md`

**Interfaces:**
- Consumes:被 `WEBSITE_VERIFICATION.md` §6 引用为"照此填"的模板。

- [ ] **Step 1: 建模板(完整内容)**

写入 `docs/CARD_TEMPLATE/verification/accepted.md`:

````markdown
# 验收证据 —— <卡名>

- 验收日期 / 验收人(MT):<YYYY-MM-DD> / <MT 验收人>
- 环境:狗地址 <ip> · 后端(factory / legged_sdk)· 驱动 commit <hash> · core 版本 <ver>
- preflight:<`python3 tools/preflight.py cards/<robot>/<card> --host <ip>` 全绿输出摘要,或贴关键几行>

## 网站验证证据
- 卡可见:<截图链接>(设备页看到该卡,名称/类型正确)
- 功能实现:<截图/录屏链接>(传感器=DATA STREAMS 数据流+变化前后;执行器=点执行后的真实效果)

## 离线测试
- <测试文件 + 结果摘要,如 `test_mt_ext.py ... 27 OK`>

## 实机真实数据样本
```json
{ "示例": "一段真实返回;传感器最好两态对比(如站立 vs 阻尼)" }
```

## MT 验收结论
- 通过 / 备注:<结论>
````

- [ ] **Step 2: 提交**

```bash
git add docs/CARD_TEMPLATE/verification/accepted.md
git commit -m "docs: 新增 accepted 证据模板 (CARD_TEMPLATE/verification)"
```

---

### Task 4: 标准 / 流程 / PR 模板 / README 挂接门槛与指针

**Files:**
- Modify: `docs/SUBMISSION_STANDARD.md`
- Modify: `docs/SUBMISSION_PROCESS.md`
- Modify: `.github/PULL_REQUEST_TEMPLATE.md`
- Modify: `README.md`

**Interfaces:**
- Consumes:`docs/WEBSITE_VERIFICATION.md`(Task 2)、`tools/preflight.py`(Task 1)、`docs/CARD_TEMPLATE/verification/accepted.md`(Task 3)。

- [ ] **Step 1: `SUBMISSION_STANDARD.md` —— 加"状态与入库门槛"节 + 改验证要求**

在文件末尾(自检清单之前)新增一节:

```markdown
## 8. 状态与入库门槛

| 状态 | 含义 | 能合入 main? |
|---|---|---|
| `draft` | 仅设计,未实现/未测 | ❌ |
| `offline-green` | 离线测试全绿(可含实机只读碎片) | ❌ 只能待分支/开着的 PR(标题加 `[pending-web]`) |
| `accepted` | 网站验证通过 + MT 验收通过 + 完整真实样本 + 证据齐 | ✅ 唯一可合 |

**只有 `accepted` 能合入 main。** 升 accepted 的完整流程见 [WEBSITE_VERIFICATION.md](WEBSITE_VERIFICATION.md):跑 `tools/preflight.py` → 网站看得到/点执行/看数据流 → 留证 → MT 验收。
```

把 §5 `verification/` 要求改为(在原"实机"条后补):

```markdown
- **accepted 卡另必须**:①网站验证证据(卡可见截图 + 数据流/执行效果截图,用链接不入库二进制)②MT 验收记录(人/日期/结论)③完整真实 JSON 样本。按 `docs/CARD_TEMPLATE/verification/accepted.md` 填。详见 [WEBSITE_VERIFICATION.md](WEBSITE_VERIFICATION.md)。
```

在自检清单末尾加两条:

```markdown
- [ ] `tools/preflight.py <卡目录> --host <ip>` 全绿(机器判的契约+真数据)
- [ ] accepted 卡:网站验证证据 + MT 验收记录齐(见 WEBSITE_VERIFICATION.md)
```

- [ ] **Step 2: `SUBMISSION_PROCESS.md` —— 插入网站验证步骤**

把 A 流程第 5、6、7 步之间改为(在"开 PR"后、"合并"前插入验证):

```markdown
5. **开 PR**(用 PR 模板),标题 `[<机器人>] add <卡片名>: <一句话>`;**未达 accepted 时标题加 `[pending-web]`**。
6. **更新 README 收录表**(加一行)——可在同 PR 里改。
7. **网站验证 + MT 验收(升 accepted 的必经)**:
   - 跑 `python3 tools/preflight.py cards/<机器人>/<卡片名> --host <驱动IP>`,全绿。
   - 按 [WEBSITE_VERIFICATION.md](WEBSITE_VERIFICATION.md) 在 core 网站验证功能(看得到 / 点执行 / 看数据流)。
   - 请 MT 验收;齐证据写入 `verification/accepted.md`,`metadata.status→accepted`。
8. 审核人对照提交标准检查 → **确认 `status==accepted` 且证据齐**后合并到 main。**offline-green 的 PR 不合并**(可开着协作)。
```

- [ ] **Step 3: `.github/PULL_REQUEST_TEMPLATE.md` —— 加网站验证区块**

在模板末尾追加:

```markdown
## 网站验证(升 accepted 必填;未达 accepted 请在标题加 `[pending-web]`,审核不予合并)

- preflight 输出(粘关键几行):
  ```
  <python3 tools/preflight.py cards/<robot>/<card> --host <ip> 的输出>
  ```
- 卡可见截图:<链接>
- 功能实现截图(数据流/执行效果):<链接>
- 实机真实样本:见 `verification/accepted.md`
- MT 验收人 / 日期 / 结论:<...>

## 自检清单
- [ ] `preflight.py` 全绿
- [ ] accepted 卡:网站证据 + MT 验收记录齐(见 docs/WEBSITE_VERIFICATION.md)
- [ ] 未达 accepted 已在 PR 标题加 `[pending-web]`
```

- [ ] **Step 4: `README.md` —— 补一句入库门槛**

在"已收录卡片"表的状态图例那行后补一句:

```markdown
> **入库门槛**:只有 `accepted`(网站验证 + MT 验收通过)的卡才合入 main;`offline-green` 卡的 PR 可开着(标 `[pending-web]`)但不合并。见 [docs/WEBSITE_VERIFICATION.md](docs/WEBSITE_VERIFICATION.md)。
```

- [ ] **Step 5: 校验无断链**

Run: `grep -rn "WEBSITE_VERIFICATION\|preflight\|pending-web\|CARD_TEMPLATE/verification" docs/ README.md .github/`
Expected: 四处文件都指向 `WEBSITE_VERIFICATION.md`;门槛表述一致(只有 accepted 合 main)。

- [ ] **Step 6: 提交**

```bash
git add docs/SUBMISSION_STANDARD.md docs/SUBMISSION_PROCESS.md .github/PULL_REQUEST_TEMPLATE.md README.md
git commit -m "docs: 入库门槛收紧为 accepted + 各处挂接网站验证方案指针"
```

---

## 收尾(非代码,记在计划里)

- pending 分支 `add/unitree-go1-readonly-verified-3cards`(fall_alarm/net/odometry,offline-green):其 PR 标题加 `[pending-web]`,不合并;待狗上电按 WEBSITE_VERIFICATION 验过 + MT 验收再升 accepted 合入。
- 网络:push/PR 受公司网 GitHub 限流影响,窗口开时再推。

## Self-Review

- **Spec 覆盖**:①状态模型/门槛→Task 4 Step1 + README;②WEBSITE_VERIFICATION 流程→Task 2;③preflight.py(线格式/检查项/边界/错误处理)→Task 1;④标准/流程/PR 改动→Task 4;⑤accepted 证据模板→Task 3;⑥pending 分支处置→收尾。无遗漏。
- **占位扫描**:模板文件里的 `<卡名>`/`<ip>` 是**有意填空**,非计划占位;其余步骤均含完整代码/文本/命令。
- **类型一致**:`run_checks`/`check_descriptor`/`check_sensor_read`/`load_card_meta`/`rpc`/`find_tool` 在 Task 1 接口块与实现、测试中签名一致;常量 `PASS/WARN/FAIL` 统一。
