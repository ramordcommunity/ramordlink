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
    # Hotspot (Wireless AP) Translations
    "card_hotspot_title": {
        "tr": "Kablosuz Wi-Fi Hotspot",
        "en": "Wireless Wi-Fi Hotspot",
        "de": "Drahtloser Wi-Fi-Hotspot",
        "es": "Punto de Acceso Wi-Fi Inalámbrico",
        "fr": "Point d'Accès Wi-Fi Sans Fil",
        "it": "Hotspot Wi-Fi Wireless",
    },
    "hotspot_off": {
        "tr": "Hotspot Kapalı",
        "en": "Hotspot Off",
        "de": "Hotspot Aus",
        "es": "Punto de Acceso Desactivado",
        "fr": "Point d'Accès Désactivé",
        "it": "Hotspot Disattivato",
    },
    "hotspot_on": {
        "tr": "Hotspot Yayında",
        "en": "Hotspot Active",
        "de": "Hotspot Aktiv",
        "es": "Punto de Acceso Activo",
        "fr": "Point d'Accès Actif",
        "it": "Hotspot Attivo",
    },
    "hotspot_not_supported": {
        "tr": "Wi-Fi kartınız AP (Hotspot) modunu desteklemiyor",
        "en": "Your Wi-Fi card does not support AP (Hotspot) mode",
        "de": "Ihre Wi-Fi-Karte unterstützt den AP-Modus nicht",
        "es": "Su tarjeta Wi-Fi no admite el modo AP (Hotspot)",
        "fr": "Votre carte Wi-Fi ne prend pas en charge le mode AP",
        "it": "La scheda Wi-Fi non supporta la modalità AP",
    },
    "hotspot_ssid": {
        "tr": "Ağ Adı (SSID)",
        "en": "Network Name (SSID)",
        "de": "Netzwerkname (SSID)",
        "es": "Nombre de Red (SSID)",
        "fr": "Nom du Réseau (SSID)",
        "it": "Nome Rete (SSID)",
    },
    "hotspot_password": {
        "tr": "Şifre",
        "en": "Password",
        "de": "Passwort",
        "es": "Contraseña",
        "fr": "Mot de Passe",
        "it": "Password",
    },
    "hotspot_btn_enable": {
        "tr": "Hotspot Başlat",
        "en": "Start Hotspot",
        "de": "Hotspot Starten",
        "es": "Iniciar Punto de Acceso",
        "fr": "Démarrer le Point d'Accès",
        "it": "Avvia Hotspot",
    },
    "hotspot_btn_disable": {
        "tr": "Hotspot Durdur",
        "en": "Stop Hotspot",
        "de": "Hotspot Stoppen",
        "es": "Detener Punto de Acceso",
        "fr": "Arrêter le Point d'Accès",
        "it": "Arresta Hotspot",
    },
    "hotspot_hint": {
        "tr": "Bilgisayarınızı kablosuz modeme dönüştürerek telefon ve diğer PC'lerin internete kablosuz bağlanmasını sağlar.",
        "en": "Turns your computer into a wireless router, allowing phones and other PCs to access the internet via Wi-Fi.",
        "de": "Verwandelt Ihren Computer in einen WLAN-Router für Telefone und andere PCs.",
        "es": "Convierte tu computadora en un router inalámbrico para compartir Internet por Wi-Fi.",
        "fr": "Transforme votre ordinateur en routeur sans fil pour partager Internet via Wi-Fi.",
        "it": "Trasforma il computer in un router wireless per condividere Internet via Wi-Fi.",
    },
    "err_hotspot_start": {
        "tr": "Hotspot başlatılamadı",
        "en": "Failed to start hotspot",
        "de": "Hotspot konnte nicht gestartet werden",
        "es": "No se pudo iniciar el punto de acceso",
        "fr": "Échec du démarrage du point d'accès",
        "it": "Impossibile avviare l'hotspot",
    },
    "err_hotspot_stop": {
        "tr": "Hotspot durdurulamadı",
        "en": "Failed to stop hotspot",
        "de": "Hotspot konnte nicht gestoppt werden",
        "es": "No se pudo detener el punto de acceso",
        "fr": "Échec de l'arrêt du point d'accès",
        "it": "Impossibile arrestare l'hotspot",
    },
    # Buttons & Actions
    "btn_copy": {
        "tr": "Kopyala",
        "en": "Copy",
        "de": "Kopieren",
        "es": "Copiar",
        "fr": "Copier",
        "it": "Copia",
    },
    "btn_copy_address": {
        "tr": "Adresi Kopyala",
        "en": "Copy Address",
        "de": "Adresse Kopieren",
        "es": "Copiar Dirección",
        "fr": "Copier l'Adresse",
        "it": "Copia Indirizzo",
    },
    "btn_refresh": {
        "tr": "Yenile",
        "en": "Refresh",
        "de": "Aktualisieren",
        "es": "Actualizar",
        "fr": "Actualiser",
        "it": "Aggiorna",
    },
    "btn_quit": {
        "tr": "Çıkış",
        "en": "Quit",
        "de": "Beenden",
        "es": "Salir",
        "fr": "Quitter",
        "it": "Esci",
    },
    "autostart": {
        "tr": "Açılışta Başlat",
        "en": "Start on Boot",
        "de": "Beim Start ausführen",
        "es": "Iniciar al arrancar",
        "fr": "Démarrer au lancement",
        "it": "Avvia all'avvio",
    },
    # Wi-Fi & File Access Explanations
    "wifi_files_title": {
        "tr": "Yerel Ağdan (Wi-Fi) Dosya Erişimi",
        "en": "Local Network (Wi-Fi) File Access",
        "de": "Lokaler Netzwerk- (Wi-Fi) Dateizugriff",
        "es": "Acceso a Archivos por Red Local (Wi-Fi)",
        "fr": "Accès aux Fichiers via Réseau Local (Wi-Fi)",
        "it": "Accesso ai File da Rete Locale (Wi-Fi)",
    },
    "wifi_files_desc": {
        "tr": "Aynı Wi-Fi ağına bağlı telefon ve bilgisayarların tarayıcıdan dosya alıp göndermesine izin ver.",
        "en": "Allow phones and computers on the same Wi-Fi network to upload and download files via browser.",
        "de": "Erlauben Sie Telefonen und PCs im selben Wi-Fi den Dateitransfer über den Browser.",
        "es": "Permitir que teléfonos y PC en la misma red Wi-Fi transfieran archivos por el navegador.",
        "fr": "Autoriser les téléphones et PC sur le même réseau Wi-Fi à transférer des fichiers via navigateur.",
        "it": "Consenti a telefoni e PC sulla stessa rete Wi-Fi di trasferire file tramite browser.",
    },
    "wifi_access_title": {
        "tr": "Wi-Fi Üzerinden KVM Bağlantısı",
        "en": "KVM Connection via Wi-Fi",
        "de": "KVM-Verbindung über Wi-Fi",
        "es": "Conexión KVM por Wi-Fi",
        "fr": "Connexion KVM via Wi-Fi",
        "it": "Connessione KVM tramite Wi-Fi",
    },
    "wifi_access_desc": {
        "tr": "Aynı Wi-Fi ağındaki ikinci bilgisayarın kablosuz olarak fare ve klavyenize bağlanmasını sağlar.",
        "en": "Allows a secondary PC on the same Wi-Fi to connect to your mouse & keyboard wirelessly.",
        "de": "Ermöglicht einem zweiten PC im selben Wi-Fi die kabellose Maus- und Tastaturverbindung.",
        "es": "Permite que una segunda PC en el mismo Wi-Fi se conecte al ratón y teclado de forma inalámbrica.",
        "fr": "Permet à un second PC sur le même réseau Wi-Fi de se connecter sans fil à la souris et au clavier.",
        "it": "Consente a un secondo PC sulla stessa rete Wi-Fi di connettersi senza fili a mouse e tastiera.",
    },
    # Statuses
    "files_active": {
        "tr": "Açık · Tarayıcıdan erişilebilir",
        "en": "Active · Accessible via browser",
        "de": "Aktiv · Über Browser erreichbar",
        "es": "Activo · Accesible desde el navegador",
        "fr": "Actif · Accessible via navigateur",
        "it": "Attivo · Accessibile da browser",
    },
    "files_off": {
        "tr": "Kapalı",
        "en": "Off",
        "de": "Aus",
        "es": "Desactivado",
        "fr": "Désactivé",
        "it": "Disattivato",
    },
    "files_waiting_sharing": {
        "tr": "İnternet paylaşımı bekleniyor",
        "en": "Waiting for internet sharing",
        "de": "Warten auf Internetfreigabe",
        "es": "Esperando que se comparta Internet",
        "fr": "En attente du partage Internet",
        "it": "In attesa della condivisione Internet",
    },
    "mouse_connected": {
        "tr": "İkinci PC Bağlı",
        "en": "Secondary PC Connected",
        "de": "Zweiter PC Verbunden",
        "es": "Segunda PC Conectada",
        "fr": "Second PC Connecté",
        "it": "Secondo PC Connesso",
    },
    "mouse_waiting": {
        "tr": "İkinci PC Bekleniyor",
        "en": "Waiting for Secondary PC",
        "de": "Warten auf zweiten PC",
        "es": "Esperando segunda PC",
        "fr": "En attente du second PC",
        "it": "In attesa del secondo PC",
    },
    "mouse_waiting_sharing": {
        "tr": "İnternet paylaşımı bekleniyor",
        "en": "Waiting for internet sharing",
        "de": "Warten auf Internetfreigabe",
        "es": "Esperando que se comparta Internet",
        "fr": "En attente du partage Internet",
        "it": "In attesa della condivisione Internet",
    },
    "mouse_off": {
        "tr": "Kapalı",
        "en": "Off",
        "de": "Aus",
        "es": "Desactivado",
        "fr": "Désactivé",
        "it": "Disattivato",
    },
    "mouse_not_installed": {
        "tr": "Deskflow kurulu değil",
        "en": "Deskflow not installed",
        "de": "Deskflow nicht installiert",
        "es": "Deskflow no está instalado",
        "fr": "Deskflow non installé",
        "it": "Deskflow non installato",
    },
    "mouse_install_guide": {
        "tr": "Deskflow KVM paketini kurmak için sistem paket yöneticinizi kullanın.",
        "en": "Use your system package manager to install the Deskflow KVM package.",
        "de": "Verwenden Sie Ihren Paketmanager, um das Deskflow KVM-Paket zu installieren.",
        "es": "Use el administrador de paquetes del sistema para instalar Deskflow KVM.",
        "fr": "Utilisez le gestionnaire de paquets de votre système pour installer Deskflow KVM.",
        "it": "Usa il gestore pacchetti di sistema per installare Deskflow KVM.",
    },
    "cable_connected": {
        "tr": "Kablo Bağlı",
        "en": "Cable Connected",
        "de": "Kabel Verbunden",
        "es": "Cable Conectado",
        "fr": "Câble Connecté",
        "it": "Cavo Connesso",
    },
    "cable_disconnected": {
        "tr": "Kablo takılı değil",
        "en": "Cable disconnected",
        "de": "Kabel nicht eingesteckt",
        "es": "Cable no conectado",
        "fr": "Câble non branché",
        "it": "Cavo non collegato",
    },
    "no_clients": {
        "tr": "Bağlı istemci yok",
        "en": "No connected clients",
        "de": "Keine verbundenen Clients",
        "es": "No hay clientes conectados",
        "fr": "Aucun client connecté",
        "it": "Nessun client connesso",
    },
    # UI Labels & Prompts
    "lbl_select_iface": {
        "tr": "Paylaşılacak Ethernet Kartı:",
        "en": "Ethernet Card to Share:",
        "de": "Zu teilende Ethernet-Karte:",
        "es": "Tarjeta Ethernet a Compartir:",
        "fr": "Carte Ethernet à Partager :",
        "it": "Scheda Ethernet da Condividere:",
    },
    "edge_question": {
        "tr": "İkinci Bilgisayar Hangi Kenarda?",
        "en": "Which Edge is the Secondary PC On?",
        "de": "An welchem Rand befindet sich der zweite PC?",
        "es": "¿En qué borde está la segunda PC?",
        "fr": "Sur quel bord se trouve le second PC ?",
        "it": "Su quale bordo si trova il secondo PC?",
    },
    "edge_hint": {
        "tr": "Fareyi seçtiğiniz kenarın dışına doğru sürdüğünüzde otomatik olarak diğer bilgisayarın ekranına geçer.",
        "en": "Moving the mouse cursor past the selected screen edge moves control seamlessly to the secondary PC.",
        "de": "Wenn Sie die Maus über den gewählten Rand bewegen, wechselt die Steuerung zum zweiten PC.",
        "es": "Mover el cursor más allá del borde seleccionado transfiere el control a la segunda PC.",
        "fr": "Déplacer la souris au-delà du bord sélectionné bascule le contrôle vers le second PC.",
        "it": "Spostando il cursore oltre il bordo selezionato, il controllo passa all'altro PC.",
    },
    "info_ethernet": {
        "tr": "Ethernet Durumu",
        "en": "Ethernet Status",
        "de": "Ethernet-Status",
        "es": "Estado de Ethernet",
        "fr": "État Ethernet",
        "it": "Stato Ethernet",
    },
    "info_client_pc": {
        "tr": "Kablodaki Cihazlar",
        "en": "Connected Devices",
        "de": "Verbundene Geräte",
        "es": "Dispositivos Conectados",
        "fr": "Appareils Connectés",
        "it": "Dispositivi Connessi",
    },
    "info_wifi": {
        "tr": "Mevcut Wi-Fi",
        "en": "Current Wi-Fi",
        "de": "Aktuelles Wi-Fi",
        "es": "Wi-Fi Actual",
        "fr": "Wi-Fi Actuel",
        "it": "Wi-Fi Attuale",
    },
    "info_gateway": {
        "tr": "Ağ Geçidi / DHCP",
        "en": "Gateway / DHCP",
        "de": "Gateway / DHCP",
        "es": "Puerta de Enlace / DHCP",
        "fr": "Passerelle / DHCP",
        "it": "Gateway / DHCP",
    },
    "info_folder": {
        "tr": "Paylaşılan Klasör",
        "en": "Shared Folder",
        "de": "Freigegebener Ordner",
        "es": "Carpeta Compartida",
        "fr": "Dossier Partagé",
        "it": "Cartella Condivisa",
    },
    "info_addresses": {
        "tr": "Erişim Adresleri",
        "en": "Access Addresses",
        "de": "Zugriffsadressen",
        "es": "Direcciones de Acceso",
        "fr": "Adresses d'Accès",
        "it": "Indirizzi di Accesso",
    },
    "addr_cable": {
        "tr": "Kablo (Web)",
        "en": "Cable (Web)",
        "de": "Kabel (Web)",
        "es": "Cable (Web)",
        "fr": "Câble (Web)",
        "it": "Cavo (Web)",
    },
    "addr_wifi": {
        "tr": "Wi-Fi (Web)",
        "en": "Wi-Fi (Web)",
        "de": "Wi-Fi (Web)",
        "es": "Wi-Fi (Web)",
        "fr": "Wi-Fi (Web)",
        "it": "Wi-Fi (Web)",
    },
    "addr_smb": {
        "tr": "Ağ Klasörü (SMB)",
        "en": "Network Folder (SMB)",
        "de": "Netzwerkordner (SMB)",
        "es": "Carpeta de Red (SMB)",
        "fr": "Dossier Réseau (SMB)",
        "it": "Cartella di Rete (SMB)",
    },
    # Tray Items
    "tray_enable": {
        "tr": "İnternet Paylaşımını Aç",
        "en": "Turn On Internet Sharing",
        "de": "Internetfreigabe Aktivieren",
        "es": "Activar Compartir Internet",
        "fr": "Activer le Partage Internet",
        "it": "Attiva Condivisione Internet",
    },
    "tray_disable": {
        "tr": "İnternet Paylaşımını Kapat",
        "en": "Turn Off Internet Sharing",
        "de": "Internetfreigabe Deaktivieren",
        "es": "Desactivar Compartir Internet",
        "fr": "Désactiver le Partage Internet",
        "it": "Disattiva Condivisione Internet",
    },
    "tray_mouse_enable": {
        "tr": "Mouse Paylaşımını Aç",
        "en": "Turn On Mouse Sharing",
        "de": "Mausfreigabe Aktivieren",
        "es": "Activar Compartir Ratón",
        "fr": "Activer le Partage Souris",
        "it": "Attiva Condivisione Mouse",
    },
    "tray_mouse_disable": {
        "tr": "Mouse Paylaşımını Kapat",
        "en": "Turn Off Mouse Sharing",
        "de": "Mausfreigabe Deaktivieren",
        "es": "Desactivar Compartir Ratón",
        "fr": "Désactiver le Partage Souris",
        "it": "Disattiva Condivisione Mouse",
    },
    "tray_files_enable": {
        "tr": "Dosya Paylaşımını Aç",
        "en": "Turn On File Sharing",
        "de": "Dateifreigabe Aktivieren",
        "es": "Activar Compartir Archivos",
        "fr": "Activer le Partage de Fichiers",
        "it": "Attiva Condivisione File",
    },
    "tray_files_disable": {
        "tr": "Dosya Paylaşımını Kapat",
        "en": "Turn Off File Sharing",
        "de": "Dateifreigabe Deaktivieren",
        "es": "Desactivar Compartir Archivos",
        "fr": "Désactiver le Partage de Fichiers",
        "it": "Disattiva Condivisione File",
    },
    "tray_show": {
        "tr": "Pencereyi Göster",
        "en": "Show Window",
        "de": "Fenster Anzeigen",
        "es": "Mostrar Ventana",
        "fr": "Afficher la Fenêtre",
        "it": "Mostra Finestra",
    },
    "tray_hint": {
        "tr": "Ramord Link arka planda sistem tepsisinde çalışmaya devam ediyor.",
        "en": "Ramord Link continues running in the background in system tray.",
        "de": "Ramord Link läuft im Hintergrund in der Taskleiste weiter.",
        "es": "Ramord Link continúa ejecutándose en segundo plano en la bandeja del sistema.",
        "fr": "Ramord Link continue de fonctionner en arrière-plan dans la barre d'état.",
        "it": "Ramord Link continua a funzionare in background nella barra delle applicazioni.",
    },
    # Windows Setup Dialog
    "win_setup_title": {
        "tr": "Windows Tarafı Kurulum Rehberi",
        "en": "Windows Setup Guide",
        "de": "Windows-Einrichtungsanleitung",
        "es": "Guía de Configuración de Windows",
        "fr": "Guide de Configuration Windows",
        "it": "Guida alla Configurazione di Windows",
    },
    "win_setup_step1": {
        "tr": "Windows PC'ye Deskflow kurun (deskflow.org/download).",
        "en": "Install Deskflow on Windows PC (deskflow.org/download).",
        "de": "Installieren Sie Deskflow auf dem Windows-PC (deskflow.org/download).",
        "es": "Instale Deskflow en la PC con Windows (deskflow.org/download).",
        "fr": "Installez Deskflow sur le PC Windows (deskflow.org/download).",
        "it": "Installa Deskflow sul PC Windows (deskflow.org/download).",
    },
    "win_setup_step2": {
        "tr": "Deskflow uygulamasını 'Client' (İstemci) modunda başlatın.",
        "en": "Start Deskflow in 'Client' mode.",
        "de": "Starten Sie Deskflow im 'Client'-Modus.",
        "es": "Inicie Deskflow en modo 'Cliente'.",
        "fr": "Démarrez Deskflow en mode 'Client'.",
        "it": "Avvia Deskflow in modalità 'Client'.",
    },
    "win_setup_step3": {
        "tr": "Sunucu IP adresi olarak şunu girin",
        "en": "Enter the following as the Server IP address",
        "de": "Geben Sie Folgendes als Server-IP-Adresse ein",
        "es": "Ingrese lo siguiente como dirección IP del servidor",
        "fr": "Entrez ce qui suit comme adresse IP du serveur",
        "it": "Inserisci il seguente indirizzo IP del server",
    },
    "win_setup_step4": {
        "tr": "Ekran adı (Screen name) olarak şunu yazın",
        "en": "Enter the following as Screen name",
        "de": "Geben Sie Folgendes als Computernamen ein",
        "es": "Ingrese lo siguiente como nombre de pantalla",
        "fr": "Entrez ce qui suit comme nom d'écran",
        "it": "Inserisci il seguente nome schermo",
    },
    "win_setup_step5": {
        "tr": "Güvenlik ayarlarında 'Use TLS encryption' seçeneğini kapalı tutun.",
        "en": "Keep 'Use TLS encryption' turned off in Security settings.",
        "de": "Lassen Sie 'Use TLS encryption' in den Sicherheitseinstellungen deaktiviert.",
        "es": "Mantenga desactivado 'Use TLS encryption' en Configuración de seguridad.",
        "fr": "Désactivez 'Use TLS encryption' dans les paramètres de sécurité.",
        "it": "Mantieni disattivato 'Use TLS encryption' nelle impostazioni di sicurezza.",
    },
    "win_setup_step6": {
        "tr": "'Start' düğmesine basın. Bağlanınca burada 'İkinci PC Bağlı' yazacaktır.",
        "en": "Press 'Start'. When connected, 'Secondary PC Connected' will appear here.",
        "de": "Drücken Sie 'Start'. Nach der Verbindung wird hier 'Zweiter PC Verbunden' angezeigt.",
        "es": "Presione 'Start'. Al conectarse, aparecerá aquí 'Segunda PC Conectada'.",
        "fr": "Cliquez sur 'Start'. Une fois connecté, 'Second PC Connecté' s'affichera ici.",
        "it": "Premi 'Start'. Una volta connesso, apparirà qui 'Secondo PC Connesso'.",
    },
    # Help Dialog
    "help_step1_title": {
        "tr": "İnternet Paylaşımı:",
        "en": "Internet Sharing:",
        "de": "Internetfreigabe:",
        "es": "Compartir Internet:",
        "fr": "Partage Internet :",
        "it": "Condivisione Internet:",
    },
    "help_step1_desc": {
        "tr": "Ethernet kablosuyla veya Wi-Fi Hotspot ile tek tıkla diğer cihazların internete çıkmasını sağlayın.",
        "en": "Allow other devices to access the internet via Ethernet cable or Wi-Fi Hotspot with one click.",
        "de": "Ermöglichen Sie anderen Geräten den Internetzugang über Ethernet oder WLAN-Hotspot mit einem Klick.",
        "es": "Permita que otros dispositivos accedan a Internet por Ethernet o Hotspot Wi-Fi con un clic.",
        "fr": "Permettez à d'autres appareils d'accéder à Internet par Ethernet ou Hotspot Wi-Fi en un clic.",
        "it": "Consenti ad altri dispositivi di accedere a Internet tramite Ethernet o Hotspot Wi-Fi con un clic.",
    },
    "help_step2_title": {
        "tr": "Mouse ve Klavye (KVM):",
        "en": "Mouse & Keyboard (KVM):",
        "de": "Maus & Tastatur (KVM):",
        "es": "Ratón y Teclado (KVM):",
        "fr": "Souris & Clavier (KVM) :",
        "it": "Mouse e Tastiera (KVM):",
    },
    "help_step2_desc": {
        "tr": "İkinci bilgisayara Deskflow kurup farenizi seçtiğiniz ekran kenarından doğrudan diğer ekrana geçirin.",
        "en": "Install Deskflow on the second PC and seamlessly move your mouse cursor across screen edges.",
        "de": "Installieren Sie Deskflow auf dem zweiten PC und bewegen Sie die Maus über den Bildschirmrand.",
        "es": "Instale Deskflow en la segunda PC y mueva el cursor suavemente entre las pantallas.",
        "fr": "Installez Deskflow sur le second PC et déplacez la souris de manière fluide entre les écrans.",
        "it": "Installa Deskflow sul secondo PC e sposta il cursore del mouse senza interruzioni tra gli schermi.",
    },
    "help_step3_title": {
        "tr": "Dosya Paylaşımı:",
        "en": "File Sharing:",
        "de": "Dateifreigabe:",
        "es": "Compartir Archivos:",
        "fr": "Partage de Fichiers :",
        "it": "Condivisione File:",
    },
    "help_step3_desc": {
        "tr": "Telefon ve bilgisayarlardan tarayıcı ile dosya yükleyip indirin veya SMB ağ klasörünü kullanın.",
        "en": "Upload and download files from phones and PCs via web browser or use the SMB network share.",
        "de": "Laden Sie Dateien von Telefonen und PCs per Webbrowser hoch/runter oder nutzen Sie die SMB-Freigabe.",
        "es": "Suba y descargue archivos desde teléfonos y PC mediante el navegador web o use la carpeta SMB.",
        "fr": "Téléversez et téléchargez des fichiers depuis téléphones et PC via navigateur ou utilisez le partage SMB.",
        "it": "Carica e scarica file da telefoni e PC tramite browser web o utilizza la condivisione di rete SMB.",
    },
    "help_contact": {
        "tr": "Resmi Destek: ramordhelp@gmail.com",
        "en": "Official Support: ramordhelp@gmail.com",
        "de": "Offizieller Support: ramordhelp@gmail.com",
        "es": "Soporte Oficial: ramordhelp@gmail.com",
        "fr": "Support Officiel : ramordhelp@gmail.com",
        "it": "Supporto Ufficiale: ramordhelp@gmail.com",
    },
    # Errors
    "err_sharing_start": {
        "tr": "İnternet paylaşımı başlatılamadı",
        "en": "Failed to start internet sharing",
        "de": "Internetfreigabe konnte nicht gestartet werden",
        "es": "No se pudo iniciar el uso compartido de Internet",
        "fr": "Échec du démarrage du partage Internet",
        "it": "Impossibile avviare la condivisione Internet",
    },
    "err_sharing_stop": {
        "tr": "İnternet paylaşımı durdurulamadı",
        "en": "Failed to stop internet sharing",
        "de": "Internetfreigabe konnte nicht gestoppt werden",
        "es": "No se pudo detener el uso compartido de Internet",
        "fr": "Échec de l'arrêt du partage Internet",
        "it": "Impossibile arrestare la condivisione Internet",
    },
    "err_start_sharing_first": {
        "tr": "Önce internet paylaşımını açın",
        "en": "Turn on internet sharing first",
        "de": "Aktivieren Sie zuerst die Internetfreigabe",
        "es": "Primero active el uso compartido de Internet",
        "fr": "Activez d'abord le partage Internet",
        "it": "Attiva prima la condivisione Internet",
    },
    "err_start_sharing_desc": {
        "tr": "Bu özelliğin çalışabilmesi için önce yukarıdaki 'İnternet Paylaşımını Aç' düğmesine basmalısınız.",
        "en": "To use this feature, please press 'Turn On Internet Sharing' above first.",
        "de": "Um diese Funktion zu nutzen, aktivieren Sie bitte zuerst die Internetfreigabe oben.",
        "es": "Para usar esta función, primero active el botón 'Activar Compartir Internet' arriba.",
        "fr": "Pour utiliser cette fonctionnalité, activez d'abord le partage Internet ci-dessus.",
        "it": "Per utilizzare questa funzione, premi prima il pulsante 'Attiva Condivisione Internet' in alto.",
    },
    "err_mouse_start": {
        "tr": "Mouse paylaşımı başlatılamadı",
        "en": "Failed to start mouse sharing",
        "de": "Mausfreigabe konnte nicht gestartet werden",
        "es": "No se pudo iniciar el uso compartido del ratón",
        "fr": "Échec du démarrage du partage de la souris",
        "it": "Impossibile avviare la condivisione del mouse",
    },
    "err_file_server": {
        "tr": "Dosya sunucusu başlatılamadı",
        "en": "Failed to start file server",
        "de": "Dateiserver konnte nicht gestartet werden",
        "es": "No se pudo iniciar el servidor de archivos",
        "fr": "Échec du démarrage du serveur de fichiers",
        "it": "Impossibile avviare il server di file",
    },
    # Tab selection for sharing
    "card_hero_title": {
        "tr": "İnternet Paylaşımı",
        "en": "Internet Sharing",
        "de": "Internetfreigabe",
        "es": "Compartir Internet",
        "fr": "Partage Internet",
        "it": "Condivisione Internet",
    },
    "tab_ethernet": {
        "tr": "Kablolu (Ethernet)",
        "en": "Wired (Ethernet)",
        "de": "Kabelgebunden (Ethernet)",
        "es": "Cableado (Ethernet)",
        "fr": "Filaire (Ethernet)",
        "it": "Cablato (Ethernet)",
    },
    "tab_wireless": {
        "tr": "Kablosuz (Wi-Fi Hotspot)",
        "en": "Wireless (Wi-Fi Hotspot)",
        "de": "Drahtlos (Wi-Fi-Hotspot)",
        "es": "Inalámbrico (Hotspot Wi-Fi)",
        "fr": "Sans Fil (Hotspot Wi-Fi)",
        "it": "Wireless (Hotspot Wi-Fi)",
    },
    "hero_hint_ethernet": {
        "tr": "Ethernet kablosuyla bağlı olan Windows PC veya diğer cihaza internet verin.",
        "en": "Share internet with the Windows PC or secondary device connected via Ethernet cable.",
        "de": "Geben Sie das Internet für den über Ethernet verbundenen PC frei.",
        "es": "Comparta Internet con la PC o dispositivo conectado por cable Ethernet.",
        "fr": "Partagez Internet avec le PC ou périphérique connecté par câble Ethernet.",
        "it": "Condividi Internet con il PC o dispositivo connesso tramite cavo Ethernet.",
    },
    "hero_hint_hotspot": {
        "tr": "Bilgisayarınızı kablosuz modeme dönüştürerek telefon ve diğer PC'lerin Wi-Fi ile bağlanmasını sağlayın.",
        "en": "Turn your computer into a Wi-Fi hotspot so phones and other PCs can connect wirelessly.",
        "de": "Verwandeln Sie Ihren PC in einen Wi-Fi-Hotspot für Telefone und andere PCs.",
        "es": "Convierta su PC en un punto de acceso Wi-Fi para conectar teléfonos y otras computadoras.",
        "fr": "Transformez votre PC en borne Wi-Fi pour connecter téléphones et autres PC.",
        "it": "Trasforma il tuo PC in un hotspot Wi-Fi per connettere telefoni e altri PC.",
    },
    # File Share Folder & Instructions
    "btn_change_folder": {
        "tr": "Klasörü Değiştir",
        "en": "Change Folder",
        "de": "Ordner Ändern",
        "es": "Cambiar Carpeta",
        "fr": "Changer de Dossier",
        "it": "Cambia Cartella",
    },
    "btn_show_win_files_guide": {
        "tr": "Windows'tan Nasıl Bağlanılır?",
        "en": "How to Connect from Windows?",
        "de": "Wie verbinde ich mich von Windows?",
        "es": "¿Cómo conectarse desde Windows?",
        "fr": "Comment se connecter depuis Windows ?",
        "it": "Come connettersi da Windows?",
    },
    "win_files_guide_title": {
        "tr": "Windows'tan Dosya Paylaşımına Bağlanma Rehberi",
        "en": "Guide: Connecting to File Sharing from Windows",
        "de": "Anleitung: Verbindung zur Dateifreigabe von Windows",
        "es": "Guía: Conexión a la Carpeta Compartida desde Windows",
        "fr": "Guide : Connexion au Partage de Fichiers depuis Windows",
        "it": "Guida: Connessione alla Condivisione File da Windows",
    },
    "win_files_guide_step1_title": {
        "tr": "1. Yöntem: Tarayıcıdan Tek Tıkla Bağlanma (En Kolay)",
        "en": "Method 1: Connect via Browser (Easiest)",
        "de": "Methode 1: Über den Browser verbinden (Am einfachsten)",
        "es": "Método 1: Conectar por Navegador (Más Fácil)",
        "fr": "Méthode 1 : Se connecter via Navigateur (Le plus simple)",
        "it": "Metodo 1: Connetti via Browser (Più Semplice)",
    },
    "win_files_guide_step1_desc": {
        "tr": "Windows PC'de Chrome, Edge vb. tarayıcınızı açın ve adres çubuğuna şunu yazın:\n"
              "http://192.168.50.1:8080\n"
              "(Dosyaları sürükleyip bırakarak yükleyebilir veya anında indirebilirsiniz.)",
        "en": "Open Chrome, Edge, etc. on your Windows PC and enter in the address bar:\n"
              "http://192.168.50.1:8080\n"
              "(You can drag & drop files to upload or click to download immediately.)",
        "de": "Öffnen Sie Chrome, Edge usw. auf Ihrem Windows-PC und geben Sie ein:\n"
              "http://192.168.50.1:8080\n"
              "(Dateien per Drag & Drop hochladen oder direkt herunterladen.)",
        "es": "Abra Chrome, Edge, etc. en su PC con Windows y escriba:\n"
              "http://192.168.50.1:8080\n"
              "(Puede arrastrar y soltar archivos para subir o descargar directamente.)",
        "fr": "Ouvrez Chrome, Edge, etc. sur Windows et entrez dans la barre d'adresse :\n"
              "http://192.168.50.1:8080\n"
              "(Glissez-déposez des fichiers pour téléverser ou téléchargez directement.)",
        "it": "Apri Chrome, Edge, ecc. su Windows e inserisci nella barra degli indirizzi:\n"
              "http://192.168.50.1:8080\n"
              "(Trascina i file per caricarli o scaricali direttamente.)",
    },
    "win_files_guide_step2_title": {
        "tr": "2. Yöntem: Windows Dosya Gezgini (Ağ Klasörü / SMB)",
        "en": "Method 2: Windows File Explorer (Network Folder / SMB)",
        "de": "Methode 2: Windows Datei-Explorer (Netzwerkordner / SMB)",
        "es": "Método 2: Explorador de Archivos de Windows (Carpeta de Red / SMB)",
        "fr": "Méthode 2 : Explorateur de Fichiers Windows (Dossier Réseau / SMB)",
        "it": "Metodo 2: Esplora File di Windows (Cartella di Rete / SMB)",
    },
    "win_files_guide_step2_desc": {
        "tr": "Windows PC'de klavyeden [Win + R] tuşlarına basın (veya Dosya Gezgini adres çubuğuna tıklayın):\n"
              "\\\\192.168.50.1\\Genel\n"
              "yazıp Enter'a basın. Paylaşılan klasör doğrudan Windows içinde normal bir yerel klasör gibi açılacaktır.",
        "en": "On your Windows PC, press [Win + R] (or click the File Explorer address bar):\n"
              "Type: \\\\192.168.50.1\\Genel\n"
              "and press Enter. The shared folder will open directly like a native folder.",
        "de": "Drücken Sie auf dem Windows-PC [Win + R] (oder in die Explorer-Adressleiste):\n"
              "Eingeben: \\\\192.168.50.1\\Genel\n"
              "und Enter drücken. Der Ordner öffnet sich wie ein normaler lokaler Ordner.",
        "es": "En su PC con Windows, presione [Win + R] (o en la barra del Explorador):\n"
              "Escriba: \\\\192.168.50.1\\Genel\n"
              "y presione Enter. La carpeta se abrirá directamente como una carpeta nativa.",
        "fr": "Sur Windows, appuyez sur [Win + R] (ou dans la barre d'adresse) :\n"
              "Tapez : \\\\192.168.50.1\\Genel\n"
              "et validez. Le dossier s'ouvrira comme un dossier Windows classique.",
        "it": "Su Windows, premi [Win + R] (o nella barra degli indirizzi di Esplora File):\n"
              "Digita: \\\\192.168.50.1\\Genel\n"
              "e premi Invio. La cartella si aprirà direttamente come una cartella normale.",
    },
    "dialog_select_shared_folder": {
        "tr": "Paylaşılacak Klasörü Seçin",
        "en": "Select Folder to Share",
        "de": "Freizugebenden Ordner auswählen",
        "es": "Seleccione la Carpeta a Compartir",
        "fr": "Sélectionner le Dossier à Partager",
        "it": "Seleziona la Cartella da Condividere",
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
