# -*- coding: utf-8 -*-
"""
Ramord Link - Multilingual Localization Module (6 Languages: tr, en, de, es, fr, it)
Compliant with Ramord System Rules.
Official Contact: ramordhelp@gmail.com
"""

from __future__ import annotations
import locale
import os

LANGUAGES = {
    "tr": "Türkçe",
    "en": "English",
    "de": "Deutsch",
    "es": "Español",
    "fr": "Français",
    "it": "Italiano",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "app_title": {
        "tr": "Ramord Link",
        "en": "Ramord Link",
        "de": "Ramord Link",
        "es": "Ramord Link",
        "fr": "Ramord Link",
        "it": "Ramord Link",
    },
    "app_subtitle": {
        "tr": "Windows & Linux için Tek Tıkla İnternet, KVM ve Dosya Köprüsü",
        "en": "One-Click Internet, KVM & File Bridge for Windows & Linux",
        "de": "Ein-Klick-Internet-, KVM- und Datei-Bridge für Windows & Linux",
        "es": "Puente de Internet, KVM y Archivos con un Clic para Windows y Linux",
        "fr": "Passerelle Internet, KVM et Fichiers en un Clic pour Windows & Linux",
        "it": "Bridge Internet, KVM e File con un Clic per Windows e Linux",
    },
    "hero_hint_off": {
        "tr": "Windows PC'nin internete çıkması için aşağıdaki düğmeye basın.",
        "en": "Press the button below to grant internet access to Windows PC.",
        "de": "Drücken Sie die Taste unten, um dem Windows-PC Internetzugriff zu gewähren.",
        "es": "Presione el botón de abajo para dar acceso a Internet a la PC con Windows.",
        "fr": "Appuyez sur le bouton ci-dessous pour donner accès à Internet au PC Windows.",
        "it": "Premi il pulsante qui sotto per consentire l'accesso a Internet al PC Windows.",
    },
    "hero_hint_on": {
        "tr": "İnternet paylaşımı aktif. Windows PC Ethernet üzerinden bağlı.",
        "en": "Internet sharing is active. Windows PC is connected via Ethernet.",
        "de": "Internetfreigabe ist aktiv. Windows-PC ist über Ethernet verbunden.",
        "es": "Compartir Internet está activo. La PC con Windows está conectada por Ethernet.",
        "fr": "Le partage Internet est actif. Le PC Windows est connecté via Ethernet.",
        "it": "La condivisione Internet è attiva. Il PC Windows è connesso via Ethernet.",
    },
    "state_off": {
        "tr": "Paylaşım Kapalı",
        "en": "Sharing Off",
        "de": "Freigabe Aus",
        "es": "Compartir Desactivado",
        "fr": "Partage Désactivé",
        "it": "Condivisione Disattivata",
    },
    "state_on": {
        "tr": "Paylaşım Açık",
        "en": "Sharing Active",
        "de": "Freigabe Aktiv",
        "es": "Compartir Activo",
        "fr": "Partage Actif",
        "it": "Condivisione Attiva",
    },
    "btn_enable": {
        "tr": "İnternet Paylaşımını Aç",
        "en": "Turn On Internet Sharing",
        "de": "Internetfreigabe Einschalten",
        "es": "Activar Compartir Internet",
        "fr": "Activer le Partage Internet",
        "it": "Attiva Condivisione Internet",
    },
    "btn_disable": {
        "tr": "İnternet Paylaşımını Kapat",
        "en": "Turn Off Internet Sharing",
        "de": "Internetfreigabe Ausschalten",
        "es": "Desactivar Compartir Internet",
        "fr": "Désactiver le Partage Internet",
        "it": "Disattiva Condivisione Internet",
    },
    "btn_busy": {
        "tr": "İşleniyor...",
        "en": "Processing...",
        "de": "Verarbeitung...",
        "es": "Procesando...",
        "fr": "Traitement...",
        "it": "Elaborazione...",
    },
    "card_mouse_title": {
        "tr": "Mouse ve Klavye (KVM)",
        "en": "Mouse & Keyboard (KVM)",
        "de": "Maus & Tastatur (KVM)",
        "es": "Ratón y Teclado (KVM)",
        "fr": "Souris & Clavier (KVM)",
        "it": "Mouse e Tastiera (KVM)",
    },
    "card_mouse_sub": {
        "tr": "İmleci ekran kenarına götürünce Windows'a geçer",
        "en": "Moves pointer to Windows when pushed to screen edge",
        "de": "Bewegt den Mauszeiger zu Windows am Bildschirmrand",
        "es": "Mueve el puntero a Windows al tocar el borde de la pantalla",
        "fr": "Déplace le pointeur vers Windows au bord de l'écran",
        "it": "Sposta il puntatore su Windows toccando il bordo dello schermo",
    },
    "card_files_title": {
        "tr": "Dosya Paylaşımı (Web & Ağ)",
        "en": "File Sharing (Web & Network)",
        "de": "Dateifreigabe (Web & Netzwerk)",
        "es": "Compartir Archivos (Web y Red)",
        "fr": "Partage de Fichiers (Web & Réseau)",
        "it": "Condivisione File (Web e Rete)",
    },
    "card_files_sub": {
        "tr": "Tarayıcıdan ve Windows Gezgininden hızlı transfer",
        "en": "Fast transfer from browser and Windows Explorer",
        "de": "Schnelle Übertragung über Browser und Windows-Explorer",
        "es": "Transferencia rápida desde el navegador y el Explorador de Windows",
        "fr": "Transfert rapide depuis le navigateur et l'Explorateur Windows",
        "it": "Trasferimento rapido da browser e da Esplora File di Windows",
    },
    "edge_label": {
        "tr": "Windows ekran konumu:",
        "en": "Windows screen position:",
        "de": "Windows-Bildschirmposition:",
        "es": "Posición de pantalla de Windows:",
        "fr": "Position de l'écran Windows :",
        "it": "Posizione dello schermo Windows:",
    },
    "edge_left": {
        "tr": "Sol",
        "en": "Left",
        "de": "Links",
        "es": "Izquierda",
        "fr": "Gauche",
        "it": "Sinistra",
    },
    "edge_right": {
        "tr": "Sağ",
        "en": "Right",
        "de": "Rechts",
        "es": "Derecha",
        "fr": "Droite",
        "it": "Destra",
    },
    "edge_up": {
        "tr": "Üst",
        "en": "Top",
        "de": "Oben",
        "es": "Arriba",
        "fr": "Haut",
        "it": "In alto",
    },
    "edge_down": {
        "tr": "Alt",
        "en": "Bottom",
        "de": "Unten",
        "es": "Abajo",
        "fr": "Bas",
        "it": "In basso",
    },
    "btn_show_win_setup": {
        "tr": "Windows Kurulumunu Göster",
        "en": "Show Windows Setup",
        "de": "Windows-Einrichtung anzeigen",
        "es": "Mostrar Configuración de Windows",
        "fr": "Afficher la Configuration Windows",
        "it": "Mostra Configurazione Windows",
    },
    "btn_open_folder": {
        "tr": "Klasörü Aç",
        "en": "Open Folder",
        "de": "Ordner Öffnen",
        "es": "Abrir Carpeta",
        "fr": "Ouvrir le Dossier",
        "it": "Apri Cartella",
    },
    "btn_copy_url": {
        "tr": "Kopyala",
        "en": "Copy",
        "de": "Kopieren",
        "es": "Copiar",
        "fr": "Copier",
        "it": "Copia",
    },
    "btn_copied": {
        "tr": "Kopyalandı!",
        "en": "Copied!",
        "de": "Kopiert!",
        "es": "¡Copiado!",
        "fr": "Copié !",
        "it": "Copiato!",
    },
    "wifi_access_label": {
        "tr": "Wi-Fi cihazlarına da aç (Telefon vb.)",
        "en": "Allow Wi-Fi devices (Phone, etc.)",
        "de": "WLAN-Geräte zulassen (Telefon usw.)",
        "es": "Permitir dispositivos Wi-Fi (Teléfono, etc.)",
        "fr": "Autoriser les appareils Wi-Fi (Téléphone, etc.)",
        "it": "Consenti dispositivi Wi-Fi (Telefono, ecc.)",
    },
    "mouse_wifi_label": {
        "tr": "Wi-Fi üzerinden de dinle (Yedek bağlantı)",
        "en": "Listen over Wi-Fi as well (Fallback)",
        "de": "Auch über WLAN lauschen (Fallback)",
        "es": "Escuchar también por Wi-Fi (Respaldo)",
        "fr": "Écouter également sur Wi-Fi (Secours)",
        "it": "Ascolta anche via Wi-Fi (Backup)",
    },
    "details_title": {
        "tr": "Bağlantı ve Donanım Bilgileri",
        "en": "Connection & Hardware Details",
        "de": "Verbindungs- und Hardwaredetails",
        "es": "Detalles de Conexión y Hardware",
        "fr": "Détails de Connexion et Matériel",
        "it": "Dettagli Connessione e Hardware",
    },
    "lbl_cable": {
        "tr": "Ethernet Kablosu",
        "en": "Ethernet Cable",
        "de": "Ethernet-Kabel",
        "es": "Cable Ethernet",
        "fr": "Câble Ethernet",
        "it": "Cavo Ethernet",
    },
    "lbl_speed": {
        "tr": "Hat Hızı",
        "en": "Link Speed",
        "de": "Verbindungsgeschwindigkeit",
        "es": "Velocidad de Enlace",
        "fr": "Vitesse de Liaison",
        "it": "Velocità di Collegamento",
    },
    "lbl_iface": {
        "tr": "Ağ Kartı",
        "en": "Network Card",
        "de": "Netzwerkkarte",
        "es": "Tarjeta de Red",
        "fr": "Carte Réseau",
        "it": "Scheda di Rete",
    },
    "lbl_ip": {
        "tr": "Linux IP Adresi",
        "en": "Linux IP Address",
        "de": "Linux-IP-Adresse",
        "es": "Dirección IP de Linux",
        "fr": "Adresse IP Linux",
        "it": "Indirizzo IP Linux",
    },
    "lbl_wifi": {
        "tr": "Wi-Fi Ağı",
        "en": "Wi-Fi Network",
        "de": "WLAN-Netzwerk",
        "es": "Red Wi-Fi",
        "fr": "Réseau Wi-Fi",
        "it": "Rete Wi-Fi",
    },
    "lbl_clients": {
        "tr": "Bağlı Cihazlar (DHCP)",
        "en": "Connected Clients (DHCP)",
        "de": "Verbundene Clients (DHCP)",
        "es": "Clientes Conectados (DHCP)",
        "fr": "Clients Connectés (DHCP)",
        "it": "Dispositivi Connessi (DHCP)",
    },
    "lbl_samba": {
        "tr": "Windows Dosya Gezgini (SMB)",
        "en": "Windows File Explorer (SMB)",
        "de": "Windows-Datei-Explorer (SMB)",
        "es": "Explorador de Windows (SMB)",
        "fr": "Explorateur Windows (SMB)",
        "it": "Esplora File di Windows (SMB)",
    },
    "status_plugged": {
        "tr": "Bağlı",
        "en": "Connected",
        "de": "Verbunden",
        "es": "Conectado",
        "fr": "Connecté",
        "it": "Connesso",
    },
    "status_unplugged": {
        "tr": "Kablo Takılı Değil",
        "en": "Cable Unplugged",
        "de": "Kabel nicht eingesteckt",
        "es": "Cable Desconectado",
        "fr": "Câble Débranché",
        "it": "Cavo Non Collegato",
    },
    "status_running": {
        "tr": "Açık · Çalışıyor",
        "en": "Active · Running",
        "de": "Aktiv · Läuft",
        "es": "Activo · Ejecutándose",
        "fr": "Actif · En cours",
        "it": "Attivo · In esecuzione",
    },
    "status_waiting": {
        "tr": "İnternet paylaşımı bekleniyor",
        "en": "Waiting for internet sharing",
        "de": "Warten auf Internetfreigabe",
        "es": "Esperando conexión compartida",
        "fr": "En attente du partage Internet",
        "it": "In attesa della condivisione Internet",
    },
    "status_win_connected": {
        "tr": "Windows bağlı",
        "en": "Windows connected",
        "de": "Windows verbunden",
        "es": "Windows conectado",
        "fr": "Windows connecté",
        "it": "Windows connesso",
    },
    "status_win_waiting": {
        "tr": "Windows bağlantısı bekleniyor",
        "en": "Waiting for Windows connection",
        "de": "Warten auf Windows-Verbindung",
        "es": "Esperando conexión de Windows",
        "fr": "En attente de connexion Windows",
        "it": "In attesa di connessione da Windows",
    },
    "status_stopped": {
        "tr": "Kapalı",
        "en": "Disabled",
        "de": "Deaktiviert",
        "es": "Desactivado",
        "fr": "Désactivé",
        "it": "Disattivato",
    },
    "btn_help": {
        "tr": "Yardım",
        "en": "Help",
        "de": "Hilfe",
        "es": "Ayuda",
        "fr": "Aide",
        "it": "Aiuto",
    },
    "help_title": {
        "tr": "Ramord Link - Kullanım Rehberi",
        "en": "Ramord Link - User Guide",
        "de": "Ramord Link - Benutzerhandbuch",
        "es": "Ramord Link - Guía de Usuario",
        "fr": "Ramord Link - Guide d'Utilisation",
        "it": "Ramord Link - Guida Utente",
    },
    "help_text": {
        "tr": "1) İnternet Paylaşımı:\n"
              "Ethernet kablosunu iki bilgisayar arasına takın ve üstteki düğmeyi açın. Windows otomatik IP alıp internete çıkar.\n\n"
              "2) Mouse & Klavye (KVM):\n"
              "Windows PC'nize Deskflow (deskflow.org) kurun, Client modunda 192.168.50.1 sunucusuna bağlayın. İmleci kenara sürükleyerek Windows'u yönetebilirsiniz.\n\n"
              "3) Dosya Paylaşımı:\n"
              "Web sunucusunu açarak tarayıcıdan sürükle-bırak ile dosya aktarın veya Windows Dosya Gezgini'ne SMB adresini yapıştırın.\n\n"
              "Resmi Destek: ramordhelp@gmail.com",
        "en": "1) Internet Sharing:\n"
              "Plug Ethernet cable between PCs and click the top button. Windows PC automatically acquires IP and accesses the Internet.\n\n"
              "2) Mouse & Keyboard (KVM):\n"
              "Install Deskflow on Windows (deskflow.org), set to Client mode, and connect to 192.168.50.1. Move pointer to screen edge to control Windows.\n\n"
              "3) File Sharing:\n"
              "Turn on file server to transfer files via drag-and-drop in browser or paste the SMB address into Windows File Explorer.\n\n"
              "Official Support: ramordhelp@gmail.com",
        "de": "1) Internetfreigabe:\n"
              "Verbinden Sie die PCs mit einem Ethernet-Kabel und aktivieren Sie die Freigabe. Der Windows-PC erhält automatisch eine IP.\n\n"
              "2) Maus & Tastatur (KVM):\n"
              "Installieren Sie Deskflow unter Windows, Client-Modus aktivieren und mit 192.168.50.1 verbinden.\n\n"
              "3) Dateifreigabe:\n"
              "Aktivieren Sie den Dateiserver für Web-Drag-and-Drop oder nutzen Sie die SMB-Adresse im Windows-Explorer.\n\n"
              "Offizieller Support: ramordhelp@gmail.com",
        "es": "1) Compartir Internet:\n"
              "Conecte el cable Ethernet y active el botón superior. La PC con Windows obtendrá IP y conexión a Internet.\n\n"
              "2) Ratón y Teclado (KVM):\n"
              "Instale Deskflow en Windows, modo Cliente y conéctese a 192.168.50.1. Mueva el cursor al borde para controlar Windows.\n\n"
              "3) Compartir Archivos:\n"
              "Abra el servidor web para arrastrar y soltar archivos o use la ruta SMB en el Explorador de Windows.\n\n"
              "Soporte Oficial: ramordhelp@gmail.com",
        "fr": "1) Partage Internet :\n"
              "Branchez le câble Ethernet entre les PC et activez le partage. Windows acquiert automatiquement une IP.\n\n"
              "2) Souris & Clavier (KVM) :\n"
              "Installez Deskflow sur Windows, activez le mode Client et connectez-vous à 192.168.50.1.\n\n"
              "3) Partage de Fichiers :\n"
              "Activez le serveur web pour glisser-déposer des fichiers ou utilisez l'adresse SMB dans l'Explorateur Windows.\n\n"
              "Support Officiel : ramordhelp@gmail.com",
        "it": "1) Condivisione Internet:\n"
              "Collega il cavo Ethernet e attiva il pulsante in alto. Windows riceverà automaticamente l'IP e navigherà in rete.\n\n"
              "2) Mouse e Tastiera (KVM):\n"
              "Installa Deskflow su Windows, modalità Client e connettiti a 192.168.50.1. Sposta il cursore sul bordo per controllare Windows.\n\n"
              "3) Condivisione File:\n"
              "Attiva il server per trasferire file via browser o incolla l'indirizzo SMB in Esplora File.\n\n"
              "Supporto Ufficiale: ramordhelp@gmail.com",
    },
    "tray_toggle_on": {
        "tr": "İnternet Paylaşımını Kapat",
        "en": "Turn Off Internet Sharing",
        "de": "Internetfreigabe Beenden",
        "es": "Desactivar Compartir Internet",
        "fr": "Arrêter le Partage Internet",
        "it": "Arresta Condivisione Internet",
    },
    "tray_toggle_off": {
        "tr": "İnternet Paylaşımını Aç",
        "en": "Turn On Internet Sharing",
        "de": "Internetfreigabe Starten",
        "es": "Activar Compartir Internet",
        "fr": "Démarrer le Partage Internet",
        "it": "Avvia Condivisione Internet",
    },
    "tray_quit": {
        "tr": "Çıkış",
        "en": "Quit",
        "de": "Beenden",
        "es": "Salir",
        "fr": "Quitter",
        "it": "Esci",
    },
    "web_title": {
        "tr": "Ramord Link - Dosya Paylaşımı",
        "en": "Ramord Link - File Sharing",
        "de": "Ramord Link - Dateifreigabe",
        "es": "Ramord Link - Compartir Archivos",
        "fr": "Ramord Link - Partage de Fichiers",
        "it": "Ramord Link - Condivisione File",
    },
    "web_drop": {
        "tr": "Dosyaları buraya sürükleyin veya tıklayarak seçin",
        "en": "Drag files here or click to browse",
        "de": "Dateien hierher ziehen oder zum Auswählen klicken",
        "es": "Arrastre archivos aquí o haga clic para seleccionar",
        "fr": "Glissez les fichiers ici ou cliquez pour parcourir",
        "it": "Trascina i file qui o clicca per sfogliare",
    },
    "web_uploading": {
        "tr": "Yükleniyor:",
        "en": "Uploading:",
        "de": "Wird hochgeladen:",
        "es": "Subiendo:",
        "fr": "Téléversement :",
        "it": "Caricamento:",
    },
    "web_done": {
        "tr": "Yükleme tamamlandı",
        "en": "Upload complete",
        "de": "Upload abgeschlossen",
        "es": "Subida completada",
        "fr": "Téléversement terminé",
        "it": "Caricamento completato",
    },
    "web_file": {
        "tr": "Dosya",
        "en": "File",
        "de": "Datei",
        "es": "Archivo",
        "fr": "Fichier",
        "it": "File",
    },
    "web_size": {
        "tr": "Boyut",
        "en": "Size",
        "de": "Größe",
        "es": "Tamaño",
        "fr": "Taille",
        "it": "Dimensione",
    },
    "web_date": {
        "tr": "Tarih",
        "en": "Date",
        "de": "Datum",
        "es": "Fecha",
        "fr": "Date",
        "it": "Data",
    },
    "web_empty": {
        "tr": "Henüz paylaşılan dosya yok",
        "en": "No shared files yet",
        "de": "Noch keine freigegebenen Dateien",
        "es": "Aún no hay archivos compartidos",
        "fr": "Aucun fichier partagé pour le moment",
        "it": "Nessun file condiviso al momento",
    },
}

CURRENT_LANG = "tr"


def detect_system_language() -> str:
    """Detects system language and falls back gracefully."""
    for env in ("LC_ALL", "LC_MESSAGES", "LANG"):
        val = os.environ.get(env, "")
        if val:
            prefix = val.split(".")[0].split("_")[0].lower()
            if prefix in LANGUAGES:
                return prefix
    try:
        loc = locale.getdefaultlocale()[0]
        if loc:
            prefix = loc.split("_")[0].lower()
            if prefix in LANGUAGES:
                return prefix
    except Exception:
        pass
    return "en"


def get_lang() -> str:
    global CURRENT_LANG
    return CURRENT_LANG


def set_lang(lang_code: str) -> None:
    global CURRENT_LANG
    if lang_code in LANGUAGES:
        CURRENT_LANG = lang_code


def t(key: str, lang: str | None = None) -> str:
    target_lang = lang or CURRENT_LANG
    entry = TRANSLATIONS.get(key, {})
    return entry.get(target_lang, entry.get("en", entry.get("tr", key)))
