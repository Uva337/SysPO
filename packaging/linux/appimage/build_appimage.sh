#!/bin/bash
# Build portable AppImage for SysAdminAssistant
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
  rm -rf dist build/linux "$SCRIPT_DIR/AppDir"
fi
command -v pyinstaller >/dev/null 2>&1 || { echo "[ERROR] PyInstaller not found"; exit 1; }
command -v wget >/dev/null 2>&1 || { echo "[ERROR] wget not found"; exit 1; }
python icon.py
pip install -r requirements.txt
pyinstaller packaging/windows/SysAdmin.spec --distpath dist/SysAdminAssistant-linux --workpath build/linux --clean
mkdir -p "$SCRIPT_DIR/AppDir/usr/bin"
cp -r dist/SysAdminAssistant-linux/* "$SCRIPT_DIR/AppDir/usr/bin/"
mkdir -p "$SCRIPT_DIR/AppDir/usr/share/icons/hicolor/128x128/apps"
mkdir -p "$SCRIPT_DIR/AppDir/usr/share/applications"
cp app_icon.png "$SCRIPT_DIR/AppDir/usr/share/icons/hicolor/128x128/apps/sysadmin.png"
cp packaging/linux/appimage/sysadmin.desktop "$SCRIPT_DIR/AppDir/"
APPIMAGE_TOOL="$SCRIPT_DIR/linuxdeploy-x86_64.AppImage"
if [ ! -f "$APPIMAGE_TOOL" ]; then
  wget -O "$APPIMAGE_TOOL" https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
  chmod +x "$APPIMAGE_TOOL"
fi
"$APPIMAGE_TOOL" --appdir "$SCRIPT_DIR/AppDir" --desktop-file "$SCRIPT_DIR/AppDir/sysadmin.desktop" --icon-file "$SCRIPT_DIR/AppDir/usr/share/icons/hicolor/128x128/apps/sysadmin.png" --output appimage
mv SysAdminAssistant*.AppImage SysAdminAssistant-1.0.0.AppImage
