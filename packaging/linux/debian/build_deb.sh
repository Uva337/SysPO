#!/bin/bash
# Build Debian package for SysAdminAssistant
set -e
CLEAN=0
for arg in "$@"; do
  # use --clean to remove previous builds
  [ "$arg" = "--clean" ] && CLEAN=1
done
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$SCRIPT_DIR/../.."
cd "$REPO_ROOT"
if [ $CLEAN -eq 1 ]; then
  rm -rf dist build/linux "$SCRIPT_DIR/usr/share/SysAdminAssistant"
fi
command -v pyinstaller >/dev/null 2>&1 || { echo "[ERROR] PyInstaller not found"; exit 1; }
command -v dpkg-deb >/dev/null 2>&1 || { echo "[ERROR] dpkg-deb not found"; exit 1; }
python icon.py
pip install -r requirements.txt
pyinstaller packaging/windows/SysAdmin.spec --distpath dist/SysAdminAssistant-linux --workpath build/linux --clean
mkdir -p "$SCRIPT_DIR/usr/share/SysAdminAssistant"
cp -r dist/SysAdminAssistant-linux/* "$SCRIPT_DIR/usr/share/SysAdminAssistant/"
mkdir -p "$SCRIPT_DIR/usr/bin" "$SCRIPT_DIR/usr/share/applications" "$SCRIPT_DIR/usr/share/icons/hicolor/128x128/apps"
cat > "$SCRIPT_DIR/usr/bin/sysadmin-assistant" <<'LAUNCH'
#!/bin/sh
exec /usr/share/SysAdminAssistant/SysAdminAssistant "$@"
LAUNCH
chmod 755 "$SCRIPT_DIR/usr/bin/sysadmin-assistant"
cp packaging/linux/appimage/sysadmin.desktop "$SCRIPT_DIR/usr/share/applications/sysadmin.desktop"
cp app_icon.png "$SCRIPT_DIR/usr/share/icons/hicolor/128x128/apps/sysadmin.png"
dpkg-deb --build "$SCRIPT_DIR" "sysadmin-assistant_1.0.0_amd64.deb"
echo "Debian package created: sysadmin-assistant_1.0.0_amd64.deb"
