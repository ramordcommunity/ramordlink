# Ramord Link

<p align="center">
  <img src="assets/ramord-link.svg" width="128" height="128" alt="Ramord Link Logo">
  <br>
  <b>One-Click Internet, KVM & File Sharing Bridge for Windows & Linux</b>
  <br>
  <i>Windows ve Linux için Tek Tıkla İnternet, KVM ve Dosya Paylaşım Köprüsü</i>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#trke-aklama">Türkçe Açıklama</a> •
  <a href="#contact">Contact</a>
</p>

---

## English

**Ramord Link** is a modern, lightweight, modular open-source desktop application designed to bridge a Linux workstation and a secondary computer (such as a Windows PC or Mac) over a single Ethernet cable and local Wi-Fi.

### Key Capabilities

1. **One-Click Internet Sharing (NAT Gateway):**
   - Automatically detects active Ethernet and Wi-Fi network interfaces.
   - Configures NetworkManager shared profile (`192.168.50.1/24` with built-in DHCP server `192.168.50.10 - 254`).
   - Automatically bridges incoming Wi-Fi internet to the connected computer over Ethernet with zero manual iptables configuration.

2. **KVM Mouse & Keyboard Sharing (Deskflow Integration):**
   - Seamlessly moves your mouse and keyboard between Linux and Windows screens.
   - Edge directional selector (Right, Left, Above, Below) with live configuration updates.
   - Optional Wi-Fi connection mode for wireless secondary PCs.
   - Real-time connection status monitoring.

3. **Multilingual Drag & Drop Web File Transfer:**
   - Built-in lightweight HTTP file server (Port `8080`) serving the shared folder (`~/Genel`).
   - Drag & Drop browser uploads directly from phone or secondary PC.
   - 4 GB upload safety threshold and 100 MB disk quota safety buffer.
   - Atomic file writes using temporary `.part` files.
   - Native Samba (`smb://`) path endpoint integration.

4. **Full 6-Language Localization:**
   - Native support for **English (`en`)**, **Turkish (`tr`)**, **German (`de`)**, **Spanish (`es`)**, **French (`fr`)**, and **Italian (`it`)**.
   - System language auto-detection and on-the-fly dynamic language switching in both Desktop GUI and Web interface.

5. **Desktop & System Integration:**
   - Single-instance enforcement via local socket (`ramord-link`).
   - System tray icon with background minimization and quick-action menu.
   - Autostart toggle (`~/.config/autostart`).

---

### Installation

#### Prerequisites

- Linux (Arch Linux, Fedora, Ubuntu/Debian, or openSUSE)
- Python 3.9+
- `PySide6`
- `NetworkManager` (`nmcli`)
- Optional: `deskflow` (for mouse/keyboard sharing)
- Optional: `samba` (for Windows SMB network folder access)

#### Quick Setup

```bash
git clone https://github.com/ramordcommunity/ramordlink.git
cd ramordlink
./install.sh
```

The installer installs:
- Binary launcher in `~/.local/bin/ramord-link`
- Backwards-compatibility symlink `~/.local/bin/internet-paylasim -> ~/.local/bin/ramord-link`
- Desktop shortcut in `~/.local/share/applications/ramord-link.desktop`
- Scalable SVG icon in `~/.local/share/icons/hicolor/scalable/apps/ramord-link.svg`

To run:
```bash
ramord-link
```

---

## Türkçe Açıklama

**Ramord Link**, Linux bilgisayarınız ile ikincil bir bilgisayarı (Windows PC veya Mac) tek bir Ethernet kablosu ve yerel Wi-Fi ağı üzerinden birbirine bağlayan modern, modüler ve açık kaynaklı bir köprü uygulamasıdır.

### Temel Özellikler

- **Tek Tıkla İnternet Paylaşımı:** Wi-Fi internetinizi tek tıkla Ethernet kablosu üzerinden diğer bilgisayarla paylaşın (`192.168.50.1/24` ağ geçidi ve otomatik DHCP).
- **Mouse ve Klavye Paylaşımı (KVM):** Masanızdaki fare ve klavyeyi Deskflow entegrasyonuyla Windows ekranına pürüzsüzce geçirin.
- **Web Dosya Paylaşımı (Sürükle & Bırak):** Tarayıcı üzerinden telefon ve bilgisayarlardan `~/Genel` klasörüne dosya gönderip indirin (4 GB limit ve kota korumalı).
- **6 Dilde Tam Destek:** Türkçe, İngilizce, Almanca, İspanyolca, Fransızca ve İtalyanca arayüz desteği.
- **Sistem Tepsisi & Arka Plan:** Kapatıldığında tepsiye küçülür, tek örnek kilidiyle çakışmaları önler.

---

## License

Distributed under the **GNU General Public License v3.0 (GPL-3.0)**. See [LICENSE](LICENSE) for details.

---

## Contact & Support

- **Official Email:** `ramordhelp@gmail.com`
- **GitHub Organization:** [Ramord Community](https://github.com/ramordcommunity)
