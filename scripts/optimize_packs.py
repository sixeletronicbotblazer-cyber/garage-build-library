#!/usr/bin/env python3
"""Optimize the pack mockup PNGs: keep alpha, downscale to 1000px, max compression."""
from PIL import Image
import os

SRC = "/home/z/my-project/work/assets_v2/assets"
DST = "/home/z/my-project/download/garage-build-library/assets"

for name in ("pack-starter-en.png", "pack-complete-en.png"):
    src = os.path.join(SRC, name)
    dst = os.path.join(DST, name)
    im = Image.open(src)
    print(name, "original:", im.size, f"{os.path.getsize(src)/1024:.0f} KB")
    if im.width > 1000:
        im = im.resize((1000, int(im.height * 1000 / im.width)), Image.LANCZOS)
    im.save(dst, "PNG", optimize=True)
    print(name, "optimized:", im.size, f"{os.path.getsize(dst)/1024:.0f} KB")
