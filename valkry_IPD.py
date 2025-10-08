#!/usr/bin/env python3
import json, re, argparse
from datetime import datetime, timedelta, timezone
from rich.console import Console
from rich.table import Table
from rich.text import Text

EVE_LOG = "/var/log/suricata/eve.json"

# --- Your IPs ---
Target_endpoint = "<yourIP>"
known_host  = {"<IP>"} #identified familiar endpoints
known_host = {"<IP>", "<IP>"} #identified familiar endpoints
known_host = {"<IP>"} #identified familiar endpoints
known_VPN = {"<IP>", "<IP>"} #identify your vpn IPs 

def label_ip(ip: str) -> str:
    if ip in MACS:    return "Mac-Local"
    if ip in KALIS:   return "Kali-Local"
    if ip in ROUTERS: return "Router"
    if ip in PROTONS: return "ProtonVPN"
    if ip.startswith("192.168."): return "Unknown-Local"
    return "Unknown"

def colorize_label(label: str) -> Text:
    colors = {
        "Target_endpoint": "green",
        "known_host1": "cyan",
        "known_host2": "yellow",
        "known_host3": "magenta",
        "Unknown-Local": "blue",
        "Unknown/suspicious": "red",
    }
    return Text(label, style=colors.get(label, "white"))

def parse_ts(ts: str):
    ts = ts.replace("Z", "+00:00")
    ts = re.sub(r'([+-]\d{2})(\d{2})$', r'\1:\2', ts)
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return None

def iter_inbound(beelink_ip: str, hours: int):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    with open(EVE_LOG, "r") as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get("event_type") != "flow":
                continue

            ts = parse_ts(e.get("timestamp",""))
            if not ts or ts < cutoff:
                continue

            src = e.get("src_ip"); dst = e.get("dest_ip")
            proto = e.get("proto"); dpt = e.get("dest_port")

            if not src or not dst:
                continue

            # INBOUND ONLY: traffic hitting Beelink
            if dst != beelink_ip:
                continue

            yield {
                "ts": ts,
                "ip": src,
                "label": label_ip(src),
                "proto": proto or "",
                "port": dpt if dpt is not None else "",
            }

def main():
    ap = argparse.ArgumentParser(description="Show inbound IPs hitting Beelink from Suricata eve.json")
    ap.add_argument("--dest-ip", default=BEELINK_IP, help="Beelink IP (default: 192.168.0.66)")
    ap.add_argument("--hours", type=int, default=24, help="Lookback window in hours (default: 24)")
    ap.add_argument("--count", type=int, default=100, help="Max rows to show (default: 100)")
    args = ap.parse_args()

    rows = list(iter_inbound(args.dest_ip, args.hours))
    rows.sort(key=lambda r: r["ts"], reverse=True)
    rows = rows[:args.count]

    table = Table(show_header=True, header_style="bold")
    table.add_column("Timestamp", style="cyan")
    table.add_column("IP", style="white")
    table.add_column("Label")  # <-- we’ll colorize manually per row
    table.add_column("Proto", justify="center")
    table.add_column("Port", justify="right")

    for r in rows:
        table.add_row(
            r["ts"].strftime("%Y-%m-%d %H:%M:%S"),
            r["ip"],
            colorize_label(r["label"]),
            r["proto"],
            str(r["port"]),
        )

    Console().print(table)

if __name__ == "__main__":
    main()
