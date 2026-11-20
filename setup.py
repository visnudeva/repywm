import glob
import os
import shutil
import subprocess
import sys

from setuptools import setup

# Vendored wlroots 0.16 needs these on modern GCC / libinput (Arch 2025+).
MESON_FLAGS = [
    "-Dwlroots:examples=false",
    "-Dwlroots:werror=false",
]


def run(cmd):
    print("+", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    sys.stdout.write(proc.stdout or "")
    if proc.returncode != 0:
        raise SystemExit(
            "Fatal: command failed (%s): %s" % (proc.returncode, " ".join(cmd))
        )


def build_native():
    # Prefer a pre-built .so from install.sh (system meson). Pip's isolated
    # build env cannot import Arch's /usr/bin/meson (mesonbuild missing).
    if os.environ.get("REPYWM_SKIP_NATIVE") == "1" and os.path.isfile("pywm/_pywm.so"):
        print("+ REPYWM_SKIP_NATIVE=1 — using existing pywm/_pywm.so", flush=True)
        return

    if os.path.isfile("pywm/_pywm.so") and os.environ.get("REPYWM_FORCE_NATIVE") != "1":
        print("+ pywm/_pywm.so already present — skip native rebuild", flush=True)
        return

    if os.path.isdir("build"):
        try:
            run(["meson", "setup", "--reconfigure", "build", *MESON_FLAGS])
        except SystemExit:
            shutil.rmtree("build")
            run(["meson", "setup", "build", *MESON_FLAGS])
    else:
        run(["meson", "setup", "build", *MESON_FLAGS])

    run(["ninja", "-C", "build"])

    matches = sorted(glob.glob("build/_pywm*.so"))
    if not matches:
        raise SystemExit("Fatal: Could not find shared library build/_pywm*.so")
    so = matches[0]
    dest = os.path.join("pywm", "_pywm.so")
    print("+ copy %s -> %s" % (so, dest), flush=True)
    shutil.copy2(so, dest)


build_native()

setup(
    name="pywm",
    version="0.3",
    description="wlroots-based Wayland compositor with Python frontend (repywm fork)",
    url="https://github.com/visnudeva/repywm",
    author="Jonas Bucher",
    author_email="j.bucher.mn@gmail.com",
    package_data={"pywm": ["_pywm.so", "py.typed"]},
    packages=["pywm"],
    install_requires=["evdev", "imageio", "pycairo", "numpy"],
)
