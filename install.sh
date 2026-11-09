#!/usr/bin/env bash
# Ramord Link - Local Installation & System Integration Script
# Official Contact: ramordhelp@gmail.com

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/scalable/apps"
TARGET_BIN="${BIN_DIR}/ramord-link"
LEGACY_BIN="${BIN_DIR}/internet-paylasim"

echo "==> Installing Ramord Link..."

# 1. Ensure target directories exist
mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}"

# 2. Install executable runner into ~/.local/bin/ramord-link
cat << EOF > "${TARGET_BIN}"
#!/usr/bin/env bash
exec python3 "${SCRIPT_DIR}/main.py" "\$@"
EOF
chmod +x "${TARGET_BIN}"

# 3. Maintain backwards compatibility symlink for internet-paylasim
ln -sf "${TARGET_BIN}" "${LEGACY_BIN}"

# 4. Install Application Icon
cp -f "${SCRIPT_DIR}/assets/ramord-link.svg" "${ICON_DIR}/ramord-link.svg"
# Also provide legacy icon name if referenced anywhere
cp -f "${SCRIPT_DIR}/assets/ramord-link.svg" "${ICON_DIR}/internet-paylasim.svg"

# 5. Install Desktop File
cp -f "${SCRIPT_DIR}/assets/ramord-link.desktop" "${DESKTOP_DIR}/ramord-link.desktop"

# 6. Update desktop and icon caches if tools exist
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true
fi

if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t "${HOME}/.local/share/icons/hicolor" >/dev/null 2>&1 || true
fi

echo "==> Ramord Link installed successfully!"
echo "    Binary:  ${TARGET_BIN}"
echo "    Symlink: ${LEGACY_BIN} -> ${TARGET_BIN}"
echo "    Desktop: ${DESKTOP_DIR}/ramord-link.desktop"
echo "    Icon:    ${ICON_DIR}/ramord-link.svg"
