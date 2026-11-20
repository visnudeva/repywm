#!/usr/bin/env bash
# Build pywm/_pywm.so with the *system* meson/ninja (not pip's isolated env).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

MESON_FLAGS=(-Dwlroots:examples=false -Dwlroots:werror=false)

if [[ ! -f subprojects/wlroots/meson.build ]]; then
  echo "wlroots submodule missing — run: git submodule update --init --recursive" >&2
  exit 1
fi

need_cmd() { command -v "$1" >/dev/null || { echo "missing: $1" >&2; exit 1; }; }
need_cmd meson
need_cmd ninja

rm -rf build
echo "[*] meson setup build ${MESON_FLAGS[*]}"
meson setup build "${MESON_FLAGS[@]}"
echo "[*] ninja -C build  (a few minutes)"
ninja -C build
so="$(ls -1 build/_pywm*.so | head -1)"
cp -f "$so" pywm/_pywm.so
ls -l pywm/_pywm.so
echo "[+] native build OK"
