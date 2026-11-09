# -*- coding: utf-8 -*-
"""
Ramord Link - Dynamic Network Management Module
Auto-detects network interfaces, manages NetworkManager shared profile,
and monitors client devices.
"""

from __future__ import annotations
import os
import re
import subprocess
from pathlib import Path

CONNECTION_NAME = "win-share"
SHARE_IP = "192.168.50.1"
DHCP_RANGE = "192.168.50.10 - 192.168.50.254"
SMB_SHARE_NAME = "Genel"


def run_cmd(cmd: list[str], timeout: int = 20) -> subprocess.CompletedProcess:
    env = dict(os.environ, LC_ALL="C", LANG="C")
    try:
        return subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False, env=env
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(cmd, 1, "", str(exc))


def detect_interfaces() -> tuple[list[str], list[str]]:
    """
    Scans system network interfaces.
    Returns: (list_of_ethernet_ifaces, list_of_wifi_ifaces)
    """
    ethernet_ifaces: list[str] = []
    wifi_ifaces: list[str] = []

    # 1. Check via nmcli if available
    res = run_cmd(["nmcli", "-t", "-f", "DEVICE,TYPE", "device"])
    if res.returncode == 0:
        for line in res.stdout.splitlines():
            if ":" not in line:
                continue
            dev, dev_type = line.split(":", 1)
            dev = dev.strip()
            dev_type = dev_type.strip().lower()
            if dev == "lo":
                continue
            if dev_type == "ethernet" and dev not in ethernet_ifaces:
                ethernet_ifaces.append(dev)
            elif dev_type == "wifi" and dev not in wifi_ifaces:
                wifi_ifaces.append(dev)

    # 2. Fallback via /sys/class/net
    net_path = Path("/sys/class/net")
    if net_path.exists():
        for iface_dir in net_path.iterdir():
            name = iface_dir.name
            if name == "lo" or name.startswith("virbr") or name.startswith("docker"):
                continue
            # If wireless directory exists inside interface folder
            if (iface_dir / "wireless").exists() or (iface_dir / "phy80211").exists():
                if name not in wifi_ifaces:
                    wifi_ifaces.append(name)
            else:
                if name.startswith(("eno", "eth", "enp", "enx", "usb")) and name not in ethernet_ifaces:
                    ethernet_ifaces.append(name)

    # Ensure eno1 / wlan0 priority if present
    if "eno1" in ethernet_ifaces:
        ethernet_ifaces.remove("eno1")
        ethernet_ifaces.insert(0, "eno1")
    if "wlan0" in wifi_ifaces:
        wifi_ifaces.remove("wlan0")
        wifi_ifaces.insert(0, "wlan0")

    return ethernet_ifaces, wifi_ifaces


def get_default_ethernet() -> str:
    eths, _ = detect_interfaces()
    return eths[0] if eths else "eno1"


def get_default_wifi() -> str:
    _, wifis = detect_interfaces()
    return wifis[0] if wifis else "wlan0"


def read_sys_file(path: str) -> str:
    try:
        return Path(path).read_text().strip()
    except OSError:
        return ""


def is_carrier_up(iface: str) -> bool:
    return read_sys_file(f"/sys/class/net/{iface}/carrier") == "1"


def get_link_speed(iface: str) -> str:
    speed = read_sys_file(f"/sys/class/net/{iface}/speed")
    if speed.isdigit() and int(speed) > 0:
        return f"{int(speed)} Mbps"
    return "-"


def get_iface_ip(iface: str) -> str:
    out = run_cmd(["ip", "-4", "-brief", "addr", "show", iface]).stdout
    for part in out.split():
        if "/" in part and part[0].isdigit():
            return part
    return "-"


def get_active_connection(iface: str) -> str | None:
    out = run_cmd(["nmcli", "-t", "-f", "GENERAL.CONNECTION", "device", "show", iface]).stdout
    for line in out.splitlines():
        if line.startswith("GENERAL.CONNECTION:"):
            val = line.split(":", 1)[1].strip()
            return val or None
    return None


def is_sharing_active(iface: str) -> bool:
    return get_active_connection(iface) == CONNECTION_NAME


def get_wifi_info(wifi_iface: str) -> tuple[str, str]:
    ssid = "-"
    out = run_cmd(["nmcli", "-t", "-f", "ACTIVE,SSID", "device", "wifi"]).stdout
    for line in out.splitlines():
        if line.startswith("yes:"):
            ssid = line.split(":", 1)[1]
            break
    ip = "-"
    out = run_cmd(["nmcli", "-t", "-f", "IP4.ADDRESS", "device", "show", wifi_iface]).stdout
    for line in out.splitlines():
        if line.startswith("IP4.ADDRESS"):
            ip = line.split(":", 1)[1].split("/")[0]
            break
    return ssid, ip


def get_connected_clients(iface: str) -> list[tuple[str, str]]:
    out = run_cmd(["ip", "neigh", "show", "dev", iface]).stdout
    found: list[tuple[str, str]] = []
    for line in out.splitlines():
        match = re.search(r"^(\d+\.\d+\.\d+\.\d+)\s+lladdr\s+([0-9a-f:]+)\s+(\S+)", line)
        if not match:
            continue
        ip, mac, state = match.groups()
        if state.upper() == "FAILED":
            continue
        found.append((ip, mac.upper()))
    return found


link_speed = get_link_speed
iface_address = get_iface_ip
sharing_active = is_sharing_active
wifi_info = lambda wifi_iface=None: get_wifi_info(wifi_iface or get_default_wifi())
clients = get_connected_clients



def connection_profile_exists() -> bool:
    out = run_cmd(["nmcli", "-t", "-f", "NAME", "connection", "show"]).stdout
    return CONNECTION_NAME in out.splitlines()


def enable_sharing(iface: str) -> tuple[bool, str]:
    if not connection_profile_exists():
        add_res = run_cmd(
            [
                "nmcli", "connection", "add", "type", "ethernet",
                "ifname", iface, "con-name", CONNECTION_NAME,
                "ipv4.method", "shared", "ipv4.addresses", f"{SHARE_IP}/24",
                "ipv6.method", "ignore",
            ]
        )
        if add_res.returncode != 0:
            return False, add_res.stderr or add_res.stdout

    # Update interface if it changed
    run_cmd(["nmcli", "connection", "modify", CONNECTION_NAME, "connection.interface-name", iface])

    up_res = run_cmd(["nmcli", "--wait", "15", "connection", "up", CONNECTION_NAME], timeout=25)
    if up_res.returncode != 0:
        return False, up_res.stderr or up_res.stdout
    return True, ""


def disable_sharing() -> tuple[bool, str]:
    down_res = run_cmd(["nmcli", "--wait", "10", "connection", "down", CONNECTION_NAME], timeout=20)
    if down_res.returncode != 0:
        return False, down_res.stderr or down_res.stdout
    return True, ""


def is_samba_running() -> bool:
    res = run_cmd(["systemctl", "is-active", "smb"])
    if res.stdout.strip() == "active":
        return True
    res2 = run_cmd(["systemctl", "is-active", "smbd"])
    return res2.stdout.strip() == "active"
