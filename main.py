#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ramord Link - Desktop Application GUI
A modern, multilingual (6 languages: tr, en, de, es, fr, it) bridge application
providing one-click internet sharing, KVM mouse/keyboard sharing, and local web file transfer.
Built with GTK4 & Libadwaita (Apple-like modern unified window and header bar).

Official Contact: ramordhelp@gmail.com
"""

from __future__ import annotations
import html
import json
import os
import signal
import subprocess
import sys
import threading
import time
import urllib.parse
from http.server import ThreadingHTTPServer
from pathlib import Path

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Gdk

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
    HOTSPOT_CONNECTION_NAME,
    HOTSPOT_DEFAULT_PASS,
    HOTSPOT_DEFAULT_SSID,
    SHARE_IP,
    SMB_SHARE_NAME,
    clients,
    detect_interfaces,
    disable_hotspot,
    disable_sharing,
    enable_hotspot,
    enable_sharing,
    get_default_ethernet,
    get_default_wifi,
    iface_address,
    is_carrier_up,
    is_hotspot_active,
    is_samba_running,
    is_wifi_ap_supported,
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
SMB_PATH = f"\\\\{SHARE_IP}\\{SMB_SHARE_NAME}"
APP_DIR = Path(__file__).resolve().parent
ICON_PATH = APP_DIR / "assets/ramord-link.svg"
OFFICIAL_EMAIL = "ramordhelp@gmail.com"


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


class RamordLinkWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Ramord Link")
        self.set_default_size(780, 860)
        self.set_icon_name("ramord-link")

        self.settings = load_settings()
        saved_lang = self.settings.get("language")
        self.current_lang = saved_lang if saved_lang in LANGUAGES else detect_system_language()
        set_lang(self.current_lang)

        # Network interface settings
        eth_ifaces, wifi_ifaces = detect_interfaces()
        self.eth_ifaces = eth_ifaces
        self.wifi_ifaces = wifi_ifaces

        saved_eth = self.settings.get("eth_iface")
        self.active_eth = saved_eth if saved_eth in eth_ifaces else get_default_ethernet()
        self.sharing_mode = self.settings.get("sharing_mode", "ethernet")  # 'ethernet' or 'hotspot'

        self.edge = self.settings.get("edge", "right")
        if self.edge not in EDGES:
            self.edge = "right"

        # Deskflow server process
        self.deskflow_proc: subprocess.Popen | None = None
        self.deskflow_thread: threading.Thread | None = None
        self.mouse_wanted = bool(self.settings.get("mouse_enabled", False))
        self.mouse_wifi = bool(self.settings.get("mouse_wifi", False))

        # File sharing server
        self.file_server: ThreadingHTTPServer | None = None
        self.files_dir = Path(self.settings.get("files_dir", str(DEFAULT_SHARE_DIR)))
        self.files_wanted = bool(self.settings.get("files_enabled", False))
        self.wifi_enabled = bool(self.settings.get("wifi_enabled", False))

        self.theme_mode = self.settings.get("theme", "auto")
        self.css_provider = None

        self._build_ui()
        self._apply_theme()
        self._refresh_texts()
        self.refresh()

        # Start periodic UI refresh timer (every 2 seconds)
        GLib.timeout_add_seconds(2, self._on_timer_tick)

        # Auto-start services if previously wanted and network sharing active
        if self.mouse_wanted and is_deskflow_installed() and sharing_active(self.active_eth):
            GLib.timeout_add(600, lambda: self.start_mouse(silent=True) or False)
        if self.files_wanted and sharing_active(self.active_eth):
            GLib.timeout_add(900, lambda: self.start_files(silent=True) or False)

    def _on_timer_tick(self) -> bool:
        self.refresh()
        return True

    def _detect_system_theme(self) -> str:
        try:
            sm = Adw.StyleManager.get_default()
            return "night" if sm.get_dark() else "day"
        except Exception:
            return "night"

    def _resolve_theme_key(self) -> str:
        if self.theme_mode in ("day", "night"):
            return self.theme_mode
        return self._detect_system_theme()

    def _apply_theme(self):
        """Applies solid Day (#F4F1EA/#EFECE6/#2B2A27/#1A3328) or Night (#080C0A/#101613/#E8E4DA/#589E7B) theme."""
        active_key = self._resolve_theme_key()
        is_day = (active_key == "day")

        if is_day:
            bg = "#F4F1EA"
            card = "#EFECE6"
            card_border = "rgba(26, 51, 40, 0.15)"
            text = "#2B2A27"
            dim = "#6B6862"
            accent = "#1A3328"
            accent_hover = "#284e3e"
            accent_text = "#F4F1EA"
            header_bg = "#EAE5DC"
        else:
            bg = "#080C0A"
            card = "#101613"
            card_border = "rgba(88, 158, 123, 0.20)"
            text = "#E8E4DA"
            dim = "#8A948E"
            accent = "#589E7B"
            accent_hover = "#6db893"
            accent_text = "#080C0A"
            header_bg = "#0d1310"

        css_text = f"""
        window, window.background {{
            border-radius: 16px;
            background: {bg};
            color: {text};
        }}

        headerbar {{
            background: {header_bg};
            border-bottom: 1px solid {card_border};
            color: {text};
            border-top-left-radius: 16px;
            border-top-right-radius: 16px;
        }}

        preferencesgroup > box {{
            background: {card};
            border: 1px solid {card_border};
            border-radius: 14px;
            padding: 4px;
            color: {text};
        }}

        .boxed-list {{
            background: {card};
            border: 1px solid {card_border};
            border-radius: 14px;
            color: {text};
        }}

        .boxed-list row {{
            border-bottom: 1px solid {card_border};
            color: {text};
        }}

        .suggested-action {{
            background: {accent};
            color: {accent_text};
            font-weight: 700;
            border: none;
        }}

        .suggested-action:hover {{
            background: {accent_hover};
        }}

        .destructive-action {{
            background: #ef4444;
            color: #ffffff;
            font-weight: 700;
            border: none;
        }}

        popover contents, popover .view, popover listview {{
            background-color: {card};
            color: {text};
            border-radius: 12px;
            border: 1px solid {card_border};
            padding: 6px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}

        popover listview row {{
            padding: 10px 14px;
            border-radius: 8px;
            margin: 2px 0;
            min-height: 38px;
            color: {text};
        }}

        popover listview row:selected, popover listview row:hover {{
            background: {card_border};
            color: {accent};
        }}
        """

        if self.css_provider is not None:
            Gtk.StyleContext.remove_provider_for_display(
                Gdk.Display.get_default(),
                self.css_provider
            )

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(css_text.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            self.css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _build_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(main_box)

        # Header Bar
        self.header_bar = Adw.HeaderBar()
        main_box.append(self.header_bar)

        # Language Selector (Pill button with locale icon)
        self.lang_btn = Gtk.MenuButton()
        self.lang_btn.add_css_class("flat")
        self.lang_btn.set_tooltip_text("Language / Dil")

        lang_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lang_icon = Gtk.Image.new_from_icon_name("preferences-desktop-locale-symbolic")
        self.lang_btn_label = Gtk.Label(label=LANGUAGES.get(self.current_lang, "English"))
        self.lang_btn_label.add_css_class("heading")
        lang_btn_box.append(lang_icon)
        lang_btn_box.append(self.lang_btn_label)
        self.lang_btn.set_child(lang_btn_box)

        lang_popover = Gtk.Popover()
        lang_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        lang_box.set_margin_top(8)
        lang_box.set_margin_bottom(8)
        lang_box.set_margin_start(8)
        lang_box.set_margin_end(8)

        for code, label in LANGUAGES.items():
            btn = Gtk.Button(label=label)
            btn.add_css_class("flat")
            btn.connect("clicked", self._on_change_language, code, lang_popover)
            lang_box.append(btn)

        lang_popover.set_child(lang_box)
        self.lang_btn.set_popover(lang_popover)
        self.header_bar.pack_start(self.lang_btn)

        # Theme Switcher (Auto / Day / Night)
        self.theme_btn = Gtk.MenuButton()
        self.theme_btn.add_css_class("flat")
        self.theme_btn.set_tooltip_text("Theme / Tema")
        theme_btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        theme_icon = Gtk.Image.new_from_icon_name("display-brightness-symbolic")
        self.theme_btn_label = Gtk.Label(label=t(f"theme_{self.theme_mode}", self.current_lang))
        self.theme_btn_label.add_css_class("heading")
        theme_btn_box.append(theme_icon)
        theme_btn_box.append(self.theme_btn_label)
        self.theme_btn.set_child(theme_btn_box)

        theme_popover = Gtk.Popover()
        theme_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        theme_box.set_margin_top(8)
        theme_box.set_margin_bottom(8)
        theme_box.set_margin_start(8)
        theme_box.set_margin_end(8)

        for m_key in ("auto", "day", "night"):
            m_btn = Gtk.Button(label=t(f"theme_{m_key}", self.current_lang))
            m_btn.add_css_class("flat")
            m_btn.connect("clicked", self._on_change_theme, m_key, theme_popover)
            theme_box.append(m_btn)

        theme_popover.set_child(theme_box)
        self.theme_btn.set_popover(theme_popover)
        self.header_bar.pack_start(self.theme_btn)

        # Help / Guide Button in HeaderBar
        self.help_btn = Gtk.Button.new_from_icon_name("help-about-symbolic")
        self.help_btn.connect("clicked", self._on_show_help)
        self.header_bar.pack_end(self.help_btn)

        # Scrolled Window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)
        main_box.append(scrolled)

        # Clamp Container
        clamp = Adw.Clamp()
        clamp.set_maximum_size(720)
        clamp.set_tightening_threshold(560)
        scrolled.set_child(clamp)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(32)
        content_box.set_margin_start(16)
        content_box.set_margin_end(16)
        clamp.set_child(content_box)

        # 1. Header Banner Box
        self.banner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.banner_box.set_halign(Gtk.Align.CENTER)
        self.banner_box.set_margin_top(12)
        self.banner_box.set_margin_bottom(12)
        content_box.append(self.banner_box)

        if ICON_PATH.exists():
            self.banner_icon = Gtk.Image.new_from_file(str(ICON_PATH))
            self.banner_icon.set_pixel_size(96)
        else:
            self.banner_icon = Gtk.Image.new_from_icon_name("network-wired-symbolic")
            self.banner_icon.set_pixel_size(84)
        self.banner_box.append(self.banner_icon)

        self.banner_title = Gtk.Label(label="Ramord Link")
        self.banner_title.add_css_class("title-1")
        self.banner_box.append(self.banner_title)

        self.banner_desc = Gtk.Label()
        self.banner_desc.add_css_class("body")
        self.banner_desc.add_css_class("dim-label")
        self.banner_desc.set_wrap(True)
        self.banner_desc.set_justify(Gtk.Justification.CENTER)
        self.banner_desc.set_max_width_chars(54)
        self.banner_box.append(self.banner_desc)

        # 2. Internet Sharing Group (Ethernet / Hotspot)
        self.sharing_group = Adw.PreferencesGroup()
        content_box.append(self.sharing_group)

        # Mode Selection: Ethernet vs Hotspot
        self.mode_row = Adw.ComboRow()
        self.mode_model = Gtk.StringList()
        self.mode_row.set_model(self.mode_model)
        self.mode_row.connect("notify::selected", self._on_mode_combo_changed)
        self.sharing_group.add(self.mode_row)

        # Ethernet Interface Row
        self.iface_row = Adw.ComboRow()
        self.iface_model = Gtk.StringList()
        self.iface_row.set_model(self.iface_model)
        self.iface_row.connect("notify::selected", self._on_iface_combo_changed)
        self.sharing_group.add(self.iface_row)

        # Hotspot SSID & Password Rows
        self.hotspot_ssid_row = Adw.EntryRow()
        self.hotspot_ssid_row.set_text(self.settings.get("hotspot_ssid", HOTSPOT_DEFAULT_SSID))
        self.sharing_group.add(self.hotspot_ssid_row)

        self.hotspot_pass_row = Adw.PasswordEntryRow()
        self.hotspot_pass_row.set_text(self.settings.get("hotspot_pass", HOTSPOT_DEFAULT_PASS))
        self.sharing_group.add(self.hotspot_pass_row)

        # Main Action Button Row
        self.action_row = Adw.ActionRow()
        self.action_btn = Gtk.Button()
        self.action_btn.add_css_class("suggested-action")
        self.action_btn.set_valign(Gtk.Align.CENTER)
        self.action_btn.connect("clicked", self._on_toggle_sharing)
        self.action_row.add_suffix(self.action_btn)
        self.sharing_group.add(self.action_row)

        # 3. KVM Mouse & Keyboard Group
        self.mouse_group = Adw.PreferencesGroup()
        content_box.append(self.mouse_group)

        self.mouse_switch_row = Adw.SwitchRow()
        self.mouse_switch_row.set_active(self.mouse_wanted)
        self.mouse_switch_row.connect("notify::active", self._on_mouse_switch_toggled)
        self.mouse_group.add(self.mouse_switch_row)

        self.edge_row = Adw.ComboRow()
        self.edge_model = Gtk.StringList()
        self.edge_row.set_model(self.edge_model)
        self.edge_row.connect("notify::selected", self._on_edge_changed)
        self.mouse_group.add(self.edge_row)

        self.mouse_guide_row = Adw.ActionRow()
        btn_mouse_guide = Gtk.Button.new_from_icon_name("dialog-information-symbolic")
        btn_mouse_guide.set_valign(Gtk.Align.CENTER)
        btn_mouse_guide.connect("clicked", self._on_show_mouse_guide)
        self.mouse_guide_row.add_suffix(btn_mouse_guide)
        self.mouse_group.add(self.mouse_guide_row)

        # 4. Web File Sharing Group
        self.files_group = Adw.PreferencesGroup()
        content_box.append(self.files_group)

        self.files_switch_row = Adw.SwitchRow()
        self.files_switch_row.set_active(self.files_wanted)
        self.files_switch_row.connect("notify::active", self._on_files_switch_toggled)
        self.files_group.add(self.files_switch_row)

        self.folder_row = Adw.ActionRow()
        self.folder_row.set_subtitle(str(self.files_dir))

        btn_open_folder = Gtk.Button.new_from_icon_name("folder-open-symbolic")
        btn_open_folder.set_valign(Gtk.Align.CENTER)
        btn_open_folder.connect("clicked", lambda b: Gio.AppInfo.launch_default_for_uri(f"file://{self.files_dir}", None))
        self.folder_row.add_suffix(btn_open_folder)

        btn_copy_link = Gtk.Button.new_from_icon_name("edit-copy-symbolic")
        btn_copy_link.set_valign(Gtk.Align.CENTER)
        btn_copy_link.connect("clicked", self._on_copy_web_link)
        self.folder_row.add_suffix(btn_copy_link)
        self.files_group.add(self.folder_row)

        self.smb_row = Adw.ActionRow()
        self.smb_row.set_title("Windows SMB")
        self.smb_row.set_subtitle(SMB_PATH)
        btn_copy_smb = Gtk.Button.new_from_icon_name("edit-copy-symbolic")
        btn_copy_smb.set_valign(Gtk.Align.CENTER)
        btn_copy_smb.connect("clicked", lambda b: self._copy_text(SMB_PATH))
        self.smb_row.add_suffix(btn_copy_smb)
        self.files_group.add(self.smb_row)

    def _on_change_language(self, button, code, popover):
        self.current_lang = code
        set_lang(code)
        self.settings["language"] = code
        save_settings(self.settings)
        popover.popdown()
        self._refresh_texts()
        self.refresh()

    def _on_change_theme(self, button, mode, popover):
        self.theme_mode = mode
        self.settings["theme"] = mode
        save_settings(self.settings)
        popover.popdown()
        self._apply_theme()
        self._refresh_texts()

    def _on_show_help(self, button):
        lang = self.current_lang
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=t("help_dialog_title", lang),
            body=(
                f"{t('help_p1', lang)}\n\n"
                f"{t('help_p2', lang)}\n\n"
                f"{t('help_p3', lang)}\n\n"
                f"{t('help_p4', lang)}\n\n"
                f"Contact: {OFFICIAL_EMAIL}"
            )
        )
        dialog.add_response("ok", "Tamam" if lang == "tr" else "OK")
        dialog.present()

    def _on_show_mouse_guide(self, button):
        lang = self.current_lang
        _, wifi_ip = wifi_info()
        wifi_line = f"   Wi-Fi IP: {wifi_ip}\n" if (self.mouse_wifi and wifi_ip != "-") else ""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=f"{t('win_setup_title', lang)} (Deskflow)",
            body=(
                f"1) {t('win_setup_step1', lang)}\n\n"
                f"2) {t('win_setup_step2', lang)}\n\n"
                f"3) {t('win_setup_step3', lang)}: {SHARE_IP}\n"
                f"{wifi_line}"
                f"4) {t('win_setup_step4', lang)}: {CLIENT_SCREEN}\n\n"
                f"5) {t('win_setup_step5', lang)}\n\n"
                f"6) {t('win_setup_step6', lang)}\n\n"
                f"7) {t('win_setup_step7', lang)}\n\n"
                f"{t('edge_hint', lang)}"
            )
        )
        dialog.add_response("ok", "Tamam" if lang == "tr" else "OK")
        dialog.present()

    def _on_mode_combo_changed(self, combo_row, pspec):
        idx = combo_row.get_selected()
        self.sharing_mode = "ethernet" if idx == 0 else "hotspot"
        self.settings["sharing_mode"] = self.sharing_mode
        save_settings(self.settings)
        self.iface_row.set_visible(self.sharing_mode == "ethernet")
        self.hotspot_ssid_row.set_visible(self.sharing_mode == "hotspot")
        self.hotspot_pass_row.set_visible(self.sharing_mode == "hotspot")
        self.refresh()

    def _on_iface_combo_changed(self, combo_row, pspec):
        idx = combo_row.get_selected()
        if 0 <= idx < len(self.eth_ifaces):
            self.active_eth = self.eth_ifaces[idx]
            self.settings["eth_iface"] = self.active_eth
            save_settings(self.settings)
            self.refresh()

    def _on_edge_changed(self, combo_row, pspec):
        idx = combo_row.get_selected()
        edge_keys = ["right", "left", "top", "bottom"]
        if 0 <= idx < len(edge_keys):
            self.edge = edge_keys[idx]
            self.settings["edge"] = self.edge
            save_settings(self.settings)
            write_deskflow_config(self.edge, self.mouse_wifi, share_ip=SHARE_IP)
            if self.deskflow_proc is not None and self.deskflow_proc.poll() is None:
                self.stop_mouse(restart=True, keep_wanted=True)

    def _on_mouse_switch_toggled(self, switch_row, pspec):
        enabled = switch_row.get_active()
        if enabled:
            self.mouse_wanted = True
            self.settings["mouse_enabled"] = True
            save_settings(self.settings)
            self.start_mouse(silent=not sharing_active(self.active_eth))
        else:
            self.stop_mouse()
        self.refresh()

    def _on_files_switch_toggled(self, switch_row, pspec):
        enabled = switch_row.get_active()
        if enabled:
            self.start_files()
        else:
            self.stop_files()
        self.refresh()

    def _on_toggle_sharing(self, button):
        is_eth = (self.sharing_mode == "ethernet")
        active = sharing_active(self.active_eth) if is_eth else is_hotspot_active()

        if active:
            if is_eth:
                disable_sharing(self.active_eth)
            else:
                disable_hotspot()
        else:
            if is_eth:
                ok, err = enable_sharing(self.active_eth)
                if not ok:
                    self._show_error(t("err_share_failed", self.current_lang), err)
            else:
                ssid = self.hotspot_ssid_row.get_text() or HOTSPOT_DEFAULT_SSID
                pw = self.hotspot_pass_row.get_text() or HOTSPOT_DEFAULT_PASS
                self.settings["hotspot_ssid"] = ssid
                self.settings["hotspot_pass"] = pw
                save_settings(self.settings)
                ok, err = enable_hotspot(ssid, pw)
                if not ok:
                    self._show_error(t("err_hotspot_failed", self.current_lang), err)

        self.refresh()

    def _copy_text(self, text: str):
        clipboard = Gdk.Display.get_default().get_clipboard()
        clipboard.set(text)

    def _on_copy_web_link(self, button):
        ip = iface_address(self.active_eth)
        url = f"http://{ip}:{FILE_PORT}" if ip != "-" else f"http://{SHARE_IP}:{FILE_PORT}"
        self._copy_text(url)

    def _show_error(self, title: str, detail: str):
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=title,
            body=detail
        )
        dialog.add_response("ok", "Tamam" if self.current_lang == "tr" else "OK")
        dialog.present()

    # ---------- Deskflow (KVM) Service Management ----------

    def start_mouse(self, silent: bool = False):
        if not is_deskflow_installed():
            if not silent:
                self._show_error(
                    t("mouse_not_installed", self.current_lang),
                    f"{t('mouse_install_guide', self.current_lang)}\n\nArch: sudo pacman -S deskflow\nUbuntu: sudo apt install deskflow"
                )
            self.mouse_switch_row.set_active(False)
            return

        if self.deskflow_proc is not None and self.deskflow_proc.poll() is None:
            return

        if not sharing_active(self.active_eth) or iface_address(self.active_eth) == "-":
            if not silent:
                self._show_error(t("err_start_sharing_first", self.current_lang), t("err_start_sharing_desc", self.current_lang))
            self.mouse_switch_row.set_active(False)
            return

        write_deskflow_config(self.edge, self.mouse_wifi, share_ip=SHARE_IP)
        try:
            self.deskflow_proc = subprocess.Popen(
                ["deskflow-core", "server", "-f"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            self.mouse_wanted = True
            self.settings["mouse_enabled"] = True
            save_settings(self.settings)
        except Exception as e:
            if not silent:
                self._show_error(t("err_mouse_start", self.current_lang), str(e))
            self.mouse_switch_row.set_active(False)

    def stop_mouse(self, restart: bool = False, keep_wanted: bool = False):
        if self.deskflow_proc is not None:
            try:
                self.deskflow_proc.terminate()
                self.deskflow_proc.wait(timeout=1.5)
            except Exception:
                try:
                    self.deskflow_proc.kill()
                except Exception:
                    pass
            self.deskflow_proc = None

        self.mouse_wanted = keep_wanted
        self.settings["mouse_enabled"] = keep_wanted
        save_settings(self.settings)

        if restart:
            self.start_mouse()

    # ---------- File Sharing Service Management ----------

    def start_files(self, silent: bool = False):
        if self.file_server is not None:
            return
        if not sharing_active(self.active_eth) or iface_address(self.active_eth) == "-":
            if not silent:
                self._show_error(t("err_start_sharing_first", self.current_lang), t("err_start_sharing_desc", self.current_lang))
            self.files_switch_row.set_active(False)
            return

        try:
            self.files_dir.mkdir(parents=True, exist_ok=True)
            handler = type("Handler", (FileShareHandler,), {"directory": str(self.files_dir)})
            bind_ip = "0.0.0.0" if self.wifi_enabled else SHARE_IP
            server = ThreadingHTTPServer((bind_ip, FILE_PORT), handler)
            server.daemon_threads = True
            self.file_server = server
            self.files_wanted = True
            self.settings["files_enabled"] = True
            save_settings(self.settings)

            threading.Thread(target=server.serve_forever, daemon=True).start()
        except Exception as exc:
            self.files_wanted = False
            self.settings["files_enabled"] = False
            save_settings(self.settings)
            self.files_switch_row.set_active(False)
            if not silent:
                self._show_error(t("err_file_server", self.current_lang), str(exc))

    def stop_files(self):
        server = self.file_server
        self.file_server = None
        if server is not None:
            try:
                server.shutdown()
                server.server_close()
            except OSError:
                pass
        self.files_wanted = False
        self.settings["files_enabled"] = False
        save_settings(self.settings)

    def refresh(self):
        is_eth = (self.sharing_mode == "ethernet")
        active = sharing_active(self.active_eth) if is_eth else is_hotspot_active()
        lang = self.current_lang

        if active:
            self.action_btn.set_label(t("btn_disable", lang))
            self.action_btn.remove_css_class("suggested-action")
            self.action_btn.add_css_class("destructive-action")
            self.action_row.set_title(t("state_on", lang))
            self.action_row.set_subtitle(t("hero_hint_on", lang) if is_eth else t("hotspot_on", lang))
        else:
            self.action_btn.set_label(t("btn_enable", lang))
            self.action_btn.remove_css_class("destructive-action")
            self.action_btn.add_css_class("suggested-action")
            self.action_row.set_title(t("state_off", lang))
            self.action_row.set_subtitle(t("hero_hint_ethernet", lang) if is_eth else t("hero_hint_hotspot", lang))

        ip = iface_address(self.active_eth)
        web_url = f"http://{ip}:{FILE_PORT}" if ip != "-" else f"http://{SHARE_IP}:{FILE_PORT}"
        self.folder_row.set_title(f"Web: {web_url}")

    def _refresh_texts(self):
        lang = self.current_lang
        self.set_title(t("app_title", lang))
        self.banner_title.set_label(t("app_title", lang))
        self.banner_desc.set_label(t("app_subtitle", lang))
        self.lang_btn_label.set_label(LANGUAGES.get(lang, "English"))
        self.theme_btn_label.set_label(t(f"theme_{self.theme_mode}", lang))

        self.sharing_group.set_title(html.escape(t("tab_ethernet", lang) + " / " + t("tab_wireless", lang)))
        self.mode_row.set_title(t("lbl_select_iface", lang))

        # Mode model
        self.mode_model.splice(0, self.mode_model.get_n_items(), [t("tab_ethernet", lang), t("tab_wireless", lang)])
        self.mode_row.set_selected(0 if self.sharing_mode == "ethernet" else 1)

        # Eth Interface combo model
        if self.eth_ifaces:
            self.iface_model.splice(0, self.iface_model.get_n_items(), self.eth_ifaces)
            if self.active_eth in self.eth_ifaces:
                self.iface_row.set_selected(self.eth_ifaces.index(self.active_eth))
        self.iface_row.set_title(t("lbl_select_iface", lang))
        self.iface_row.set_visible(self.sharing_mode == "ethernet")

        self.hotspot_ssid_row.set_title(t("hotspot_ssid", lang))
        self.hotspot_pass_row.set_title(t("hotspot_password", lang))
        self.hotspot_ssid_row.set_visible(self.sharing_mode == "hotspot")
        self.hotspot_pass_row.set_visible(self.sharing_mode == "hotspot")

        # Mouse & Keyboard
        self.mouse_group.set_title(html.escape(t("card_mouse_title", lang)))
        self.mouse_switch_row.set_title(html.escape(t("card_mouse_title", lang)))
        self.mouse_switch_row.set_subtitle(t("mouse_on", lang) if self.mouse_wanted else t("mouse_off", lang))

        edge_keys = ["right", "left", "top", "bottom"]
        edge_labels = [t(f"edge_{k}", lang) for k in edge_keys]
        self.edge_model.splice(0, self.edge_model.get_n_items(), edge_labels)
        if self.edge in edge_keys:
            self.edge_row.set_selected(edge_keys.index(self.edge))
        self.edge_row.set_title(t("edge_question", lang))
        self.mouse_guide_row.set_title(t("btn_show_win_setup", lang))

        # File Sharing
        self.files_group.set_title(html.escape(t("card_files_title", lang)))
        self.files_switch_row.set_title(html.escape(t("card_files_title", lang)))
        self.files_switch_row.set_subtitle(t("files_on", lang) if self.files_wanted else t("files_off", lang))


class RamordLinkApp(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id="com.ramord.link",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )

    def do_activate(self):
        windows = self.get_windows()
        if not windows:
            win = RamordLinkWindow(self)
            win.present()
        else:
            # Toggle behavior: clicking or pressing shortcut toggles show/hide
            for w in list(windows):
                w.close()
            self.quit()


def main():
    app = RamordLinkApp()

    def handle_sig(sig, frame):
        for w in list(app.get_windows()):
            try:
                w.close()
            except Exception:
                pass
        app.quit()

    try:
        signal.signal(signal.SIGINT, handle_sig)
        signal.signal(signal.SIGTERM, handle_sig)
    except Exception:
        pass

    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
