#!/usr/bin/env python3
"""Generate Neko Catcher PWA icons (matcha tile + black cat face)."""
from PIL import Image, ImageDraw

DARK = (13, 59, 46)      # --dark-green
DEEP = (20, 84, 63)      # --deep-green
CAT = (26, 23, 20)       # cat body
MATCHA = (197, 224, 122) # glowing eyes
SAKURA = (255, 183, 197) # nose / inner ear


def vgradient(size, top, bottom):
    img = Image.new("RGB", (size, size), top)
    px = img.load()
    for y in range(size):
        t = y / (size - 1)
        # radial-ish: blend toward darker at edges/bottom
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(size):
            px[x, y] = (r, g, b)
    return img


def draw_cat(d, cx, cy, s):
    """Draw a centered black cat face. s = head half-width."""
    # Ears
    ear_h = s * 0.95
    d.polygon([(cx - s * 0.95, cy - s * 0.15),
               (cx - s * 0.55, cy - s * 0.15 - ear_h),
               (cx - s * 0.15, cy - s * 0.15)], fill=CAT)
    d.polygon([(cx + s * 0.15, cy - s * 0.15),
               (cx + s * 0.55, cy - s * 0.15 - ear_h),
               (cx + s * 0.95, cy - s * 0.15)], fill=CAT)
    # Inner ears (sakura)
    d.polygon([(cx - s * 0.72, cy - s * 0.20),
               (cx - s * 0.55, cy - s * 0.15 - ear_h * 0.62),
               (cx - s * 0.38, cy - s * 0.20)], fill=SAKURA)
    d.polygon([(cx + s * 0.38, cy - s * 0.20),
               (cx + s * 0.55, cy - s * 0.15 - ear_h * 0.62),
               (cx + s * 0.72, cy - s * 0.20)], fill=SAKURA)
    # Head (rounded)
    d.rounded_rectangle([cx - s, cy - s * 0.55, cx + s, cy + s * 0.95],
                        radius=s * 0.55, fill=CAT)
    # Eyes (matcha, glowing)
    ew, eh = s * 0.26, s * 0.40
    ey = cy - s * 0.02
    for ox in (-s * 0.42, s * 0.42):
        d.ellipse([cx + ox - ew / 2, ey - eh / 2,
                   cx + ox + ew / 2, ey + eh / 2], fill=MATCHA)
        # pupil
        d.ellipse([cx + ox - ew * 0.18, ey - eh * 0.32,
                   cx + ox + ew * 0.18, ey + eh * 0.32], fill=CAT)
    # Nose
    nw = s * 0.14
    d.polygon([(cx - nw, cy + s * 0.30),
               (cx + nw, cy + s * 0.30),
               (cx, cy + s * 0.46)], fill=SAKURA)
    # Mouth
    d.line([(cx, cy + s * 0.46), (cx, cy + s * 0.58)], fill=(58, 46, 40), width=max(2, int(s * 0.04)))
    d.arc([cx - s * 0.30, cy + s * 0.40, cx, cy + s * 0.72], 20, 160, fill=(58, 46, 40), width=max(2, int(s * 0.04)))
    d.arc([cx, cy + s * 0.40, cx + s * 0.30, cy + s * 0.72], 20, 160, fill=(58, 46, 40), width=max(2, int(s * 0.04)))


def make(size, cat_scale=0.34, supersample=4):
    S = size * supersample
    img = vgradient(S, DEEP, (6, 29, 22)).convert("RGBA")
    d = ImageDraw.Draw(img)
    draw_cat(d, S / 2, S / 2 - S * 0.02, S * cat_scale)
    return img.resize((size, size), Image.LANCZOS)


# Standard / maskable: cat kept within safe zone via smaller scale
for name, size, scale in [
    ("icon-192.png", 192, 0.40),
    ("icon-512.png", 512, 0.40),
    ("icon-maskable-512.png", 512, 0.30),  # smaller -> fits Android safe zone
    ("apple-touch-icon.png", 180, 0.40),
    ("favicon-32.png", 32, 0.42),
]:
    make(size, scale).save(name)
    print("wrote", name)
