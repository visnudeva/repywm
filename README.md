# repywm

Fork of [pywm](https://github.com/jbuchermn/pywm) — the C / [wlroots](https://github.com/swaywm/wlroots) backend used by [renewm](https://github.com/visnudeva/renewm). Upstream **newm** and **pywm** are unmaintained; this pair exists so we can update wlroots and fix bugs for local testing.

Python still does layout and input logic; **repywm** owns rendering, surfaces, and seats.

Also see the community fork [pywm-atha](https://git.sr.ht/~atha/pywm-atha) (kept in sync with newer wlroots) if we need to pull fixes from there.

## With renewm

Prefer the renewm installer (installs this backend + the compositor):

```sh
cd ~/code/GITHUB/renewm
./install.sh
# later:
./install.sh --update
```

If `../repywm` sits next to the renewm checkout, that path is used in editable mode. Otherwise pip pulls `https://github.com/visnudeva/repywm`.

## Standalone install

```sh
# system deps: see Prerequisites below, or let renewm's install.sh handle Arch
pip3 install --user -e .
```

Package name on the Python side stays **`pywm`** (so renewm’s `from pywm import …` keeps working).

## Prerequisites

Same as upstream / wlroots:

* python, pip, gcc, meson, ninja, pkg-config
* wayland, wayland-protocols, xorg-xwayland
* EGL, GLESv2, libdrm, GBM, libinput, xkbcommon, udev, pixman, libseat

Arch (also installed by renewm’s script):

```sh
sudo pacman -S --needed python meson ninja wayland wayland-protocols \
  xorg-xwayland libinput libxkbcommon mesa pixman seatd \
  xcb-util-errors xcb-util-renderutil xcb-util-wm
```

## Develop

```sh
# Ryoku
cd ~/code/GITHUB/repywm
# …edit C/Python…
git add -A && git commit -m "…" && git push

# SweetPotatOs — from renewm tree
cd ~/code/GITHUB/renewm && ./install.sh --update
```

## License

Same as upstream: see the repository license / headers.
