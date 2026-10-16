#!/usr/bin/env python3
"""Build end title card PNG (1280x720) with PIL: MIDNIGHT DREAD TALES."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))

def font(size, bold=True):
    # pick a solid Noto face available on the system
    cands = [
        "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for c in cands:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def spaced(draw, xy, text, fnt, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        w = draw.textlength(ch, font=fnt)
        x += w + tracking
    return x

def main():
    W, H = 1280, 720
    img = Image.new("RGB", (W, H), (8, 8, 10))
    d = ImageDraw.Draw(img)
    # faint vignette-ish red accent line
    d.rectangle([W//2 - 120, H//2 + 40, W//2 + 120, H//2 + 44], fill=(120, 20, 20))
    title = "MIDNIGHT DREAD TALES"
    f1 = font(64)
    tw = sum(d.textlength(c, font=f1) + 14 for c in title) - 14
    spaced(d, ((W - tw)//2, H//2 - 90), title, f1, (235, 235, 240), 14)
    sub = "a new nightmare, every night"
    f2 = font(30)
    sw = d.textlength(sub, font=f2)
    d.text(((W - sw)//2, H//2 + 80), sub, font=f2, fill=(150, 150, 160))
    out = os.path.join(BASE, "endcard.png")
    img.save(out)
    print("OK:", out)

if __name__ == "__main__":
    main()
