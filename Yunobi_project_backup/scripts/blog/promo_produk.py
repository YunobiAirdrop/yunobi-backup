#!/usr/bin/env python3
"""Generator gambar promo produk afiliasi — desain e-commerce profesional.
Foto produk hero + badge PROMO + harga besar + nama produk + CTA.
Pakai: promo_produk.py --gambar foto.jpg --nama "Nama Produk" --harga "Rp99.000" --out promo.jpg [--warna "#FF6B35"]
"""
import argparse, os, textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def fb(size):
    return ImageFont.truetype(FONT_BOLD, size)

def fr(size):
    return ImageFont.truetype(FONT_REG, size)

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def bikin_promo(path_gambar, nama, harga, path_out, warna="#E63946",
                badge="PROMO SPESIAL", sub="Harga promo terbatas!"):
    aksen = hex2rgb(warna)
    # 1. background gradient lembut
    bg = Image.new("RGB", (W, H), (248, 249, 252))
    d = ImageDraw.Draw(bg)
    # aksen gradient di atas
    for i in range(300):
        r = int(aksen[0] + (255 - aksen[0]) * i / 300 * 0.85)
        g = int(aksen[1] + (255 - aksen[1]) * i / 300 * 0.85)
        b = int(aksen[2] + (255 - aksen[2]) * i / 300 * 0.85)
        d.line([(0, i), (W, i)], fill=(r, g, b))

    # 2. foto produk dalam kartu rounded besar
    try:
        foto = Image.open(path_gambar).convert("RGB")
    except Exception:
        foto = Image.new("RGB", (800, 800), (230, 230, 235))
    # square crop
    s = min(foto.width, foto.height)
    foto = foto.crop(((foto.width - s)//2, (foto.height - s)//2,
                      (foto.width + s)//2, (foto.height + s)//2))
    FW = 760
    foto = foto.resize((FW, FW), Image.LANCZOS)
    # kartu putih dengan bayangan
    pad = 24
    kartu = Image.new("RGB", (FW + pad*2, FW + pad*2), (255, 255, 255))
    bayangan = Image.new("RGB", (W, H), (248, 249, 252))
    # tempel kartu di tengah atas
    kx, ky = (W - kartu.width)//2, 170
    bg.paste(kartu, (kx, ky))
    bg.paste(foto, (kx + pad, ky + pad))
    d = ImageDraw.Draw(bg)
    # border halus kartu
    d.rounded_rectangle([kx, ky, kx + kartu.width, ky + kartu.height],
                        radius=36, outline=(225, 228, 235), width=3)

    # 3. badge PROMO (kiri atas kartu)
    f_badge = fb(40)
    tw = d.textlength(badge, font=f_badge)
    bx, by = kx - 10, ky - 34
    d.rounded_rectangle([bx, by, bx + tw + 56, by + 72], radius=36, fill=aksen)
    d.text((bx + 28, by + 14), badge, font=f_badge, fill="white")

    # 4. nama produk (di bawah kartu)
    y = ky + kartu.height + 50
    f_nama = fb(52)
    # wrap 2 baris
    kata = nama.split()
    baris, cur = [], ""
    for k in kata:
        t = (cur + " " + k).strip()
        if d.textlength(t, font=f_nama) > W - 160:
            baris.append(cur); cur = k
        else:
            cur = t
    if cur: baris.append(cur)
    baris = baris[:2]
    for b in baris:
        tw = d.textlength(b, font=f_nama)
        d.text(((W - tw)/2, y), b, font=f_nama, fill=(30, 30, 35))
        y += 66

    # 5. sub teks
    f_sub = fr(36)
    tw = d.textlength(sub, font=f_sub)
    d.text(((W - tw)/2, y + 6), sub, font=f_sub, fill=(120, 124, 135))
    y += 60

    # 6. harga besar
    f_harga = fb(88)
    tw = d.textlength(harga, font=f_harga)
    d.text(((W - tw)/2, y), harga, font=f_harga, fill=aksen)
    y += 110

    # 7. tombol CTA
    f_cta = fb(44)
    cta = "BELI SEKARANG \u25b6"
    tw = d.textlength(cta, font=f_cta)
    cx1, cy1 = (W - tw - 110)/2, y
    cx2, cy2 = cx1 + tw + 110, y + 88
    d.rounded_rectangle([cx1, cy1, cx2, cy2], radius=44, fill=aksen)
    d.text((cx1 + 55, cy1 + 20), cta, font=f_cta, fill="white")

    bg.save(path_out, "JPEG", quality=92)
    return path_out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gambar", required=True)
    ap.add_argument("--nama", required=True)
    ap.add_argument("--harga", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--warna", default="#E63946")
    ap.add_argument("--badge", default="PROMO SPESIAL")
    ap.add_argument("--sub", default="Harga promo terbatas!")
    a = ap.parse_args()
    print("promo jadi:", bikin_promo(a.gambar, a.nama, a.harga, a.out,
                                    a.warna, a.badge, a.sub))

if __name__ == "__main__":
    main()
