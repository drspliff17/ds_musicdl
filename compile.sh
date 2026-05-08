#!/usr/bin/env bash

_notify() {
  local msg="$1"
  local doExit="${2:-false}"

  if [[ -t 1 ]]; then
    echo "$msg"
  else
    notify-send -u low -t 2000 -a center-text "$msg"
  fi

  [[ "$doExit" == "true" ]] && exit 0
}

_createBackup() {
  local proot="$HOME/dev/python/musicdl"
  local backup_location="$proot/version_backup"
  local version_backup="$backup_location/$NEW_BUILD"

  if [[ -d "$version_backup" ]]; then
    read -rp "[WARNING] Backup exists. Overwrite? [y/N] " confirm
    [[ ! "$confirm" =~ ^[Yy]$ ]] && _notify "Cancelled Compilation" "true"
    rm -rf "$version_backup"
  fi

  mkdir -p \
    "$version_backup/build/linux" \
    "$version_backup/dist/linux"

  cp -r "$proot/build/linux/." "$version_backup/build/linux"
  cp -r "$proot/dist/linux/." "$version_backup/dist/linux"

  _notify "[INFO] Backup created at $version_backup"
}

_compileLinux() {
  pyinstaller \
    --clean \
    --onefile \
    --distpath dist/linux \
    --workpath build/linux \
    --add-binary "ffmpeg:." \
    --collect-all yt_dlp \
    --collect-all eyed3 \
    musicdl.py

  _notify "Compiled Linux Build: $NEW_BUILD"
}

_compileWindows() {
  wine python -m PyInstaller \
    --clean \
    --onefile \
    --distpath dist/windows \
    --workpath build/windows \
    --add-binary "ffmpeg.exe;." \
    --collect-all yt_dlp \
    --collect-all eyed3 \
    musicdl.py

  _notify "Compiled Windows Build: $NEW_BUILD"
}

BUILDINFO="$HOME/dev/python/musicdl/buildinfo"
[[ ! -f "$BUILDINFO" ]] && _notify "[ERROR] buildinfo missing" "true"

BUILD=$(cat "$BUILDINFO")
NEW_BUILD="$1"
[[ -z "$NEW_BUILD" ]] && _notify "[ERROR] Missing build number: Current = $BUILD" "true"
echo "$NEW_BUILD" >"$BUILDINFO"

cd ~/dev/python/musicdl
_createBackup
_compileLinux
_compileWindows
