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

**Ramord Link**, Linux bilgisayarınız ile ikincil bir bilgisayarı (Windows PC veya Mac) tek bir Ethernet kablosu veya yerel Wi-Fi ağı üzerinden birbirine bağlayan modern, modüler ve açık kaynaklı bir köprü uygulamasıdır.

### Temel Özellikler

1. **Tek Tıkla İnternet Paylaşımı (Ethernet ve Wi-Fi Hotspot):**
   - Wi-Fi internetinizi tek tıkla Ethernet kablosu üzerinden diğer bilgisayarla paylaşın (`192.168.50.1/24` ağ geçidi ve otomatik yerel DHCP).
   - Kablosuz internet paylaşımını destekleyen adaptörler için dahili güvenli Wi-Fi Hotspot oluşturma imkanı.

2. **Mouse, Klavye ve Otomatik Pano Paylaşımı (KVM / Deskflow):**
   - Masanızdaki tek bir fare ve klavyeyle hem Linux hem Windows ekranını yönetin.
   - Ekran yönü seçimi: İkinci ekranı **Sağ**, **Sol**, **Üst** veya **Alt** tarafa konumlandırın.
   - **Çift Yönlü Pano Senkronizasyonu (Clipboard):** Bir bilgisayarda kopyaladığınız (`Ctrl+C`) metin, kod parçası veya pano içeriği anında diğer bilgisayara aktarılır ve doğrudan yapıştırılabilir (`Ctrl+V`).

3. **Web ve Ağ Üzerinden Dosya Paylaşımı:**
   - Hafif yerel HTTP sunucusu (Port `8080`) üzerinden telefon ve bilgisayarlardan sürükle-bırak yöntemiyle dosya yükleme ve indirme.
   - Paylaşılacak ana klasörü arayüzden seçme imkanı (`~/Genel` veya dilediğiniz özel klasör).
   - Windows kullanıcıları için yerel SMB ağ klasörü (`\\192.168.50.1\Genel`) doğrudan erişim rehberi.

4. **6 Dilde Eksiksiz Arayüz Desteği:**
   - Türkçe (`tr`), İngilizce (`en`), Almanca (`de`), İspanyolca (`es`), Fransızca (`fr`) ve İtalyanca (`it`).
   - Sistem dilini otomatik algılama ve anında dinamik dil değiştirme.

5. **Masaüstü ve Sistem Entegrasyonu:**
   - Sistem tepsisi (tray) desteği, arka planda sessiz çalışma, tek örnek (single-instance) kilidi.

---

### Windows Kurulum ve Bağlantı Adımları (Mouse, Klavye & Pano)

1. Windows bilgisayarınıza **Deskflow** indirin ve kurun ([deskflow.org/download](https://deskflow.org/download)).
2. Deskflow'u **Client (İstemci)** modunda açın.
3. Sunucu IP adresi (Server IP) kutusuna: `192.168.50.1` yazın (Ethernet kablosu bağlıyken) veya yedek Wi-Fi IP adresini girin.
4. Ekran adı (Screen name) kutusuna: `windows` yazın.
5. Güvenlik ayarlarında **Use TLS encryption** seçeneğini kapalı tutun.
6. **Start** butonuna tıklayın. Bağlantı kurulduğunda Ramord Link üzerinde "İkinci PC Bağlı" durumuna geçecek; fare, klavye ve panonuz ortak çalışacaktır.

---

## License

Distributed under the **GNU General Public License v3.0 (GPL-3.0)**. See [LICENSE](LICENSE) for details.

---

## Contact & Support

- **Official Email:** `ramordhelp@gmail.com`
- **GitHub Organization:** [Ramord Community](https://github.com/ramordcommunity)
