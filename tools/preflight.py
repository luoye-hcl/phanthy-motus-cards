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
