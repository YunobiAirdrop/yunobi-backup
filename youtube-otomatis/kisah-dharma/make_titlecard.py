#!/usr/bin/env python3
"""Title card 1280x720 untuk Kisah Dharma."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
img = Image.new("RGB", (W, H), (12, 10, 8))
px = img.load()
# vertical gradient: dark warm brown to near-black
for y in range(H):
    t = y / H
    r = int(48 - 36 * t); g = int(30 - 22 * t); b = int(16 - 12 * t)
    for x in range(W):
        px[x, y] = (r, g, b)
d = ImageDraw.Draw(img)
f_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 110)
f_mid = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 44)
f_sml = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

def center(y, text, font, fill):
    bb = d.textbbox((0, 0), text, font=font)
    d.text(((W - (bb[2] - bb[0])) / 2, y), text, font=font, fill=fill)

center(120, "KISAH DHARMA", f_sml, (200, 170, 110))
center(250, "KISAH KARNA", f_big, (245, 210, 140))
center(400, "Ksatria yang Dikhianati Takdir", f_mid, (220, 200, 170))
# thin gold rule
d.line([(W//2 - 160, 500), (W//2 + 160, 500)], fill=(200, 170, 110), width=3)
img.save("/home/hatch/workspace/youtube-otomatis/kisah-dharma/titlecard.png")
print("titlecard ok")
