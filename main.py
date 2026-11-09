# -*- coding: utf-8 -*-
"""
Ramord Link - Desktop Application GUI
A modern, multilingual (6 languages: tr, en, de, es, fr, it) bridge application
providing one-click internet sharing, KVM mouse/keyboard sharing, and local web file transfer.

Official Contact: ramordhelp@gmail.com
"""

from __future__ import annotations
import json
import os
import signal
import sys
import threading
import time
from pathlib import Path
from http.server import ThreadingHTTPServer

from PySide6.QtCore import (
    QEasingCurve,
    QProcess,
    QPropertyAnimation,
    QRectF,
    Qt,
    QTimer,
    QUrl,
    Property,
)
from PySide6.QtGui import (
    QAction,
    QColor,
    QDesktopServices,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from i18n import (
    LANGUAGES,
    detect_system_language,
    get_lang,
    set_lang,
    t,
)
from network import (
    CONNECTION_NAME,
    DHCP_RANGE,
    SHARE_IP,
    SMB_SHARE_NAME,
    clients,
    detect_interfaces,
    disable_sharing,
    enable_sharing,
    get_default_ethernet,
    get_default_wifi,
    iface_address,
    is_carrier_up,
    is_samba_running,
    link_speed,
    sharing_active,
    wifi_info,
)
from deskflow_mgr import (
    CLIENT_SCREEN,
    DESKFLOW_SCREEN,
    EDGES,
    is_client_connected,
    is_deskflow_installed,
    write_deskflow_config,
)
from file_server import (
    DEFAULT_SHARE_DIR,
    FILE_PORT,
    FileShareHandler,
)

# Configuration & paths
CONFIG_DIR = Path.home() / ".config/ramord-link"
SETTINGS_PATH = CONFIG_DIR / "settings.json"
AUTOSTART_PATH = Path.home() / ".config/autostart/ramord-link.desktop"
SMB_PATH = f"\\\\{SHARE_IP}\\{SMB_SHARE_NAME}"
ICON_PATH = Path.home() / ".local/share/icons/hicolor/scalable/apps/ramord-link.svg"

# Palette
BLUE = "#2563eb"
GREEN = "#10b981"
AMBER = "#f59e0b"
RED = "#ef4444"
BG = "#f4f6fb"
CARD_BG = "#ffffff"
CARD_BORDER = "#e2e8f0"
TEXT = "#0f172a"
DIM = "#64748b"


def load_settings() -> dict:
    try:
        data = json.loads(SETTINGS_PATH.read_text())
        if isinstance(data, dict):
            return data
    except (OSError, ValueError):
        pass
    return {}


def save_settings(data: dict) -> None:
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        SETTINGS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    except OSError:
        pass


def make_tray_icon(active: bool) -> QIcon:
    size = 64
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.Antialiasing)

    color = QColor(GREEN if active else DIM)

    # Wi-Fi broadcast ripples
    painter.setPen(Qt.NoPen)
    painter.setBrush(color)
    painter.drawEllipse(14, 38, 8, 8)
    for width, radius, alpha in ((5, 16, 230), (5, 26, 150)):
        pen = painter.pen()
        pen.setColor(QColor(color.red(), color.green(), color.blue(), alpha))
        pen.setWidth(width)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        rect = (32 - radius, 42 - radius, radius * 2, radius * 2)
        painter.drawArc(*rect, 45 * 16, 90 * 16)

    # Ethernet cable / display
    pen = painter.pen()
    pen.setColor(color)
    pen.setWidth(5)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)
    painter.drawRoundedRect(38, 34, 16, 18, 3, 3)
    painter.end()
    return QIcon(pm)


def make_feature_icon(kind: str, color: str, background: str) -> QPixmap:
    size = 44
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor(background))
    painter.drawRoundedRect(QRectF(0, 0, size, size), 13, 13)

    pen = QPen(QColor(color), 2.6)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.NoBrush)

    if kind == "mouse":
        painter.drawRoundedRect(QRectF(14, 9, 16, 26), 8, 8)
        painter.drawLine(22, 13, 22, 19)
    elif kind == "folder":
        path = QPainterPath()
        path.moveTo(10, 18)
        path.lineTo(18, 18)
        path.lineTo(21, 21)
        path.lineTo(34, 21)
        path.lineTo(34, 32)
        path.lineTo(10, 32)
        path.closeSubpath()
        painter.drawPath(path)
    else:
        painter.drawArc(QRectF(10, 12, 24, 24), 45 * 16, 90 * 16)
        painter.drawArc(QRectF(15, 17, 14, 14), 45 * 16, 90 * 16)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(color))
        painter.drawEllipse(QRectF(20, 31, 4, 4))

    painter.end()
    return pixmap


def add_shadow(widget: QWidget, blur: int = 28, y: int = 6, alpha: int = 20) -> None:
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(blur)
    effect.setOffset(0, y)
    effect.setColor(QColor(15, 23, 42, alpha))
    widget.setGraphicsEffect(effect)


class Switch(QAbstractButton):
    """Smooth, modern toggle switch."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(48, 28)
        self._knob = 0.0
        self._anim = QPropertyAnimation(self, b"knob", self)
        self._anim.setDuration(160)
        self._anim.setEasingCurve(QEasingCurve.InOutCubic)
        self.toggled.connect(self._animate)

    def _animate(self, checked: bool) -> None:
        self._anim.stop()
        self._anim.setStartValue(self._knob)
        self._anim.setEndValue(1.0 if checked else 0.0)
        self._anim.start()

    def set_state(self, checked: bool) -> None:
        self.blockSignals(True)
        self.setChecked(checked)
        self.blockSignals(False)
        self._anim.stop()
        self._knob = 1.0 if checked else 0.0
        self.update()

    def _get_knob(self) -> float:
        return self._knob

    def _set_knob(self, value: float) -> None:
        self._knob = value
        self.update()

    knob = Property(float, _get_knob, _set_knob)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect().adjusted(1, 1, -1, -1)
        if not self.isEnabled():
            track = QColor("#e2e8f0")
        else:
            track = QColor(GREEN if self.isChecked() else "#cbd5e1")
        painter.setPen(Qt.NoPen)
        painter.setBrush(track)
        painter.drawRoundedRect(QRectF(rect), rect.height() / 2, rect.height() / 2)
        diameter = rect.height() - 6
        x = rect.x() + 3 + (rect.width() - diameter - 6) * self._knob
        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(QRectF(x, rect.y() + 3, diameter, diameter))
        painter.end()


STYLE = f"""
QWidget {{
    background: {BG};
    color: {TEXT};
    font-family: "Noto Sans", "Segoe UI", sans-serif;
    font-size: 13px;
}}
QLabel, QCheckBox {{ background: transparent; }}
QFrame#card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 18px;
}}
QFrame#hero {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #eef4ff, stop:1 #f1fbf6);
    border: 1px solid #dbe7fb;
    border-radius: 20px;
}}
QLabel#title {{ font-size: 21px; font-weight: 800; color: {TEXT}; }}
QLabel#subtitle {{ color: {DIM}; font-size: 12px; }}
QLabel#state {{ font-size: 24px; font-weight: 800; }}
QLabel#sectionTitle {{ font-size: 16px; font-weight: 800; }}
QLabel#key {{ color: {DIM}; font-size: 12px; }}
QLabel#value {{ font-weight: 600; }}
QLabel#mono {{
    color: #334155;
    font-family: "JetBrains Mono", "DejaVu Sans Mono", monospace;
    font-size: 12px;
}}
QPushButton#toggle {{
    border: none; border-radius: 14px; padding: 16px;
    font-size: 16px; font-weight: 800; color: #ffffff;
    background: {BLUE};
}}
QPushButton#toggle:hover {{ background: #1d4ed8; }}
QPushButton#toggle:pressed {{ background: #1e40af; }}
QPushButton#toggle[off="true"] {{ background: #e2e8f0; color: #334155; }}
QPushButton#toggle[off="true"]:hover {{ background: #d6deea; }}
QPushButton#ghost {{
    background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-radius: 10px; padding: 9px 14px; color: {TEXT}; font-weight: 600;
}}
QPushButton#ghost:hover {{ background: #f8fafc; border-color: #cbd5e1; }}
QPushButton#soft {{
    background: #f2f6fc; border: 1px solid #e2e8f2;
    border-radius: 10px; padding: 10px 14px; color: #1e293b; font-weight: 600;
}}
QPushButton#soft:hover {{ background: #e8eff9; border-color: #cbd9ee; }}
QPushButton#help {{
    background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-radius: 12px; padding: 8px 13px; color: {DIM}; font-weight: 600;
}}
QPushButton#help:hover {{ color: {BLUE}; border-color: #bfdbfe; background: #f5f9ff; }}
QPushButton#edge {{
    background: #f8fafc; border: 1px solid {CARD_BORDER}; border-radius: 9px;
    padding: 8px 16px; color: {DIM}; font-weight: 700;
}}
QPushButton#edge:hover {{ background: #eef2f8; }}
QPushButton#edge[selected="true"] {{
    background: #e8f0ff; border-color: {BLUE}; color: {BLUE};
}}
QPushButton#disclosure {{
    background: transparent; border: none; color: {DIM};
    font-weight: 700; font-size: 12px; text-align: left; padding: 4px 2px;
}}
QPushButton#disclosure:hover {{ color: {TEXT}; }}
QComboBox {{
    background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-radius: 8px; padding: 4px 10px; min-width: 90px;
    font-weight: 600; color: {TEXT};
}}
QComboBox:hover {{ border-color: #cbd5e1; }}
QComboBox::drop-down {{ border: none; width: 18px; }}
QCheckBox {{ color: {DIM}; spacing: 8px; }}
QCheckBox::indicator {{
    width: 16px; height: 16px; border-radius: 5px;
    border: 1px solid #cbd5e1; background: #ffffff;
}}
QCheckBox::indicator:checked {{ background: {GREEN}; border-color: {GREEN}; }}
QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
QScrollBar::handle:vertical {{
    background: #cfd8e6; min-height: 32px; border-radius: 5px;
}}
QScrollBar::handle:vertical:hover {{ background: #b6c2d6; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}
QMenu {{
    background: {CARD_BG}; border: 1px solid {CARD_BORDER};
    border-radius: 10px; padding: 6px;
}}
QMenu::item {{ padding: 7px 18px; border-radius: 6px; }}
QMenu::item:selected {{ background: #eef4ff; }}
"""


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.quitting = False
        self.tray: QSystemTrayIcon | None = None
        self.busy = False
        self.settings = load_settings()

        # Initialize language: user preference or system auto-detect
        saved_lang = self.settings.get("language")
        if saved_lang in LANGUAGES:
            set_lang(saved_lang)
        else:
            set_lang(detect_system_language())

        # Network interface settings
        eth_ifaces, wifi_ifaces = detect_interfaces()
        self.eth_ifaces = eth_ifaces
        self.wifi_ifaces = wifi_ifaces

        saved_eth = self.settings.get("eth_iface")
        self.active_eth = saved_eth if saved_eth in eth_ifaces else get_default_ethernet()

        self.edge = self.settings.get("edge", "right")
        if self.edge not in EDGES:
            self.edge = "right"
        self.deskflow_output = ""

        # Deskflow server process
        self.deskflow = QProcess(self)
        self.deskflow.setProgram("deskflow-core")
        self.deskflow.setArguments(["server"])
        self.deskflow.setProcessChannelMode(QProcess.MergedChannels)
        self.deskflow.readyReadStandardOutput.connect(self._read_deskflow)
        self.deskflow.finished.connect(self._deskflow_finished)
        self.deskflow.errorOccurred.connect(self._deskflow_error)

        # File sharing server
        self.file_server: ThreadingHTTPServer | None = None
        self.files_dir = Path(self.settings.get("files_dir", str(DEFAULT_SHARE_DIR)))
        self.files_wanted = bool(self.settings.get("files_enabled", False))
        self.mouse_wanted = bool(self.settings.get("mouse_enabled", False))
        self.wifi_enabled = bool(self.settings.get("wifi_enabled", False))
        self.mouse_wifi = bool(self.settings.get("mouse_wifi", False))
        self._mouse_last_attempt = 0.0

        self.setWindowTitle(t("app_title"))
        self.setWindowIcon(make_tray_icon(True))
        self.setMinimumSize(540, 640)
        self.resize(580, 920)

        self._build_ui()
        self._build_tray()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000)
        self.refresh()

        if self.mouse_wanted and is_deskflow_installed() and sharing_active(self.active_eth):
            QTimer.singleShot(600, lambda: self.start_mouse(silent=True))
        if self.files_wanted and sharing_active(self.active_eth):
            QTimer.singleShot(900, lambda: self.start_files(silent=True))

    # ---------- UI Construction ----------

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        content = QWidget()
        content.setObjectName("content")
        root = QVBoxLayout(content)
        root.setContentsMargins(22, 20, 22, 24)
        root.setSpacing(14)

        # ---------- Header Bar ----------
        header = QHBoxLayout()
        header.setSpacing(12)
        logo = QLabel()
        logo.setPixmap(make_feature_icon("wifi", "#ffffff", BLUE))
        logo.setFixedSize(44, 44)

        header_text = QVBoxLayout()
        header_text.setSpacing(1)
        self.title_lbl = QLabel(t("app_title"))
        self.title_lbl.setObjectName("title")
        self.subtitle_lbl = QLabel(t("app_subtitle"))
        self.subtitle_lbl.setObjectName("subtitle")
        header_text.addWidget(self.title_lbl)
        header_text.addWidget(self.subtitle_lbl)

        # Language Switcher Dropdown
        self.lang_combo = QComboBox()
        self.lang_combo.setCursor(Qt.PointingHandCursor)
        for code, label in LANGUAGES.items():
            self.lang_combo.addItem(f"{code.upper()} - {label}", code)
        current_idx = list(LANGUAGES.keys()).index(get_lang())
        self.lang_combo.setCurrentIndex(current_idx)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)

        self.help_btn = QPushButton(t("btn_help"))
        self.help_btn.setObjectName("help")
        self.help_btn.setCursor(Qt.PointingHandCursor)
        self.help_btn.clicked.connect(self.show_help)

        header.addWidget(logo)
        header.addLayout(header_text)
        header.addStretch()
        header.addWidget(self.lang_combo)
        header.addWidget(self.help_btn)
        root.addLayout(header)

        # ---------- Hero (Main Sharing Toggle) ----------
        hero = QFrame()
        hero.setObjectName("hero")
        add_shadow(hero, blur=26, y=5, alpha=18)
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(20, 18, 20, 18)
        hero_layout.setSpacing(8)

        self.state_label = QLabel(t("state_off"))
        self.state_label.setObjectName("state")
        hero_layout.addWidget(self.state_label)

        self.hero_hint = QLabel(t("hero_hint_off"))
        self.hero_hint.setObjectName("subtitle")
        self.hero_hint.setWordWrap(True)
        hero_layout.addWidget(self.hero_hint)
        hero_layout.addSpacing(2)

        # Interface Selector Row inside Hero
        iface_row = QHBoxLayout()
        iface_row.setSpacing(8)
        self.iface_label = QLabel(t("lbl_select_iface"))
        self.iface_label.setObjectName("key")
        self.iface_combo = QComboBox()
        self._refresh_iface_combo()
        self.iface_combo.currentIndexChanged.connect(self._on_iface_changed)
        iface_row.addWidget(self.iface_label)
        iface_row.addWidget(self.iface_combo)
        iface_row.addStretch()
        hero_layout.addLayout(iface_row)

        self.toggle_btn = QPushButton(t("btn_enable"))
        self.toggle_btn.setObjectName("toggle")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle)
        hero_layout.addWidget(self.toggle_btn)

        root.addWidget(hero)

        # ---------- KVM (Mouse & Keyboard) ----------
        mouse_card = QFrame()
        mouse_card.setObjectName("card")
        add_shadow(mouse_card, blur=22, y=4, alpha=14)
        mouse_layout = QVBoxLayout(mouse_card)
        mouse_layout.setContentsMargins(18, 16, 18, 16)
        mouse_layout.setSpacing(12)

        mouse_top = QHBoxLayout()
        mouse_top.setSpacing(12)
        mouse_icon = QLabel()
        mouse_icon.setPixmap(make_feature_icon("mouse", BLUE, "#e8f0ff"))
        mouse_icon.setFixedSize(44, 44)
        mouse_text = QVBoxLayout()
        mouse_text.setSpacing(1)
        self.mouse_title = QLabel(t("card_mouse_title"))
        self.mouse_title.setObjectName("sectionTitle")
        self.mouse_status = QLabel(t("mouse_off"))
        self.mouse_status.setObjectName("subtitle")
        mouse_text.addWidget(self.mouse_title)
        mouse_text.addWidget(self.mouse_status)
        self.mouse_switch = Switch()
        self.mouse_switch.set_state(self.mouse_wanted)
        self.mouse_switch.toggled.connect(self.set_mouse_enabled)
        mouse_top.addWidget(mouse_icon)
        mouse_top.addLayout(mouse_text, 1)
        mouse_top.addWidget(self.mouse_switch, 0, Qt.AlignVCenter)
        mouse_layout.addLayout(mouse_top)

        self.edge_label = QLabel(t("edge_question"))
        self.edge_label.setObjectName("key")
        mouse_layout.addWidget(self.edge_label)

        edge_row = QHBoxLayout()
        edge_row.setSpacing(7)
        self.edge_buttons: dict[str, QPushButton] = {}
        for edge_key in EDGES:
            btn = QPushButton(t(f"edge_{edge_key}"))
            btn.setObjectName("edge")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _=False, e=edge_key: self.set_edge(e))
            edge_row.addWidget(btn)
            self.edge_buttons[edge_key] = btn
        mouse_layout.addLayout(edge_row)

        self.edge_hint = QLabel(t("edge_hint"))
        self.edge_hint.setObjectName("subtitle")
        self.edge_hint.setWordWrap(True)
        mouse_layout.addWidget(self.edge_hint)

        wifi_row = QHBoxLayout()
        wifi_row.setSpacing(12)
        wifi_text = QVBoxLayout()
        wifi_text.setSpacing(1)
        self.wifi_title = QLabel(t("wifi_access_title"))
        self.wifi_title.setStyleSheet(f"color: {TEXT}; font-weight: 600;")
        self.wifi_desc = QLabel(t("wifi_access_desc"))
        self.wifi_desc.setObjectName("subtitle")
        wifi_text.addWidget(self.wifi_title)
        wifi_text.addWidget(self.wifi_desc)
        self.mouse_wifi_switch = Switch()
        self.mouse_wifi_switch.set_state(self.mouse_wifi)
        self.mouse_wifi_switch.toggled.connect(self.set_mouse_wifi)
        wifi_row.addLayout(wifi_text, 1)
        wifi_row.addWidget(self.mouse_wifi_switch, 0, Qt.AlignVCenter)
        mouse_layout.addLayout(wifi_row)

        self.mouse_help = QPushButton(t("btn_show_win_setup"))
        self.mouse_help.setObjectName("soft")
        self.mouse_help.setCursor(Qt.PointingHandCursor)
        self.mouse_help.clicked.connect(self.show_mouse_help)
        mouse_layout.addWidget(self.mouse_help)

        root.addWidget(mouse_card)

        # ---------- Files (Web HTTP Transfer) ----------
        files_card = QFrame()
        files_card.setObjectName("card")
        add_shadow(files_card, blur=22, y=4, alpha=14)
        files_layout = QVBoxLayout(files_card)
        files_layout.setContentsMargins(18, 16, 18, 16)
        files_layout.setSpacing(12)

        files_top = QHBoxLayout()
        files_top.setSpacing(12)
        files_icon = QLabel()
        files_icon.setPixmap(make_feature_icon("folder", GREEN, "#e7f8f0"))
        files_icon.setFixedSize(44, 44)
        files_text = QVBoxLayout()
        files_text.setSpacing(1)
        self.files_title = QLabel(t("card_files_title"))
        self.files_title.setObjectName("sectionTitle")
        self.files_status = QLabel(t("files_off"))
        self.files_status.setObjectName("subtitle")
        files_text.addWidget(self.files_title)
        files_text.addWidget(self.files_status)
        self.files_switch = Switch()
        self.files_switch.set_state(self.files_wanted)
        self.files_switch.toggled.connect(self.set_files_enabled)
        files_top.addWidget(files_icon)
        files_top.addLayout(files_text, 1)
        files_top.addWidget(self.files_switch, 0, Qt.AlignVCenter)
        files_layout.addLayout(files_top)

        action_row = QHBoxLayout()
        action_row.setSpacing(8)
        self.open_btn = QPushButton(t("btn_open_folder"))
        self.open_btn.setObjectName("soft")
        self.open_btn.setCursor(Qt.PointingHandCursor)
        self.open_btn.clicked.connect(self.open_files_dir)
        self.copy_btn = QPushButton(t("btn_copy_address"))
        self.copy_btn.setObjectName("soft")
        self.copy_btn.setCursor(Qt.PointingHandCursor)
        self.copy_btn.clicked.connect(self.copy_files_url)
        action_row.addWidget(self.open_btn)
        action_row.addWidget(self.copy_btn)
        action_row.addStretch()
        files_layout.addLayout(action_row)

        wifi_files_row = QHBoxLayout()
        wifi_files_row.setSpacing(12)
        wifi_files_text = QVBoxLayout()
        wifi_files_text.setSpacing(1)
        self.wifi_files_title = QLabel(t("wifi_files_title"))
        self.wifi_files_title.setStyleSheet(f"color: {TEXT}; font-weight: 600;")
        self.wifi_files_desc = QLabel(t("wifi_files_desc"))
        self.wifi_files_desc.setObjectName("subtitle")
        wifi_files_text.addWidget(self.wifi_files_title)
        wifi_files_text.addWidget(self.wifi_files_desc)
        self.wifi_switch = Switch()
        self.wifi_switch.set_state(self.wifi_enabled)
        self.wifi_switch.toggled.connect(self.set_wifi_access)
        wifi_files_row.addLayout(wifi_files_text, 1)
        wifi_files_row.addWidget(self.wifi_switch, 0, Qt.AlignVCenter)
        files_layout.addLayout(wifi_files_row)

        root.addWidget(files_card)

        # ---------- Details Disclosure ----------
        self.details_btn = QPushButton(f"{t('details_title')}  ▾")
        self.details_btn.setObjectName("disclosure")
        self.details_btn.setCursor(Qt.PointingHandCursor)
        self.details_btn.clicked.connect(self.toggle_details)
        root.addWidget(self.details_btn)

        self.details = QFrame()
        self.details.setObjectName("card")
        details_layout = QVBoxLayout(self.details)
        details_layout.setContentsMargins(18, 14, 18, 14)
        details_layout.setSpacing(8)

        self.link_key, self.link_label = self._info_row(details_layout, t("info_ethernet"), "-")
        self.client_key, self.client_label = self._info_row(details_layout, t("info_client_pc"), t("no_clients"))
        self.wifi_key, self.wifi_label = self._info_row(details_layout, t("info_wifi"), "-")
        self.gateway_key, self.gateway_label = self._info_row(
            details_layout, t("info_gateway"), f"{SHARE_IP}  ·  DHCP {DHCP_RANGE}"
        )
        self.dir_key, self.dir_label = self._info_row(
            details_layout, t("info_folder"), self._pretty_dir(self.files_dir)
        )

        self.addresses_title = self._section_title(t("info_addresses"))
        details_layout.addWidget(self.addresses_title)

        self.cable_key, self.files_url, self.cable_copy_btn = self._endpoint_row(
            details_layout, t("addr_cable"), f"http://{SHARE_IP}:{FILE_PORT}", self.copy_files_url
        )
        self.wifi_addr_key, self.files_wifi_url, self.wifi_copy_btn = self._endpoint_row(
            details_layout, t("addr_wifi"), t("state_off"), self.copy_wifi_url
        )
        self.smb_addr_key, self.smb_path, self.smb_copy_btn = self._endpoint_row(
            details_layout, t("addr_smb"), SMB_PATH, self.copy_smb_path
        )
        self.details.setVisible(False)
        root.addWidget(self.details)

        # ---------- Footer Row ----------
        footer = QHBoxLayout()
        footer.setSpacing(8)
        self.autostart = QCheckBox(t("autostart"))
        self.autostart.setChecked(AUTOSTART_PATH.exists())
        self.autostart.toggled.connect(self.set_autostart)

        self.refresh_btn = QPushButton(t("btn_refresh"))
        self.refresh_btn.setObjectName("ghost")
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.clicked.connect(self.refresh)

        self.quit_btn = QPushButton(t("btn_quit"))
        self.quit_btn.setObjectName("ghost")
        self.quit_btn.setCursor(Qt.PointingHandCursor)
        self.quit_btn.clicked.connect(self.quit_app)

        footer.addWidget(self.autostart)
        footer.addStretch()
        footer.addWidget(self.refresh_btn)
        footer.addWidget(self.quit_btn)
        root.addLayout(footer)

        scroll.setWidget(content)
        outer.addWidget(scroll)

    def _refresh_iface_combo(self) -> None:
        self.iface_combo.blockSignals(True)
        self.iface_combo.clear()
        eth_ifaces, _ = detect_interfaces()
        self.eth_ifaces = eth_ifaces
        for dev in eth_ifaces:
            self.iface_combo.addItem(f"{dev} ({'Ethernet'})", dev)
        if not eth_ifaces:
            self.iface_combo.addItem(f"{self.active_eth} ({'Fallback'})", self.active_eth)

        idx = self.iface_combo.findData(self.active_eth)
        if idx >= 0:
            self.iface_combo.setCurrentIndex(idx)
        self.iface_combo.blockSignals(False)

    def _on_iface_changed(self) -> None:
        selected = self.iface_combo.currentData()
        if selected and selected != self.active_eth:
            self.active_eth = selected
            self.settings["eth_iface"] = selected
            save_settings(self.settings)
            self.refresh()

    def _info_row(self, layout: QVBoxLayout, key: str, value: str) -> tuple[QLabel, QLabel]:
        row = QHBoxLayout()
        key_label = QLabel(key)
        key_label.setObjectName("key")
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        row.addWidget(key_label)
        row.addStretch()
        row.addWidget(value_label)
        layout.addLayout(row)
        return key_label, value_label

    def _section_title(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("section")
        return label

    def _pretty_dir(self, path: Path) -> str:
        text = str(path)
        home = str(Path.home())
        if text == home:
            return "~"
        if text.startswith(home + os.sep):
            return "~" + text[len(home):]
        return text

    def _endpoint_row(
        self, layout: QVBoxLayout, key: str, value: str, callback
    ) -> tuple[QLabel, QLabel, QPushButton]:
        row = QHBoxLayout()
        key_label = QLabel(key)
        key_label.setObjectName("key")
        key_label.setMinimumWidth(44)
        value_label = QLabel(value)
        value_label.setObjectName("mono")
        value_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        copy_btn = QPushButton(t("btn_copy"))
        copy_btn.setObjectName("ghost")
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.clicked.connect(callback)
        row.addWidget(key_label)
        row.addWidget(value_label)
        row.addStretch()
        row.addWidget(copy_btn)
        layout.addLayout(row)
        return key_label, value_label, copy_btn

    def _build_tray(self) -> None:
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        self.tray = QSystemTrayIcon(make_tray_icon(False), self)
        self.tray.setToolTip(t("app_title"))
        menu = QMenu()
        self.tray_toggle = QAction(t("tray_enable"), self)
        self.tray_toggle.triggered.connect(self.toggle)
        self.tray_mouse = QAction(t("tray_mouse_enable"), self)
        self.tray_mouse.triggered.connect(self.toggle_mouse)
        self.tray_files = QAction(t("tray_files_enable"), self)
        self.tray_files.triggered.connect(self.toggle_files)
        self.tray_show = QAction(t("tray_show"), self)
        self.tray_show.triggered.connect(self.show_window)
        self.tray_quit = QAction(t("tray_quit"), self)
        self.tray_quit.triggered.connect(self.quit_app)

        menu.addAction(self.tray_toggle)
        menu.addAction(self.tray_mouse)
        menu.addAction(self.tray_files)
        menu.addAction(self.tray_show)
        menu.addSeparator()
        menu.addAction(self.tray_quit)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._tray_clicked)
        self.tray.show()

    def _tray_clicked(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_window()

    def _on_language_changed(self, index: int) -> None:
        lang_code = self.lang_combo.itemData(index)
        if lang_code and lang_code in LANGUAGES:
            set_lang(lang_code)
            self.settings["language"] = lang_code
            save_settings(self.settings)
            self._update_ui_texts()
            self.refresh()

    def _update_ui_texts(self) -> None:
        self.setWindowTitle(t("app_title"))
        self.title_lbl.setText(t("app_title"))
        self.subtitle_lbl.setText(t("app_subtitle"))
        self.help_btn.setText(t("btn_help"))
        self.iface_label.setText(t("lbl_select_iface"))
        self.mouse_title.setText(t("card_mouse_title"))
        self.edge_label.setText(t("edge_question"))
        for edge_key, btn in self.edge_buttons.items():
            btn.setText(t(f"edge_{edge_key}"))
        self.edge_hint.setText(t("edge_hint"))
        self.wifi_title.setText(t("wifi_access_title"))
        self.wifi_desc.setText(t("wifi_access_desc"))
        self.mouse_help.setText(t("btn_show_win_setup"))

        self.files_title.setText(t("card_files_title"))
        self.open_btn.setText(t("btn_open_folder"))
        self.copy_btn.setText(t("btn_copy_address"))
        self.wifi_files_title.setText(t("wifi_files_title"))
        self.wifi_files_desc.setText(t("wifi_files_desc"))

        vis = self.details.isVisible()
        self.details_btn.setText(f"{t('details_title')}  {'▴' if vis else '▾'}")
        self.link_key.setText(t("info_ethernet"))
        self.client_key.setText(t("info_client_pc"))
        self.wifi_key.setText(t("info_wifi"))
        self.gateway_key.setText(t("info_gateway"))
        self.dir_key.setText(t("info_folder"))
        self.addresses_title.setText(t("info_addresses"))

        self.cable_key.setText(t("addr_cable"))
        self.cable_copy_btn.setText(t("btn_copy"))
        self.wifi_addr_key.setText(t("addr_wifi"))
        self.wifi_copy_btn.setText(t("btn_copy"))
        self.smb_addr_key.setText(t("addr_smb"))
        self.smb_copy_btn.setText(t("btn_copy"))

        self.autostart.setText(t("autostart"))
        self.refresh_btn.setText(t("btn_refresh"))
        self.quit_btn.setText(t("btn_quit"))

        if self.tray:
            self.tray_show.setText(t("tray_show"))
            self.tray_quit.setText(t("tray_quit"))

    # ---------- Status Refresh ----------

    def refresh(self) -> None:
        active = sharing_active(self.active_eth)
        has_link = is_carrier_up(self.active_eth)

        self.state_label.setText(t("state_on") if active else t("state_off"))
        self.state_label.setStyleSheet(
            f"color: {GREEN if active else '#334155'};"
        )
        self.hero_hint.setText(t("hero_hint_on") if active else t("hero_hint_off"))

        self.toggle_btn.setText(t("btn_disable") if active else t("btn_enable"))
        self.toggle_btn.setProperty("off", not active)
        self.toggle_btn.style().unpolish(self.toggle_btn)
        self.toggle_btn.style().polish(self.toggle_btn)

        if has_link:
            spd = link_speed(self.active_eth)
            self.link_label.setText(f"{t('cable_connected')} · {spd}")
            self.link_label.setStyleSheet(f"color: {GREEN}; font-weight: 600;")
        else:
            self.link_label.setText(t("cable_disconnected"))
            self.link_label.setStyleSheet(f"color: {AMBER}; font-weight: 600;")

        found = clients(self.active_eth)
        if found:
            self.client_label.setText("  ·  ".join(ip for ip, _ in found))
        else:
            self.client_label.setText(t("no_clients"))

        ssid, ip = wifi_info()
        self.wifi_label.setText(f"{ssid}  ·  {ip}")
        self.gateway_label.setText(f"{SHARE_IP}  ·  DHCP {DHCP_RANGE}")
        self.dir_label.setText(self._pretty_dir(self.files_dir))

        # Deskflow status
        running = self.deskflow.state() == QProcess.Running
        connected = running and is_client_connected()
        self.mouse_switch.set_state(running or self.mouse_wanted)
        self.mouse_wifi_switch.set_state(self.mouse_wifi)
        if not is_deskflow_installed():
            mouse_text, mouse_color = t("mouse_not_installed"), RED
        elif connected:
            mouse_text, mouse_color = t("mouse_connected"), GREEN
        elif running:
            mouse_text, mouse_color = t("mouse_waiting"), AMBER
        elif self.mouse_wanted:
            mouse_text, mouse_color = t("mouse_waiting_sharing"), AMBER
        else:
            mouse_text, mouse_color = t("mouse_off"), DIM
        self.mouse_status.setText(mouse_text)
        self.mouse_status.setStyleSheet(f"color: {mouse_color}; font-weight: 600;")

        for edge_k, btn in self.edge_buttons.items():
            btn.setProperty("selected", edge_k == self.edge)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        if self.deskflow.state() == QProcess.Running and not active:
            self.stop_mouse(keep_wanted=True)
        if (
            self.mouse_wanted
            and self.deskflow.state() == QProcess.NotRunning
            and active
            and iface_address(self.active_eth) != "-"
            and is_deskflow_installed()
            and time.monotonic() - self._mouse_last_attempt > 5
        ):
            self._mouse_last_attempt = time.monotonic()
            self.start_mouse(silent=True)

        # Files status
        if self.file_server is not None and not active:
            self._close_file_server()
        if (
            self.files_wanted
            and self.file_server is None
            and active
            and iface_address(self.active_eth) != "-"
        ):
            self.start_files(silent=True)

        files_on = self.file_server is not None
        self.files_switch.set_state(files_on or self.files_wanted)
        self.wifi_switch.set_state(self.wifi_enabled)
        if files_on:
            files_text, files_color = t("files_active"), GREEN
        elif self.files_wanted:
            files_text, files_color = t("files_waiting_sharing"), AMBER
        else:
            files_text, files_color = t("files_off"), DIM
        self.files_status.setText(files_text)
        self.files_status.setStyleSheet(f"color: {files_color}; font-weight: 600;")

        if self.wifi_enabled:
            w_url = self.wifi_url()
            if w_url:
                self.files_wifi_url.setText(w_url)
                self.wifi_copy_btn.setEnabled(True)
            else:
                self.files_wifi_url.setText(t("state_off"))
                self.wifi_copy_btn.setEnabled(False)
        else:
            self.files_wifi_url.setText(t("state_off"))
            self.wifi_copy_btn.setEnabled(False)

        tooltip = f"{t('app_title')}: {t('state_on') if active else t('state_off')}"
        if self.tray:
            self.tray.setIcon(make_tray_icon(active))
            self.tray.setToolTip(tooltip)
            self.tray_toggle.setText(t("tray_disable") if active else t("tray_enable"))
            self.tray_mouse.setText(t("tray_mouse_disable") if running else t("tray_mouse_enable"))
            self.tray_files.setText(t("tray_files_disable") if files_on else t("tray_files_enable"))

        self.setWindowIcon(make_tray_icon(active))

    def toggle_details(self) -> None:
        visible = not self.details.isVisible()
        self.details.setVisible(visible)
        self.details_btn.setText(
            f"{t('details_title')}  {'▴' if visible else '▾'}"
        )

    def show_help(self) -> None:
        box = QMessageBox(self)
        box.setWindowTitle(t("btn_help"))
        box.setIcon(QMessageBox.Information)
        box.setText(f"{t('app_title')} - {t('app_subtitle')}")
        box.setInformativeText(
            f"1) {t('help_step1_title')}\n{t('help_step1_desc')}\n\n"
            f"2) {t('help_step2_title')}\n{t('help_step2_desc')}\n\n"
            f"3) {t('help_step3_title')}\n{t('help_step3_desc')}\n\n"
            f"{t('help_contact')}"
        )
        box.exec()

    # ---------- Sharing Actions ----------

    def toggle(self) -> None:
        if self.busy:
            return
        active = sharing_active(self.active_eth)
        self.busy = True
        self.toggle_btn.setEnabled(False)
        self.toggle_btn.setText(t("btn_busy"))
        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            if active:
                self._disable()
            else:
                self._enable()
        finally:
            QApplication.restoreOverrideCursor()
            self.toggle_btn.setEnabled(True)
            self.busy = False
            self.refresh()

    def _enable(self) -> None:
        success, msg = enable_sharing(self.active_eth)
        if not success:
            self._error(t("err_sharing_start"), msg)

    def _disable(self) -> None:
        success, msg = disable_sharing()
        if not success:
            self._error(t("err_sharing_stop"), msg)

    def _error(self, title: str, detail: str) -> None:
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setIcon(QMessageBox.Warning)
        box.setText(title)
        box.setInformativeText((detail or "").strip()[:600])
        box.exec()

    # ---------- Deskflow (KVM) Actions ----------

    def set_edge(self, edge: str) -> None:
        if edge not in EDGES:
            return
        self.edge = edge
        self.settings["edge"] = edge
        save_settings(self.settings)
        write_deskflow_config(edge, self.mouse_wifi, share_ip=SHARE_IP)
        if self.deskflow.state() == QProcess.Running:
            self.stop_mouse(restart=True, keep_wanted=True)
        self.refresh()

    def set_mouse_wifi(self, enabled: bool) -> None:
        self.mouse_wifi = enabled
        self.settings["mouse_wifi"] = enabled
        save_settings(self.settings)
        if self.deskflow.state() == QProcess.Running:
            self.stop_mouse(restart=True, keep_wanted=True)
        self.refresh()

    def set_mouse_enabled(self, enabled: bool) -> None:
        if enabled:
            self.mouse_wanted = True
            self.settings["mouse_enabled"] = True
            save_settings(self.settings)
            self.start_mouse(silent=not sharing_active(self.active_eth))
        else:
            self.stop_mouse()
        self.refresh()

    def toggle_mouse(self) -> None:
        running = self.deskflow.state() == QProcess.Running
        self.set_mouse_enabled(not (running or self.mouse_wanted))

    def start_mouse(self, silent: bool = False) -> None:
        if not is_deskflow_installed():
            if not silent:
                self._error(
                    t("mouse_not_installed"),
                    f"{t('mouse_install_guide')}\n\nArch Linux: sudo pacman -S deskflow\nDebian/Ubuntu: sudo apt install deskflow",
                )
            return
        if self.deskflow.state() != QProcess.NotRunning:
            return
        if not sharing_active(self.active_eth) or iface_address(self.active_eth) == "-":
            if not silent:
                self._error(t("err_start_sharing_first"), t("err_start_sharing_desc"))
            return
        write_deskflow_config(self.edge, self.mouse_wifi, share_ip=SHARE_IP)
        self.deskflow_output = ""
        self.deskflow.start()
        if not self.deskflow.waitForStarted(4000):
            if not silent:
                self._error(t("err_mouse_start"), self.deskflow.errorString())
            return
        self.mouse_wanted = True
        self.settings["mouse_enabled"] = True
        save_settings(self.settings)

    def stop_mouse(self, restart: bool = False, keep_wanted: bool = False) -> None:
        if self.deskflow.state() != QProcess.NotRunning:
            self.deskflow.terminate()
            if not self.deskflow.waitForFinished(3000):
                self.deskflow.kill()
                self.deskflow.waitForFinished(1500)
        self.mouse_wanted = keep_wanted
        self.settings["mouse_enabled"] = keep_wanted
        save_settings(self.settings)
        if restart:
            self.start_mouse()

    def _read_deskflow(self) -> None:
        data = bytes(self.deskflow.readAllStandardOutput()).decode("utf-8", "replace")
        if data:
            self.deskflow_output = (self.deskflow_output + data)[-4000:]

    def _deskflow_finished(self, code: int, status: QProcess.ExitStatus) -> None:
        pass

    def _deskflow_error(self, error: QProcess.ProcessError) -> None:
        pass

    def show_mouse_help(self) -> None:
        box = QMessageBox(self)
        box.setWindowTitle(t("win_setup_title"))
        box.setIcon(QMessageBox.Information)
        _, wifi_ip = wifi_info()
        wifi_line = ""
        if self.mouse_wifi and wifi_ip != "-":
            wifi_line = f"   Wi-Fi IP: {wifi_ip}\n"
        box.setText(f"{t('card_mouse_title')} (Deskflow)")
        box.setInformativeText(
            f"1) {t('win_setup_step1')}\n\n"
            f"2) {t('win_setup_step2')}\n\n"
            f"3) {t('win_setup_step3')}: {SHARE_IP}\n"
            f"{wifi_line}"
            f"4) {t('win_setup_step4')}: {CLIENT_SCREEN}\n\n"
            f"5) {t('win_setup_step5')}\n\n"
            f"6) {t('win_setup_step6')}\n\n"
            f"{t('edge_hint')}"
        )
        box.exec()

    # ---------- File Server Actions ----------

    def _close_file_server(self) -> None:
        server = self.file_server
        self.file_server = None
        if server is not None:
            try:
                server.shutdown()
                server.server_close()
            except OSError:
                pass

    def start_files(self, silent: bool = False) -> None:
        if self.file_server is not None:
            return
        if not sharing_active(self.active_eth) or iface_address(self.active_eth) == "-":
            if not silent:
                self._error(t("err_start_sharing_first"), t("err_start_sharing_desc"))
            return
        try:
            self.files_dir.mkdir(parents=True, exist_ok=True)
            handler = type("Handler", (FileShareHandler,), {"directory": str(self.files_dir)})
            bind_ip = "0.0.0.0" if self.wifi_enabled else SHARE_IP
            server = ThreadingHTTPServer((bind_ip, FILE_PORT), handler)
        except OSError as exc:
            self.files_wanted = False
            self.settings["files_enabled"] = False
            save_settings(self.settings)
            if not silent:
                self._error(
                    t("err_file_server"),
                    f"{exc}\n\nPort {FILE_PORT} might already be in use.",
                )
            return
        server.daemon_threads = True
        self.file_server = server
        self.files_wanted = True
        self.settings["files_enabled"] = True
        self.settings["files_dir"] = str(self.files_dir)
        save_settings(self.settings)
        threading.Thread(target=server.serve_forever, daemon=True).start()

    def stop_files(self) -> None:
        self._close_file_server()
        self.files_wanted = False
        self.settings["files_enabled"] = False
        save_settings(self.settings)

    def set_files_enabled(self, enabled: bool) -> None:
        if enabled:
            self.files_wanted = True
            self.settings["files_enabled"] = True
            save_settings(self.settings)
            self.start_files(silent=not sharing_active(self.active_eth))
        else:
            self.stop_files()
        self.refresh()

    def toggle_files(self) -> None:
        running = self.file_server is not None
        self.set_files_enabled(not (running or self.files_wanted))

    def copy_files_url(self) -> None:
        QApplication.clipboard().setText(f"http://{SHARE_IP}:{FILE_PORT}")

    def wifi_url(self) -> str:
        _, ip = wifi_info()
        if ip == "-":
            return ""
        return f"http://{ip}:{FILE_PORT}"

    def copy_wifi_url(self) -> None:
        url = self.wifi_url()
        if url:
            QApplication.clipboard().setText(url)

    def set_wifi_access(self, enabled: bool) -> None:
        self.wifi_enabled = enabled
        self.settings["wifi_enabled"] = enabled
        save_settings(self.settings)
        if self.file_server is not None or self.files_wanted:
            self._close_file_server()
            self.start_files(silent=True)
        self.refresh()

    def copy_smb_path(self) -> None:
        QApplication.clipboard().setText(SMB_PATH)

    def open_files_dir(self) -> None:
        try:
            self.files_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.files_dir)))

    def set_autostart(self, enabled: bool) -> None:
        try:
            if enabled:
                AUTOSTART_PATH.parent.mkdir(parents=True, exist_ok=True)
                bin_path = Path.home() / ".local/bin/ramord-link"
                AUTOSTART_PATH.write_text(
                    "[Desktop Entry]\n"
                    "Type=Application\n"
                    "Name=Ramord Link\n"
                    f"Exec={bin_path}\n"
                    f"Icon={ICON_PATH}\n"
                    "Terminal=false\n"
                    "X-GNOME-Autostart-enabled=true\n"
                )
            elif AUTOSTART_PATH.exists():
                AUTOSTART_PATH.unlink()
        except OSError as exc:
            QMessageBox.warning(self, "Error", f"Failed to set autostart:\n{exc}")

    # ---------- Window Management ----------

    def show_window(self) -> None:
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event) -> None:
        if self.tray and not self.quitting:
            event.ignore()
            self.hide()
            self.tray.showMessage(
                t("app_title"),
                t("tray_hint"),
                QSystemTrayIcon.Information,
                2500,
            )
        else:
            event.accept()

    def quit_app(self) -> None:
        self.quitting = True
        self.stop_mouse()
        self.stop_files()
        if self.tray:
            self.tray.hide()
        QApplication.quit()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("ramord-link")
    app.setDesktopFileName("ramord-link")
    app.setQuitOnLastWindowClosed(False)
    app.setStyleSheet(STYLE)

    # Single-instance enforcement
    server_key = "ramord-link"
    probe = QLocalSocket()
    probe.connectToServer(server_key)
    if probe.waitForConnected(250):
        probe.write(b"show")
        probe.flush()
        probe.waitForBytesWritten(250)
        probe.disconnectFromServer()
        return 0

    QLocalServer.removeServer(server_key)
    server = QLocalServer(app)
    server.listen(server_key)

    window = MainWindow()
    server.newConnection.connect(window.show_window)
    window.show()

    signal.signal(signal.SIGINT, lambda *_: app.quit())
    timer = QTimer()
    timer.start(300)
    timer.timeout.connect(lambda: None)

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
