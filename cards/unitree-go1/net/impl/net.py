# -*- coding: utf-8 -*-
# 摘录自 luoye-hcl/go1-driver:unitree/go1/plugins/mt_state.py
# 仅为审核理解 net 卡如何产出返回值。以源仓库为准,不保证独立运行。

from plugins.mt_base import MtStateCard, now_ms


class NetCard(MtStateCard):
    """网络健康(驱动增值卡):主机名/IPv4/Wi-Fi 信号。联调时无线易掉,这张卡让大模型/人
    一眼看清链路。纯系统读(不经硬件)→ 不套硬件状态新鲜度抑制,始终可读。"""
    CARD = "net"; CONTROL_LEVEL = "ANY"
    TOPIC = "state/net"; FMT = "data/json"; HZ = 0.5
    DESC = "Go1 网络健康 —— 主机名/IPv4/Wi-Fi 信号强度(联调掉线排查用)。"

    def _produce(self):
        # 系统级读取,不依赖硬件帧 → 不套 MtStateCard 的 fresh 抑制
        d = self._payload()
        d["timestamp_ms"] = now_ms()
        d["control_level"] = self._ctrl.control_level
        return d

    def _payload(self):
        import socket
        out = {"available": True, "hostname": None, "ipv4": None, "wifi": {"available": False}}
        try:
            out["hostname"] = socket.gethostname()
        except Exception:  # noqa: BLE001
            pass
        out["ipv4"] = self._primary_ipv4()
        out["wifi"] = self._wifi_stats()
        return out

    @staticmethod
    def _primary_ipv4():
        import socket
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))    # 不真发包,只用于选默认出口网卡
            return s.getsockname()[0]
        except Exception:  # noqa: BLE001
            return None
        finally:
            if s is not None:
                try:
                    s.close()
                except Exception:  # noqa: BLE001
                    pass

    @staticmethod
    def _wifi_stats():
        # Linux(狗)读 /proc/net/wireless;Mac/无该文件 → available:false(诚实标注)
        try:
            with open("/proc/net/wireless") as f:
                lines = f.read().splitlines()
        except Exception:  # noqa: BLE001
            return {"available": False, "reason": "无 /proc/net/wireless(非 Linux 或无无线网卡)"}
        for ln in lines[2:]:
            parts = ln.split()
            if len(parts) >= 4 and parts[0].endswith(":"):
                iface = parts[0].rstrip(":")
                try:
                    link = float(parts[2].rstrip("."))
                    level = float(parts[3].rstrip("."))
                except (ValueError, IndexError):
                    link, level = None, None
                return {"available": True, "iface": iface,
                        "link_quality": link, "signal_dbm": level}
        return {"available": False, "reason": "无活动无线网卡"}

# 基类 get_tool 声明 readOnly:true + topic_out /{ns}/state/net → core 只出数据流、不给执行按钮。
