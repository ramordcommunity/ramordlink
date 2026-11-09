#!/usr/bin/env bash
# Ramord Link - Local Installation & System Integration Script
# Official Contact: ramordhelp@gmail.com

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/.local/bin"
DESKTOP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons"
TARGET_BIN="${BIN_DIR}/ramord-link"
LEGACY_BIN="${BIN_DIR}/internet-paylasim"

echo "==> Installing Ramord Link..."

# 1. Ensure target directories exist
mkdir -p "${BIN_DIR}" "${DESKTOP_DIR}" "${ICON_DIR}/hicolor/scalable/apps"

# 2. Install executable runner into ~/.local/bin/ramord-link
cat << EOF > "${TARGET_BIN}"
#!/usr/bin/env bash
exec python3 "${SCRIPT_DIR}/main.py" "\$@"
EOF
chmod +x "${TARGET_BIN}"

# 3. Maintain backwards compatibility symlink for internet-paylasim
ln -sf "${TARGET_BIN}" "${LEGACY_BIN}"

# 4. Universal Icon Deployment across all discovered icon theme trees & resolutions
# (Ensures that regardless of which custom icon theme the user activates, our official icon is found)
RESOLUTIONS=(16 22 24 32 48 64 128 256 512)

# Deploy to all directories in ~/.local/share/icons
if [ -d "${ICON_DIR}" ]; then
    for tdir in "${ICON_DIR}"/*; do
        if [ -d "${tdir}" ]; then
            for app_dir in $(find "${tdir}" -type d -name "apps" 2>/dev/null); do
                cp -f "${SCRIPT_DIR}/assets/ramord-link.svg" "${app_dir}/ramord-link.svg" 2>/dev/null || true
                cp -f "${SCRIPT_DIR}/assets/ramord-link.svg" "${app_dir}/internet-paylasim.svg" 2>/dev/null || true
                
                pname="$(basename "$(dirname "${app_dir}")")"
                res=""
                if [[ "${pname}" =~ ^[0-9]+$ ]]; then
                    res="${pname}"
                elif [[ "${pname}" =~ ^([0-9]+)x[0-9]+$ ]]; then
                    res="${BASH_REMATCH[1]}"
                fi
                
                if [ -n "${res}" ] && command -v rsvg-convert >/dev/null 2>&1; then
                    rsvg-convert -w "${res}" -h "${res}" "${SCRIPT_DIR}/assets/ramord-link.svg" -o "${app_dir}/ramord-link.png" 2>/dev/null || true
                    cp -f "${app_dir}/ramord-link.png" "${app_dir}/internet-paylasim.png" 2>/dev/null || true
                elif command -v rsvg-convert >/dev/null 2>&1; then
                    rsvg-convert -w 128 -h 128 "${SCRIPT_DIR}/assets/ramord-link.svg" -o "${app_dir}/ramord-link.png" 2>/dev/null || true
                    cp -f "${app_dir}/ramord-link.png" "${app_dir}/internet-paylasim.png" 2>/dev/null || true
                fi
            done
            
            if command -v gtk-update-icon-cache >/dev/null 2>&1; then
                gtk-update-icon-cache -f -t "${tdir}" >/dev/null 2>&1 || true
            fi
        fi
    done
fi

# Also ensure standard pixmaps fallback directory (~/.local/share/pixmaps and /usr/share/pixmaps fallback)
mkdir -p "${HOME}/.local/share/pixmaps"
cp -f "${SCRIPT_DIR}/assets/ramord-link.svg" "${HOME}/.local/share/pixmaps/ramord-link.svg"
if command -v rsvg-convert >/dev/null 2>&1; then
    rsvg-convert -w 256 -h 256 "${SCRIPT_DIR}/assets/ramord-link.svg" -o "${HOME}/.local/share/pixmaps/ramord-link.png" 2>/dev/null || true
fi

# 5. Install Desktop File
cp -f "${SCRIPT_DIR}/assets/ramord-link.desktop" "${DESKTOP_DIR}/ramord-link.desktop"
rm -f "${DESKTOP_DIR}/internet-paylasim.desktop"

# 6. Update desktop and icon caches
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "${DESKTOP_DIR}" >/dev/null 2>&1 || true
fi

if command -v kbuildsycoca6 >/dev/null 2>&1; then
    kbuildsycoca6 --noincremental >/dev/null 2>&1 || true
fi

echo "==> Ramord Link installed successfully!"
echo "    Binary:  ${TARGET_BIN}"
echo "    Desktop: ${DESKTOP_DIR}/ramord-link.desktop"
echo "    Icon:    ${ICON_DIR}/hicolor/scalable/apps/ramord-link.svg"
