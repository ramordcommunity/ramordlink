# -*- coding: utf-8 -*-
"""
Ramord Link - Deskflow KVM Mouse & Keyboard Sharing Manager
"""

from __future__ import annotations
import os
import subprocess
from pathlib import Path

DESKFLOW_DIR = Path.home() / ".config/Deskflow"
DESKFLOW_CONF = DESKFLOW_DIR / "Deskflow.conf"
DESKFLOW_SERVER_CONF = DESKFLOW_DIR / "server.conf"
DESKFLOW_LOG = DESKFLOW_DIR / "deskflow.log"
DESKFLOW_SCREEN = "ramord"
CLIENT_SCREEN = "windows"
DESKFLOW_PORT = 24800

EDGES = {
    "left": "left",
    "right": "right",
    "up": "up",
    "down": "down",
}
OPPOSITE = {"left": "right", "right": "left", "up": "down", "down": "up"}


def is_deskflow_installed() -> bool:
    res = subprocess.run(["sh", "-c", "command -v deskflow-core"], capture_output=True, text=True)
    return res.returncode == 0


def is_client_connected() -> bool:
    try:
        res = subprocess.run(
            ["ss", "-tnH", "state", "established"], capture_output=True, text=True, check=False
        )
        needle = f":{DESKFLOW_PORT}"
        return any(needle in line for line in res.stdout.splitlines())
    except Exception:
        return False


def write_deskflow_config(edge: str, listen_all: bool = False, share_ip: str = "192.168.50.1") -> None:
    edge = edge if edge in EDGES else "right"
    opposite = OPPOSITE[edge]
    listen_ip = "0.0.0.0" if listen_all else share_ip
    DESKFLOW_DIR.mkdir(parents=True, exist_ok=True)
    
    DESKFLOW_CONF.write_text(
        "[core]\n"
        "coreMode=2\n"
        f"computerName={DESKFLOW_SCREEN}\n"
        f"interface={listen_ip}\n"
        "preventSleep=true\n"
        "\n"
        "[log]\n"
        "level=Info\n"
        "toFile=true\n"
        f"file={DESKFLOW_LOG}\n"
        "\n"
        "[security]\n"
        "tlsEnabled=false\n"
        "checkPeerFingerprints=false\n"
        "\n"
        f"[computer_{DESKFLOW_SCREEN}]\n"
        f"name={DESKFLOW_SCREEN}\n"
        "\n"
        f"[computer_{CLIENT_SCREEN}]\n"
        f"name={CLIENT_SCREEN}\n"
        "\n"
        "[server]\n"
        "externalConfig=true\n"
        f"externalConfigFile={DESKFLOW_SERVER_CONF}\n"
        "enableClipboard=true\n"
        "switchDelay=250\n"
    )
    
    DESKFLOW_SERVER_CONF.write_text(
        "section: links\n"
        f"\t{DESKFLOW_SCREEN}:\n"
        f"\t\t{edge} = {CLIENT_SCREEN}\n"
        f"\t{CLIENT_SCREEN}:\n"
        f"\t\t{opposite} = {DESKFLOW_SCREEN}\n"
        "end\n"
        "\n"
        "section: options\n"
        "\tclipboardSharing = true\n"
        "\tswitchDelay = 250\n"
        "end\n"
    )
